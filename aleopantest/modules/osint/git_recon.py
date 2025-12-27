from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class GitRecon(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="GitHub Recon",
            category=ToolCategory.OSINT,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Mencari informasi publik tentang user atau organisasi di GitHub",
            usage="aleopantest run git-recon --org <name>",
            example="aleopantest run git-recon --org google",
            parameters={"org": "Nama user atau organisasi GitHub"},
            requirements=["requests"],
            tags=["osint", "github", "recon"]
        )
        super().__init__(metadata)

    def run(self, org: str = "", **kwargs):
        if not org: return {"error": "Organization/User name is required"}
        try:
            user_info = requests.get(f"https://api.github.com/users/{org}").json()
            repos = requests.get(f"https://api.github.com/users/{org}/repos?per_page=10").json()
            repo_list = [r['name'] for r in repos] if isinstance(repos, list) else []
            return {"user": org, "info": user_info, "latest_repos": repo_list}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, org: str = "", **kwargs) -> bool: return bool(org)
