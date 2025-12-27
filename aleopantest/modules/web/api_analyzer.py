from typing import Dict, Any, List
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class APIAnalyzer(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="API Analyzer",
            description="Analyze web API endpoints for common vulnerabilities and documentation",
            version="3.0.0",
            author="Aleocrophic Team",
            category=ToolCategory.WEB,
            usage="aleopantest run api-analyzer --url <api_url>",
            requirements=["requests"],
            tags=["web", "api", "analyzer", "vulnerability"],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "url",
                    "label": "Base API URL",
                    "type": "text",
                    "placeholder": "https://api.example.com/v1",
                    "required": True
                },
                {
                    "name": "headers",
                    "label": "Custom Headers (JSON)",
                    "type": "textarea",
                    "placeholder": '{"Authorization": "Bearer token"}'
                }
            ]
        )
        super().__init__(metadata)

    def run(self, url: str = "", headers: str = "", **kwargs) -> Dict[str, Any]:
        if not url:
            self.add_error("API URL is required")
            return self.get_results()

        self.add_result(f"[*] Analisis API pada: {url}")
        
        # Real logic to check common paths
        common_paths = [
            "/api", "/v1", "/v2", "/swagger.json", "/api-docs", 
            "/config", "/debug", "/env", "/health", "/metrics"
        ]
        
        custom_headers = {}
        if headers:
            try:
                import json
                custom_headers = json.loads(headers)
            except:
                self.add_error("Invalid JSON in headers")

        found = []
        for path in common_paths:
            test_url = url.rstrip('/') + path
            try:
                r = requests.get(test_url, headers=custom_headers, timeout=5, verify=False)
                if r.status_code != 404:
                    status = "Found"
                    if r.status_code == 200:
                        status = "Accessible (200 OK)"
                        if "swagger" in r.text.lower() or "openapi" in r.text.lower():
                            status += " [DOCS DETECTED]"
                    
                    self.add_result(f"[+] Endpoint: {test_url} - {status}")
                    found.append({"path": path, "status": r.status_code})
            except:
                pass

        if not found:
            self.add_result("[-] Tidak ditemukan endpoint standar.")
        else:
            self.add_result(f"\n[*] Total {len(found)} endpoint ditemukan.")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
