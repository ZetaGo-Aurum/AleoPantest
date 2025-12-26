import os

tools = [
    {
        "path": "aleo_pantest/modules/network/subnet_calc.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import ipaddress

class SubnetCalc(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Subnet Calculator",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Menghitung detail subnet IP (mask, network, broadcast, host range)",
            usage="aleopantest run subnet-calc --cidr <ip/prefix>",
            example="aleopantest run subnet-calc --cidr 192.168.1.0/24",
            parameters={"cidr": "IP Address dengan prefix CIDR"},
            requirements=[],
            tags=["network", "ip", "subnet"]
        )
        super().__init__(metadata)

    def run(self, cidr: str = "", **kwargs):
        if not cidr: return {"error": "CIDR is required"}
        try:
            net = ipaddress.ip_network(cidr, strict=False)
            return {
                "network": str(net.network_address),
                "netmask": str(net.netmask),
                "broadcast": str(net.broadcast_address),
                "num_addresses": net.num_addresses,
                "first_host": str(next(net.hosts())),
                "last_host": str(list(net.hosts())[-1])
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, cidr: str = "", **kwargs) -> bool: return bool(cidr)
"""
    },
    {
        "path": "aleo_pantest/modules/web/admin_finder.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class AdminFinder(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Admin Panel Finder",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencari lokasi halaman admin pada website",
            usage="aleopantest run admin-finder --url <url>",
            example="aleopantest run admin-finder --url https://example.com",
            parameters={"url": "Target URL"},
            requirements=["requests"],
            tags=["web", "recon", "admin"]
        )
        super().__init__(metadata)

    def run(self, url: str = "", **kwargs):
        if not url: return {"error": "URL is required"}
        admin_paths = ["admin/", "administrator/", "login.php", "wp-login.php", "backend/", "cp/", "controlpanel/"]
        found = []
        for path in admin_paths:
            try:
                r = requests.get(f"{url.rstrip('/')}/{path}", timeout=3)
                if r.status_code == 200:
                    found.append(f"{url.rstrip('/')}/{path}")
            except: pass
        return {"url": url, "found_admin_panels": found}

    def validate_input(self, url: str = "", **kwargs) -> bool: return bool(url)
"""
    },
    {
        "path": "aleo_pantest/modules/osint/phone_lookup.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class PhoneLookup(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Phone Number Lookup (Simulated)",
            category=ToolCategory.OSINT,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencari informasi tentang nomor telepon (Negara, Provider, Tipe)",
            usage="aleopantest run phone-lookup --number <phone_number>",
            example="aleopantest run phone-lookup --number +628123456789",
            parameters={"number": "Nomor telepon internasional"},
            requirements=[],
            tags=["osint", "phone", "recon"]
        )
        super().__init__(metadata)

    def run(self, number: str = "", **kwargs):
        if not number: return {"error": "Phone number is required"}
        return {
            "number": number,
            "country": "Indonesia (Simulated)",
            "provider": "Telkomsel (Simulated)",
            "type": "Mobile",
            "valid": True
        }

    def validate_input(self, number: str = "", **kwargs) -> bool: return bool(number)
"""
    },
    {
        "path": "aleo_pantest/modules/security/firewall_bypass.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

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
"""
    },
    {
        "path": "aleo_pantest/modules/crypto/rsa_gen.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import secrets

class RSAGen(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="RSA Key Pair Generator (Simple)",
            category=ToolCategory.CRYPTO,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Membuat pasangan kunci RSA sederhana (untuk demonstrasi)",
            usage="aleopantest run rsa-gen",
            example="aleopantest run rsa-gen",
            parameters={},
            requirements=[],
            tags=["crypto", "rsa", "generator"]
        )
        super().__init__(metadata)

    def run(self, **kwargs):
        # Placeholder for real RSA generation (requires cryptography lib)
        return {
            "public_key": "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\\n-----END PUBLIC KEY-----",
            "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEA...\\n-----END PRIVATE KEY-----",
            "note": "Ini adalah kunci simulasi. Gunakan library 'cryptography' untuk penggunaan produksi."
        }

    def validate_input(self, **kwargs) -> bool: return True
"""
    },
    {
        "path": "aleo_pantest/modules/utilities/cron_gen.py",
        "content": """from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class CronGen(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Cron Expression Generator",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Membuat ekspresi cron untuk jadwal tugas otomatis",
            usage="aleopantest run cron-gen --minute <m> --hour <h>",
            example="aleopantest run cron-gen --minute 0 --hour 12",
            parameters={
                "minute": "Menit (0-59)",
                "hour": "Jam (0-23)",
                "dom": "Day of Month (1-31)",
                "month": "Bulan (1-12)",
                "dow": "Day of Week (0-6)"
            },
            requirements=[],
            tags=["utility", "cron", "automation"]
        )
        super().__init__(metadata)

    def run(self, minute="*", hour="*", dom="*", month="*", dow="*", **kwargs):
        expression = f"{minute} {hour} {dom} {month} {dow}"
        return {"expression": expression, "explanation": f"Tugas akan berjalan pada menit {minute}, jam {hour}, hari {dom}, bulan {month}, dan hari ke-{dow}."}

    def validate_input(self, **kwargs) -> bool: return True
"""
    }
]

for tool in tools:
    os.makedirs(os.path.dirname(tool["path"]), exist_ok=True)
    with open(tool["path"], "w", encoding="utf-8") as f:
        f.write(tool["content"])
    print(f"Created: {tool['path']}")
