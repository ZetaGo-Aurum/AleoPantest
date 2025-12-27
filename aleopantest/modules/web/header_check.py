from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class HeaderChecker(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Security Header Checker",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Menganalisis HTTP security headers pada target website",
            usage="aleopantest run header-check --url <url>",
            example="aleopantest run header-check --url https://google.com",
            parameters={"url": "Target URL"},
            requirements=["requests"],
            tags=["web", "security", "headers"]
        )
        super().__init__(metadata)

    def run(self, url: str = "", **kwargs):
        if not url: return {"error": "URL is required"}
        if not url.startswith('http'): url = 'http://' + url
        try:
            resp = requests.get(url, timeout=10)
            headers = resp.headers
            security_headers = [
                "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options",
                "Strict-Transport-Security", "Referrer-Policy", "Permissions-Policy"
            ]
            results = {h: headers.get(h, "MISSING") for h in security_headers}
            return {"url": url, "headers": results}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, url: str = "", **kwargs) -> bool: return bool(url)
