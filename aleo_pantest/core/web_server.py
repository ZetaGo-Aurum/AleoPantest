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
        def mount(self, *args, **kwargs): pass
    app = DummyApp()

import io
import json
from pydantic import BaseModel
import os
from typing import Dict, Any, List
from datetime import datetime

from ..cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY
from ..core.automation import AutomationEngine
from ..core.base_tool import BaseTool

if HAS_WEB_DEPS:
    app = FastAPI(title="AleoPantest V3 API")
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
                        from ..core.logger import logger
                        logger.error(f"Error loading tool {tool_id}: {str(e)}")
        return result
    except Exception as e:
        from ..core.logger import logger
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
        
        # Run tool
        result = tool_instance.run(**final_params)
        
        if result is None:
            result = {"status": "success", "output": "Tool executed but returned no results.", "results": []}
        
        # Store results for potential download (in-memory simple cache)
        if not hasattr(app, 'last_results'):
            app.last_results = {}
        app.last_results[request.tool_id] = {
            'instance': tool_instance,
            'results': result,
            'timestamp': datetime.now().timestamp()
        }
        
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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

def start_web_server(host: str = "127.0.0.1", port: int = 8000):
    if not HAS_WEB_DEPS:
        print("❌ Error: Web dependencies (fastapi, uvicorn) are not installed.")
        print("💡 Run: pip install fastapi uvicorn")
        return

    print(f"🚀 AleoPantest Web Server starting at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_web_server(port=8002)
