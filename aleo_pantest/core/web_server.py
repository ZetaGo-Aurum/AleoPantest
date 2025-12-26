import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import io
import json
from pydantic import BaseModel
import os
import sys
from typing import Dict, Any, List
from datetime import datetime

from ..cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY
from ..core.automation import AutomationEngine
from ..core.base_tool import BaseTool

app = FastAPI(title="AleoPantest V3 API")
automation_engine = AutomationEngine()

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web_assets")
app.mount("/assets", StaticFiles(directory=static_path), name="assets")

class ToolRunRequest(BaseModel):
    tool_id: str
    target: str = ""
    params: Dict[str, Any] = {}

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/api/admin")
async def get_admin():
    return BaseTool.get_admin_info()

@app.get("/api/tools")
async def get_tools():
    # Return full metadata for all tools
    result = {}
    for cat, tools in TOOLS_BY_CATEGORY.items():
        result[cat] = []
        for tool_id in tools:
            if tool_id in TOOLS_REGISTRY:
                try:
                    instance = TOOLS_REGISTRY[tool_id]()
                    tool_data = instance.metadata.to_dict()
                    tool_data['id'] = tool_id
                    result[cat].append(tool_data)
                except Exception as e:
                    print(f"Error loading tool {tool_id}: {e}")
    return result

@app.post("/api/run")
async def run_tool(request: ToolRunRequest):
    if request.tool_id not in TOOLS_REGISTRY:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    try:
        # Get tool instance
        tool_class = TOOLS_REGISTRY[request.tool_id]
        tool_instance = tool_class()
        
        # Merge provided params with auto-filled ones
        final_params = {}
        if request.target:
            final_params = automation_engine.auto_fill_params(request.tool_id, request.target)
        
        # Override with specific params from form
        final_params.update(request.params)
        
        # Run tool
        result = tool_instance.run(**final_params)
        
        # Store results for potential download (in-memory simple cache)
        if not hasattr(app, 'last_results'):
            app.last_results = {}
        app.last_results[request.tool_id] = {
            'instance': tool_instance,
            'results': result,
            'timestamp': os.times()[4]
        }
        
        return result
    except Exception as e:
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
    print(f"🚀 AleoPantest Web Server starting at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_web_server(port=8002)
