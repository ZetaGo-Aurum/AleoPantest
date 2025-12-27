from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class IPInfo(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="IP Info Lookup",
            category=ToolCategory.UTILITIES,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Mendapatkan informasi detail tentang sebuah IP address",
            usage="aleopantest run ip-info --ip <ip>",
            example="aleopantest run ip-info --ip 8.8.8.8",
            parameters={"ip": "Target IP Address"},
            requirements=["requests"],
            tags=["utility", "ip", "recon"]
        )
        super().__init__(metadata)

    def run(self, ip: str = "", **kwargs):
        if not ip: return {"error": "IP is required"}
        try:
            r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, ip: str = "", **kwargs) -> bool: return bool(ip)
