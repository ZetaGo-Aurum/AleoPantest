import io
import json
import time
import os
import traceback
import logging
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

# Initialize logger
try:
    from .logger import logger
except (ImportError, ValueError):
    try:
        from aleo_pantest.core.logger import logger
    except ImportError:
        logger = logging.getLogger("Aleocrophic-Fallback")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

try:
    import uvicorn
    from fastapi import FastAPI, HTTPException
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse, Response
    HAS_WEB_DEPS = True
except ImportError:
    HAS_WEB_DEPS = False
    # Define dummy classes for type hinting if needed
    class FastAPI: pass
    class HTTPException(Exception): pass
    class StaticFiles: pass
    class FileResponse: pass
    class JSONResponse: pass
    class Response: pass
    
    class DummyApp:
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
        def delete(self, *args, **kwargs): return lambda f: f
        def mount(self, *args, **kwargs): pass
        def exception_handler(self, *args, **kwargs): return lambda f: f
    app = DummyApp()

# Use relative imports for other components
try:
    from ..cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY
    from .automation import AutomationEngine
    from .base_tool import BaseTool
except (ImportError, ValueError):
    from aleo_pantest.cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY
    from aleo_pantest.core.automation import AutomationEngine
    from aleo_pantest.core.base_tool import BaseTool

if HAS_WEB_DEPS:
    app = FastAPI(title="Aleocrophic V3 API")
    automation_engine = AutomationEngine()

    # Serve static files
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web_assets")
    if os.path.exists(static_path):
        app.mount("/assets", StaticFiles(directory=static_path), name="assets")
else:
    # app is already a DummyApp from the try-except block
    automation_engine = None
    static_path = ""

class ToolRunRequest(BaseModel):
    tool_id: str
    target: str = ""
    params: Dict[str, Any] = {}

@app.get("/")
@app.get("/index.html")
async def read_index():
    path = os.path.join(static_path, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse(status_code=404, content={"message": "index.html not found in web_assets"})

@app.get("/favicon.ico")
async def favicon():
    icon_path = os.path.join(static_path, "favicon.ico")
    if os.path.exists(icon_path):
        return FileResponse(icon_path)
    # Return empty 204 to avoid 404 in logs
    return Response(status_code=204)

@app.get("/api/admin")
async def get_admin():
    try:
        return BaseTool.get_admin_info()
    except Exception as e:
        return {"username": "Hunter", "hostname": "localhost", "status": "online"}

@app.post("/api/report")
async def report_result(data: Dict[str, Any]):
    """Endpoint for terminal tools to report results to the web dashboard"""
    try:
        if not hasattr(app, 'terminal_reports'):
            app.terminal_reports = []
        
        report = {
            "id": f"term_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        app.terminal_reports.insert(0, report)
        # Keep last 50 reports
        app.terminal_reports = app.terminal_reports[:50]
        
        logger.info(f"Received terminal report: {data.get('tool_id', 'unknown')}")
        return {"status": "success", "message": "Report received"}
    except Exception as e:
        logger.error(f"Error receiving terminal report: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/api/reports")
async def get_reports():
    """Endpoint to retrieve terminal reports for the web dashboard"""
    if not hasattr(app, 'terminal_reports'):
        return {"results": []}
    return {"results": app.terminal_reports}

@app.delete("/api/reports")
async def clear_reports():
    """Endpoint to clear terminal reports"""
    app.terminal_reports = []
    return {"status": "success", "message": "Reports cleared"}

@app.get("/api/tools")
async def get_tools():
    # Return full metadata for all tools
    result = {}
    try:
        for cat, tools in TOOLS_BY_CATEGORY.items():
            if not cat: continue
            result[cat] = []
            for tool_id in tools:
                if not tool_id: continue
                if tool_id in TOOLS_REGISTRY:
                    try:
                        tool_class = TOOLS_REGISTRY[tool_id]
                        if not tool_class: continue
                        instance = tool_class()
                        if not instance or not hasattr(instance, 'metadata') or not instance.metadata:
                            continue
                        tool_data = instance.metadata.to_dict()
                        tool_data['id'] = tool_id
                        result[cat].append(tool_data)
                    except Exception as e:
                        logger.error(f"Error loading tool {tool_id}: {str(e)}")
        return result
    except Exception as e:
        logger.error(f"Critical error in get_tools: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Failed to load tools", "error": str(e)})

@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found", "path": request.url.path}
    )

@app.post("/api/run")
async def run_tool(request: ToolRunRequest):
    if not request or not request.tool_id:
        raise HTTPException(status_code=400, detail="Invalid request: missing tool_id")
        
    if request.tool_id not in TOOLS_REGISTRY:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    try:
        # Get tool instance
        tool_class = TOOLS_REGISTRY[request.tool_id]
        if not tool_class:
            raise HTTPException(status_code=500, detail="Tool class not registered correctly")
            
        tool_instance = tool_class()
        if not tool_instance:
            raise HTTPException(status_code=500, detail="Failed to instantiate tool")
        
        # Merge provided params with auto-filled ones
        final_params = {}
        if request.target and automation_engine:
            try:
                final_params = automation_engine.auto_fill_params(request.tool_id, request.target)
            except Exception as e:
                print(f"Automation engine error: {e}")
        
        # Override with specific params from form
        if request.params:
            final_params.update(request.params)
        
        # Run tool with retry logic
        max_retries = 3
        retry_delay = 2
        result = None
        last_error = None
        
        # Start timing
        tool_instance.start_time = time.time()
        
        # Log to console/file but not to the web output capture yet
        logger.info(f"🚀 Running tool: {request.tool_id}")
        
        # Start log capturing for the response output
        log_capture = io.StringIO()
        capture_handler = logging.StreamHandler(log_capture)
        capture_handler.setLevel(logging.INFO)
        # Standard formatter without colors for web output
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        capture_handler.setFormatter(formatter)
        logger.addHandler(capture_handler)
        
        for attempt in range(max_retries):
            try:
                # Reset tool state for each attempt
                tool_instance.clear_results()
                tool_instance.status = "running"
                
                if attempt > 0:
                    logger.info(f"Retrying execution... (Attempt {attempt + 1}/{max_retries})")
                
                # Check if tool needs specific parameter normalization for web
                # Some tools might expect 'url' instead of 'target'
                if 'url' not in final_params and 'target' in final_params:
                    # Look at tool metadata to see if it expects 'url'
                    params_desc = tool_instance.metadata.parameters or {}
                    if 'url' in params_desc:
                        final_params['url'] = final_params.pop('target')
                elif 'target' not in final_params and 'url' in final_params:
                     params_desc = tool_instance.metadata.parameters or {}
                     if 'target' in params_desc:
                        final_params['target'] = final_params.pop('url')

                result = tool_instance.run(**final_params)
                
                # Use standard BaseTool state tracking
                if tool_instance.status == "failed" or tool_instance.errors:
                    # If it's a validation error (no results yet), don't retry
                    if not tool_instance.results and not result:
                        logger.warning(f"Validation failed for {request.tool_id}")
                        break
                    
                    if not result and not tool_instance.results:
                        logger.warning(f"Attempt {attempt + 1} failed for {request.tool_id}: No results returned")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                
                if result is not None or tool_instance.results:
                    tool_instance.status = "completed"
                    break
            except Exception as e:
                last_error = e
                tool_instance.status = "failed"
                logger.error(f"Execution error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        # Remove capture handler
        logger.removeHandler(capture_handler)
        captured_logs = log_capture.getvalue()
        
        # Get standardized summary
        summary = tool_instance.get_summary()
        
        # Format the final output string exactly as requested
        status_icon = "✓" if summary['status'] == "completed" else "❌"
        status_text = "Execution completed successfully" if summary['status'] == "completed" else f"Execution failed: {tool_instance.errors[0] if tool_instance.errors else 'Unknown error'}"
        
        # Consolidate results for display
        final_results = tool_instance.get_results()
        display_results = []
        
        if isinstance(final_results, dict):
            if "results" in final_results:
                display_results = final_results["results"]
            else:
                display_results = final_results
        else:
            display_results = final_results if final_results else (result if isinstance(result, list) else [result] if result else [])

        # If it's a list with one object, show just the object for cleaner output
        if isinstance(display_results, list) and len(display_results) == 1:
            display_results = display_results[0]

        # Construct visual output
        visual_output = f"🚀 Running: {request.tool_id}\n"
        visual_output += captured_logs.rstrip() + "\n" if captured_logs.strip() else ""
        visual_output += f"\n{status_icon} {status_text}\n\n"
        visual_output += "📊 Results:\n"
        
        if display_results:
            try:
                visual_output += json.dumps(display_results, indent=2)
            except (TypeError, ValueError):
                visual_output += str(display_results)
        else:
            visual_output += "{}"
        
        # Check if we have a valid result or if the tool failed
        if summary['status'] == "failed" and not tool_instance.results:
            status = "error"
            message = tool_instance.errors[0] if tool_instance.errors else "Tool execution failed"
            
            response_data = {
                "status": "error",
                "message": message,
                "tool_id": request.tool_id,
                "timestamp": datetime.now().isoformat(),
                "results": {
                    "results": [], 
                    "errors": tool_instance.errors,
                    "warnings": tool_instance.warnings,
                    "summary": summary
                },
                "output": visual_output
            }
            return response_data
        
        # Consolidate results for API response
        api_results = tool_instance.get_results()
            
        # Add metadata for web consistency
        response_data = {
            "status": "success",
            "message": f"Execution completed with {summary['results_count']} results" if summary['results_count'] > 0 else "Execution completed (no results)",
            "tool_id": request.tool_id,
            "timestamp": datetime.now().isoformat(),
            "results": {
                "results": api_results,
                "errors": tool_instance.errors,
                "warnings": tool_instance.warnings,
                "summary": summary
            },
            "output": visual_output
        }
        
        # If results are empty but status is success, add a helpful message
        if summary['results_count'] == 0 and summary['status'] != "failed":
            response_data["message"] = "Execution completed successfully, but no vulnerabilities or data were found."
            # Visual output already handled above
        
        # Store results for potential download (in-memory simple cache)
        if not hasattr(app, 'last_results'):
            app.last_results = {}
        app.last_results[request.tool_id] = {
            'instance': tool_instance,
            'results': result,
            'timestamp': datetime.now().timestamp()
        }
        
        return response_data
    except Exception as e:
        # Ensure capture handler is removed even if error occurs
        if 'logger' in locals() and 'capture_handler' in locals():
            logger.removeHandler(capture_handler)
            
        traceback.print_exc()
        error_msg = f"Unexpected error running tool {request.tool_id}: {str(e)}"
        logger.error(error_msg)
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": error_msg,
                "tool_id": request.tool_id,
                "timestamp": datetime.now().isoformat(),
                "traceback": traceback.format_exc() if os.environ.get("DEBUG") else None
            }
        )

@app.get("/api/download/{tool_id}/{format}")
async def download_results(tool_id: str, format: str):
    if not hasattr(app, 'last_results') or tool_id not in app.last_results:
        raise HTTPException(status_code=404, detail="No results found for this tool. Run it first.")
    
    cache = app.last_results[tool_id]
    tool_instance = cache['instance']
    results = cache['results']
    
    if format == "json":
        data = {
            'tool': tool_instance.metadata.name,
            'version': tool_instance.metadata.version,
            'timestamp': datetime.now().isoformat(),
            'results': results.get('results', []),
            'errors': results.get('errors', []),
            'warnings': results.get('warnings', [])
        }
        return JSONResponse(
            content=data,
            headers={"Content-Disposition": f"attachment; filename={tool_id}_results.json"}
        )
    elif format == "txt":
        output = f"=== {tool_instance.metadata.name} v{tool_instance.metadata.version} Report ===\n"
        output += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"Description: {tool_instance.metadata.description}\n\n"
        
        output += "--- RESULTS ---\n"
        for res in results.get('results', []):
            if isinstance(res, dict):
                for k, v in res.items():
                    output += f"{k}: {v}\n"
                output += "-" * 20 + "\n"
            else:
                output += f"{res}\n"
        
        if results.get('errors'):
            output += "\n--- ERRORS ---\n"
            for err in results.get('errors'):
                output += f"ERROR: {err}\n"
                
        if results.get('warnings'):
            output += "\n--- WARNINGS ---\n"
            for warn in results.get('warnings'):
                output += f"WARNING: {warn}\n"
                
        return Response(
            content=output,
            media_type="text/plain; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename={tool_id}_results.txt"}
        )
    
    raise HTTPException(status_code=400, detail="Invalid format. Use 'json' or 'txt'.")

def start_web_server(host: str = "127.0.0.1", port: int = 8002):
    if not HAS_WEB_DEPS:
        print("❌ Error: Web dependencies (fastapi, uvicorn) are not installed.")
        print("💡 Run: pip install fastapi uvicorn")
        return

    print(f"🚀 Aleocrophic Web Server starting at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_web_server(port=8002)
