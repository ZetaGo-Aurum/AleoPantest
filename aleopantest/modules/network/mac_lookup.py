from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class MACLookup(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="MAC Vendor Lookup",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencari informasi vendor berdasarkan MAC address",
            usage="aleopantest run mac-lookup --mac <mac_address>",
            example="aleopantest run mac-lookup --mac 00:00:5e:00:53:af",
            parameters={
                "mac": "MAC Address yang akan dicari (format: XX:XX:XX:XX:XX:XX)"
            },
            requirements=[],
            tags=["network", "mac", "recon"]
        )
        super().__init__(metadata)

    def run(self, mac: str = "", **kwargs):
        if not mac:
            return {"error": "MAC address is required"}
        
        try:
            # Using a free API for demonstration
            response = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
            if response.status_code == 200:
                return {
                    "mac": mac,
                    "vendor": response.text,
                    "status": "success"
                }
            else:
                return {"error": f"Vendor not found or API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, mac: str = "", **kwargs) -> bool:
        return len(mac.split(':')) == 6 or len(mac.split('-')) == 6
