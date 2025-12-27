import requests
import concurrent.futures
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger

class AdminFinder(BaseTool):
    """Admin Panel Finder with comprehensive path list and multi-threading"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Admin Panel Finder",
            category=ToolCategory.WEB,
            version="3.3.0",
            author="Aleocrophic Team",
            description="Mencari lokasi halaman admin pada website menggunakan daftar path umum dan multi-threading.",
            usage="aleopantest run admin-finder --url https://example.com --threads 10",
            requirements=["requests"],
            tags=["web", "recon", "admin"],
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
        self.admin_paths = [
            "admin/", "administrator/", "login.php", "wp-login.php", "backend/", "cp/", "controlpanel/",
            "admin/login.php", "admin/index.php", "admin_login.php", "administrator/login.php",
            "administrator/index.php", "login/", "signin/", "manage/", "manager/", "webadmin/",
            "admin1.php", "admin2.php", "siteadmin/", "cmsadmin/", "wp-admin/", "phpmyadmin/"
        ]

    def check_path(self, base_url, path, timeout):
        url = f"{base_url.rstrip('/')}/{path}"
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                # Check if it looks like a login page
                login_keywords = ["login", "user", "password", "sign in", "username"]
                is_login = any(keyword in r.text.lower() for keyword in login_keywords)
                return {"path": path, "url": url, "is_login": is_login}
        except:
            pass
        return None

    def run(self, url: str = "", threads: int = 10, timeout: int = 5, **kwargs):
        if not url:
            self.add_error("URL is required")
            return self.get_results()

        self.audit_log(f"Starting Admin Panel Finder: URL={url}, Threads={threads}")
        self.add_result(f"[*] Mencari halaman admin pada {url}...")
        
        found_count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_path = {executor.submit(self.check_path, url, p, timeout): p for p in self.admin_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    found_count += 1
                    login_info = " (Terdeteksi form login)" if result['is_login'] else ""
                    self.add_result(f"[+] Found: {result['url']}{login_info}")

        if found_count == 0:
            self.add_result("[-] Tidak ada halaman admin umum yang ditemukan.")
        else:
            self.add_result(f"[+] Selesai. Menemukan {found_count} potensi halaman admin.")

        return self.get_results()
