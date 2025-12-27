from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class FirewallBypass(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Firewall Bypass Guide (Informational)",
            category=ToolCategory.SECURITY,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Menyediakan teknik dan referensi umum untuk melewati firewall (WAF/IPS)",
            usage="aleopantest run firewall-bypass",
            example="aleopantest run firewall-bypass",
            parameters={},
            requirements=[],
            tags=["security", "bypass", "waf"]
        )
        super().__init__(metadata)

    def run(self, **kwargs):
        techniques = [
            "IP Fragmentation",
            "HTTP Parameter Pollution",
            "Case Sensitivity Manipulation",
            "Unicode Encoding",
            "Using Proxy/VPN",
            "DNS Tunneling"
        ]
        return {"status": "success", "techniques": techniques, "note": "Gunakan teknik ini hanya untuk tujuan pengujian penetrasi legal."}

    def validate_input(self, **kwargs) -> bool: return True
