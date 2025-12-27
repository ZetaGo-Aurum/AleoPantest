from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests
import re

class LinkExtractor(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Web Link Extractor",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mengekstrak semua link (href) dari sebuah halaman web",
            usage="aleopantest run link-extract --url <url>",
            example="aleopantest run link-extract --url https://example.com",
            parameters={"url": "Target URL"},
            requirements=["requests"],
            tags=["web", "recon", "crawler"]
        )
        super().__init__(metadata)

    def run(self, url: str = "", **kwargs):
        if not url: return {"error": "URL is required"}
        try:
            r = requests.get(url, timeout=10)
            links = re.findall(r'href=["\'](https?://.*?)["\']', r.text)
            return {"url": url, "links_found": list(set(links))}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, url: str = "", **kwargs) -> bool: return bool(url)
