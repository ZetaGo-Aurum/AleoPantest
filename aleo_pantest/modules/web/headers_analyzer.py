from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests

class HeadersAnalyzer(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="HTTP Headers Analyzer",
            category=ToolCategory.WEB,
            version="3.3.0",
            author="AleoPantest",
            description="Menganalisis HTTP security headers dari sebuah URL untuk menilai postur keamanan",
            usage="aleopantest run headers-analyzer --url <url>",
            example="aleopantest run headers-analyzer --url https://google.com",
            requirements=["requests"],
            tags=["web", "security", "headers", "recon"],
            form_schema=[
                {
                    "name": "url",
                    "label": "Target URL",
                    "type": "text",
                    "placeholder": "https://example.com",
                    "required": True
                },
                {
                    "name": "user_agent",
                    "label": "User-Agent",
                    "type": "text",
                    "default": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AleoPantest/3.3"
                }
            ]
        )
        super().__init__(metadata)

    def run(self, url: str = "", user_agent: str = "", **kwargs):
        if not url:
            self.add_error("URL is required")
            return self.get_results()

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        self.add_result(f"[*] Menganalisis header untuk: {url}")
        
        try:
            headers = {'User-Agent': user_agent} if user_agent else {}
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            resp_headers = response.headers

            security_headers = {
                "Strict-Transport-Security": "Mencegah serangan Man-in-the-Middle (HSTS).",
                "Content-Security-Policy": "Mencegah serangan XSS dan injeksi data.",
                "X-Frame-Options": "Mencegah serangan Clickjacking.",
                "X-Content-Type-Options": "Mencegah MIME type sniffing.",
                "Referrer-Policy": "Mengontrol informasi referrer yang dikirim.",
                "Permissions-Policy": "Mengontrol fitur browser (kamera, lokasi, dll).",
                "X-XSS-Protection": "Filter XSS pada browser lama (Legacy)."
            }

            found_count = 0
            self.add_result("\n[+] Hasil Analisis Header:")
            for header, desc in security_headers.items():
                val = resp_headers.get(header)
                if val:
                    self.add_result(f"  [PASS] {header}: {val}")
                    found_count += 1
                else:
                    self.add_result(f"  [FAIL] {header}: Missing!")
                    self.add_result(f"         Info: {desc}")

            score = int((found_count / len(security_headers)) * 100)
            self.add_result(f"\n[*] Security Score: {score}/100")
            
            if score < 50:
                self.add_result("[!] Rekomendasi: Server ini sangat kekurangan security headers. Segera implementasikan CSP dan HSTS.")
            elif score < 80:
                self.add_result("[!] Rekomendasi: Beberapa header penting masih hilang. Tingkatkan postur keamanan Anda.")
            else:
                self.add_result("[+] Bagus: Server memiliki postur keamanan header yang baik.")

        except Exception as e:
            self.add_error(f"Error fetching headers: {str(e)}")
            
        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
