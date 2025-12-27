from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

class WhoisHistory(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="WHOIS Analyzer",
            category=ToolCategory.OSINT,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Mendapatkan informasi detail WHOIS domain (Registrar, Expiry, Name Servers)",
            usage="aleopantest run whois-history --domain <domain>",
            example="aleopantest run whois-history --domain google.com",
            requirements=["python-whois"],
            tags=["osint", "whois", "domain", "recon"],
            form_schema=[
                {
                    "name": "domain",
                    "label": "Domain Name",
                    "type": "text",
                    "placeholder": "example.com",
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, domain: str = "", **kwargs):
        if not HAS_WHOIS:
            self.add_error("Library 'python-whois' tidak ditemukan. Silakan jalankan: pip install python-whois")
            return self.get_results()

        if not domain:
            self.add_error("Domain is required")
            return self.get_results()

        self.add_result(f"[*] Melakukan WHOIS lookup untuk: {domain}")
        
        try:
            w = whois.whois(domain)
            
            self.add_result(f"[+] Registrar: {w.registrar}")
            self.add_result(f"[+] Creation Date: {w.creation_date}")
            self.add_result(f"[+] Expiration Date: {w.expiration_date}")
            self.add_result(f"[+] Updated Date: {w.updated_date}")
            
            if w.name_servers:
                self.add_result(f"[+] Name Servers: {', '.join(w.name_servers) if isinstance(w.name_servers, list) else w.name_servers}")
            
            if w.emails:
                self.add_result(f"[+] Contact Emails: {', '.join(w.emails) if isinstance(w.emails, list) else w.emails}")
            
            self.add_result(f"[+] Organization: {w.org}")
            self.add_result(f"[+] Country: {w.country}")
            
        except Exception as e:
            self.add_error(f"Error during WHOIS lookup: {str(e)}")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
