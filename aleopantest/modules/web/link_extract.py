from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests
import re

class LinkExtractor(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Web Link Extractor",
            category=ToolCategory.WEB,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Mengekstrak semua link (href) dari sebuah halaman web",
            usage="aleopantest run link-extract --url <url>",
            example="aleopantest run link-extract --url https://example.com",
            parameters={"url": "Target URL"},
            requirements=["requests"],
            tags=["web", "recon", "crawler"]
        )
        super().__init__(metadata)

    def run(self, url: str = "", **kwargs):
        url = url or kwargs.get('target', '') or kwargs.get('url', '')
        if not url:
            self.add_error("URL is required")
            return self.get_results()
        try:
            r = requests.get(url, timeout=10)
            links = re.findall(r'href=["\'](https?://.*?)["\']', r.text)
            return {"url": url, "links_found": list(set(links))}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, url: str = "", **kwargs) -> bool: return bool(url)
