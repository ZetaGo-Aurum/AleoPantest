import requests
import concurrent.futures
from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleo_pantest.core.logger import logger

class DirBrute(BaseTool):
    """Advanced Directory Brute Forcer with multi-threading support"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Directory Brute Forcer",
            category=ToolCategory.WEB,
            version="3.3.0",
            author="AleoPantest Team",
            description="Mencari direktori tersembunyi menggunakan wordlist dan multi-threading.",
            usage="aleopantest run dir-brute --url https://example.com --threads 10",
            requirements=["requests"],
            tags=["web", "recon", "brute-force"],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "url",
                    "label": "Target URL",
                    "type": "text",
                    "placeholder": "e.g. https://example.com",
                    "required": True
                },
                {
                    "name": "threads",
                    "label": "Threads",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 50
                },
                {
                    "name": "timeout",
                    "label": "Timeout (seconds)",
                    "type": "number",
                    "default": 5,
                    "min": 1,
                    "max": 30
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        self.common_dirs = [
            "admin", "login", "config", "api", "v1", "backup", ".git", ".env",
            "administrator", "dashboard", "uploads", "images", "includes",
            "css", "js", "scripts", "temp", "tmp", "old", "new", "test",
            "phpmyadmin", "db", "database", "sql", "wp-admin", "wp-content"
        ]

    def check_dir(self, base_url, directory, timeout):
        url = f"{base_url.rstrip('/')}/{directory}"
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=False)
            if r.status_code in [200, 301, 302, 403]:
                return {"dir": directory, "url": url, "status": r.status_code}
        except:
            pass
        return None

    def run(self, url: str = "", threads: int = 10, timeout: int = 5, **kwargs):
        if not url:
            self.add_error("URL is required")
            return self.get_results()

        self.audit_log(f"Starting Directory Brute Force: URL={url}, Threads={threads}")
        self.add_result(f"[*] Memulai brute force direktori pada {url}...")
        
        found_count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_dir = {executor.submit(self.check_dir, url, d, timeout): d for d in self.common_dirs}
            for future in concurrent.futures.as_completed(future_to_dir):
                result = future.result()
                if result:
                    found_count += 1
                    status_text = {
                        200: "OK",
                        301: "Moved Permanently",
                        302: "Found/Redirect",
                        403: "Forbidden"
                    }.get(result['status'], str(result['status']))
                    self.add_result(f"[+] Found: /{result['dir']} (Status: {result['status']} {status_text})")

        if found_count == 0:
            self.add_result("[-] Tidak ada direktori umum yang ditemukan.")
        else:
            self.add_result(f"[+] Selesai. Menemukan {found_count} direktori.")

        return self.get_results()
