from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import requests
import concurrent.futures

class SocialAnalyzer(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Social Analyzer",
            category=ToolCategory.OSINT,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Mencari keberadaan username di berbagai platform media sosial secara real-time",
            usage="Aleocrophic run social-analyzer --username <user>",
            example="Aleocrophic run social-analyzer --username john_doe",
            requirements=["requests"],
            tags=["osint", "username", "social", "recon"],
            form_schema=[
                {
                    "name": "username",
                    "label": "Username",
                    "type": "text",
                    "placeholder": "e.g. janesmith",
                    "required": True
                },
                {
                    "name": "timeout",
                    "label": "Timeout (s)",
                    "type": "number",
                    "default": 5
                }
            ]
        )
        super().__init__(metadata)

    def check_site(self, site: str, url_template: str, username: str, timeout: int):
        url = url_template.format(username)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Aleocrophic/3.3'
            }
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            # Basic check: 200 OK usually means found
            # Some sites return 404, some redirect to a 'not found' page
            if response.status_code == 200:
                # Extra validation for specific sites
                if "github.com" in url and "Not Found" in response.text:
                    return None
                return {"site": site, "url": url, "status": "Found"}
            return None
        except:
            return None

    def run(self, username: str = "", timeout: int = 5, **kwargs):
        if not username:
            self.add_error("Username is required")
            return self.get_results()
            
        self.add_result(f"[*] Mencari username '{username}' di berbagai platform...")
        
        platforms = {
            "Instagram": "https://www.instagram.com/{}",
            "Twitter": "https://twitter.com/{}",
            "GitHub": "https://github.com/{}",
            "LinkedIn": "https://www.linkedin.com/in/{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Facebook": "https://www.facebook.com/{}",
            "Pinterest": "https://www.pinterest.com/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Medium": "https://medium.com/@{}",
            "YouTube": "https://www.youtube.com/@{}",
            "Twitch": "https://www.twitch.tv/{}",
            "SoundCloud": "https://soundcloud.com/{}"
        }
        
        found = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_site = {executor.submit(self.check_site, site, url, username, timeout): site for site, url in platforms.items()}
            for future in concurrent.futures.as_completed(future_to_site):
                res = future.result()
                if res:
                    found.append(res)
                    self.add_result(f"[+] {res['site']}: {res['url']}")

        if not found:
            self.add_result("[-] Tidak ditemukan profil di platform manapun.")
        else:
            self.add_result(f"\n[*] Total {len(found)} profil ditemukan.")
            
        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
