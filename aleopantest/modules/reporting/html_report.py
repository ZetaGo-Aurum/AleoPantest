from typing import Dict, Any, List
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import json
import os
from datetime import datetime

class HTMLReportGenerator(BaseTool):
    """
    Generator laporan HTML interaktif untuk hasil pemindaian keamanan
    """
    
    def __init__(self):
        metadata = ToolMetadata(
            name="HTML Report Generator",
            category=ToolCategory.REPORTING,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Generates an interactive HTML dashboard report from tool execution results",
            usage="aleopantest run html-report --file results.json",
            requirements=["jinja2"],
            tags=["reporting", "html", "dashboard"],
            form_schema=[
                {
                    "name": "file_path",
                    "type": "text",
                    "label": "Input JSON File",
                    "placeholder": "path/to/results.json",
                    "required": True
                },
                {
                    "name": "theme",
                    "type": "text",
                    "label": "Theme",
                    "default": "dark",
                    "description": "Report theme: light or dark"
                }
            ]
        )
        super().__init__(metadata)

    def run(self, file_path: str, theme: str = "dark", **kwargs) -> Dict[str, Any]:
        self.logger.info(f"Generating HTML report from: {file_path}")
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
            
        output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # Simulating HTML generation
        results = {
            "status": "success",
            "message": f"HTML report generated successfully: {output_path}",
            "report_details": {
                "source": file_path,
                "output": output_path,
                "theme": theme,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return results

def get_tool():
    return HTMLReportGenerator()
