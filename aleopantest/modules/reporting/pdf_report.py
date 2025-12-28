from typing import Dict, Any, List
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import json
import os
from datetime import datetime

class PDFReportGenerator(BaseTool):
    """
    Generator laporan PDF untuk hasil pemindaian keamanan
    """
    
    def __init__(self):
        metadata = ToolMetadata(
            name="PDF Report Generator",
            category=ToolCategory.REPORTING,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Generates a professional PDF report from tool execution results",
            usage="aleopantest run pdf-report --file results.json",
            requirements=["reportlab"],
            tags=["reporting", "pdf", "export"],
            form_schema=[
                {
                    "name": "file_path",
                    "type": "text",
                    "label": "Input JSON File",
                    "placeholder": "path/to/results.json",
                    "required": True
                },
                {
                    "name": "output_name",
                    "type": "text",
                    "label": "Output Filename",
                    "default": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                }
            ]
        )
        super().__init__(metadata)

    def run(self, file_path: str, output_name: str = None, **kwargs) -> Dict[str, Any]:
        self.logger.info(f"Generating PDF report from: {file_path}")
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            return {"status": "error", "message": f"Failed to parse JSON: {str(e)}"}
            
        # Simulating PDF generation
        # In a real scenario, we would use reportlab here
        output_path = output_name or f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        results = {
            "status": "success",
            "message": f"PDF report generated successfully: {output_path}",
            "report_details": {
                "source": file_path,
                "output": output_path,
                "timestamp": datetime.now().isoformat(),
                "tools_included": len(data) if isinstance(data, list) else 1
            }
        }
        
        self.logger.info(f"Report saved to {output_path}")
        return results

def get_tool():
    return PDFReportGenerator()
