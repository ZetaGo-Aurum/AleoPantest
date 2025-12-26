from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class UserSearch(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Username Searcher",
            category=ToolCategory.OSINT,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencari keberadaan username di berbagai platform media sosial",
            usage="Aleocrophic run user-search --username <target_username>",
            example="Aleocrophic run user-search --username zeta_go",
            parameters={
                "username": "Username yang ingin dicari"
            },
            requirements=["requests"],
            tags=["osint", "social", "recon"]
        )
        super().__init__(metadata)

    def run(self, username: str = "", **kwargs):
        if not username: return {"error": "Username is required"}
        
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "YouTube": f"https://youtube.com/@{username}",
        }
        
        results = {}
        for name, url in platforms.items():
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    results[name] = {"status": "Found", "url": url}
                else:
                    results[name] = {"status": "Not Found", "url": url}
            except:
                results[name] = {"status": "Error", "url": url}
                
        return {
            "username": username,
            "results": results
        }

    def validate_input(self, username: str = "", **kwargs) -> bool:
        return bool(username)
