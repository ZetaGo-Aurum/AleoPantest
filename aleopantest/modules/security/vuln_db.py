import requests
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class VulnDB(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Vulnerability Database Search",
            category=ToolCategory.SECURITY,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Mencari informasi kerentanan pada database publik secara real-time (via CIRCL CVE API)",
            usage="aleopantest run vuln-db --query <cve_id>",
            example="aleopantest run vuln-db --query CVE-2021-44228",
            requirements=["requests"],
            tags=["security", "vulnerability", "cve", "nvd"],
            risk_level="LOW",
            form_schema=[
                {
                    "name": "query",
                    "label": "CVE ID (e.g. CVE-2021-44228)",
                    "type": "text",
                    "placeholder": "CVE-YYYY-NNNN",
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, query: str = "", **kwargs):
        if not query:
            self.add_error("CVE ID is required")
            return self.get_results()

        if not query.upper().startswith("CVE-"):
            self.add_error("Format CVE ID salah. Gunakan format: CVE-YYYY-NNNN")
            return self.get_results()

        self.add_result(f"[*] Mencari informasi untuk {query} di database CIRCL...")
        
        try:
            url = f"https://cve.circl.lu/api/cve/{query.upper()}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    self.add_result(f"[-] Data tidak ditemukan untuk {query}.")
                    return self.get_results()

                self.add_result(f"[+] CVE ID: {data.get('id', query)}")
                self.add_result(f"[+] Summary: {data.get('summary', 'No summary available')}")
                self.add_result(f"[+] Published: {data.get('Published', 'N/A')}")
                self.add_result(f"[+] Modified: {data.get('Modified', 'N/A')}")
                
                cvss = data.get('cvss')
                if cvss:
                    self.add_result(f"[!] CVSS Score: {cvss}")
                
                refs = data.get('references', [])
                if refs:
                    self.add_result("\n[+] References:")
                    for ref in refs[:5]: # Show top 5
                        self.add_result(f"    - {ref}")
            else:
                self.add_error(f"Gagal mengambil data dari API (Status: {response.status_code})")

        except Exception as e:
            self.add_error(f"Search failed: {str(e)}")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
