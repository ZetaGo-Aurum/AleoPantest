"""
Email Finder Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import requests
import re
from typing import Dict, List, Any, Set

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class EmailFinder(BaseTool):
    """Email finder untuk mencari email addresses dari domain"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Email Finder",
            category=ToolCategory.OSINT,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Email finder untuk mencari email addresses yang terkait dengan domain menggunakan crawler dan search engine",
            usage="aleopantest run email-finder --domain target.com",
            requirements=["requests", "beautifulsoup4"],
            tags=["osint", "email", "reconnaissance", "information-gathering"],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "domain",
                    "label": "Target Domain",
                    "type": "text",
                    "placeholder": "e.g. example.com",
                    "required": True
                },
                {
                    "name": "use_search",
                    "label": "Use Search Engine",
                    "type": "boolean",
                    "default": True
                },
                {
                    "name": "hunter_api_key",
                    "label": "Hunter.io API Key (Optional)",
                    "type": "text",
                    "placeholder": "Enter your Hunter.io API key",
                    "required": False
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input with auto-detection"""
        domain = kwargs.get('domain') or kwargs.get('target')
        if not domain:
            self.add_error("Domain tidak boleh kosong. Silakan masukkan secara manual.")
            return False
        
        # Standardize domain (remove protocol if present)
        if "://" in domain:
            domain = domain.split("://")[-1].split("/")[0]
        
        self.target_domain = domain
        return True
    
    def extract_emails_from_html(self, html: str, domain: str = None) -> Set[str]:
        """Extract email addresses from HTML"""
        emails = set()
        
        # Regex pattern untuk email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(email_pattern, html)
        
        for match in matches:
            if domain:
                # Filter emails hanya dari domain tertentu
                if match.lower().endswith(domain.lower()):
                    emails.add(match.lower())
            else:
                emails.add(match.lower())
        
        return emails
    
    def search_hunter_io(self, domain: str, api_key: str) -> List[str]:
        """Search using Hunter.io API"""
        emails = []
        try:
            url = f"https://api.hunter.io/v2/domain-search"
            params = {'domain': domain, 'api_key': api_key}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for email_data in data.get('data', {}).get('emails', []):
                    emails.append(email_data['value'])
        except Exception as e:
            self.add_warning(f"Hunter.io search error: {e}")
        
        return emails

    def search_duckduckgo(self, domain: str) -> Set[str]:
        """Search for emails using DuckDuckGo"""
        emails = set()
        try:
            from duckduckgo_search import DDGS
            query = f'"{domain}" email'
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=20)
                for r in results:
                    found = self.extract_emails_from_html(r.get('body', '') + r.get('title', ''), domain)
                    emails.update(found)
        except Exception as e:
            self.add_warning(f"DuckDuckGo search error: {e}")
        return emails
    
    def run(self, **kwargs):
        """Find emails for domain"""
        self.set_core_params(**kwargs)
        if not self.validate_input(**kwargs):
            return self.get_results()
        
        domain = getattr(self, 'target_domain', kwargs.get('domain'))
        timeout = kwargs.get('timeout', 10)
        
        self.is_running = True
        self.clear_results()
        self.audit_log(f"Starting Email Finder: Domain={domain}")
        
        try:
            self.add_result(f"[*] Mencari email untuk domain: {domain}")
            
            found_emails = set()
            
            # 1. Direct Crawl
            self.add_result("[*] Mencoba merayapi website langsung...")
            urls_to_check = [
                f"http://{domain}",
                f"https://{domain}",
                f"https://www.{domain}",
                f"http://{domain}/contact",
                f"http://{domain}/about",
            ]
            
            for url in urls_to_check:
                try:
                    response = requests.get(url, timeout=timeout, headers={'User-Agent': 'Aleopantest/3.3.0'})
                    if response.status_code == 200:
                        emails = self.extract_emails_from_html(response.text, domain)
                        found_emails.update(emails)
                except:
                    pass
            
            # 2. Search Engine
            if kwargs.get('use_search', True):
                self.add_result("[*] Mencari melalui mesin pencari...")
                found_emails.update(self.search_duckduckgo(domain))
            
            # 3. Hunter.io
            api_key = kwargs.get('hunter_api_key')
            if api_key:
                self.add_result("[*] Mencari melalui Hunter.io...")
                hunter_emails = self.search_hunter_io(domain, api_key)
                found_emails.update(hunter_emails)
            
            if not found_emails:
                self.add_result("[-] Tidak ada email yang ditemukan.")
            else:
                self.add_result(f"[+] Berhasil menemukan {len(found_emails)} email:")
                for email in sorted(found_emails):
                    self.add_result(f"    - {email}")
            
            return self.get_results()
            
        except Exception as e:
            self.add_error(f"Email search failed: {e}")
            return self.get_results()
        finally:
            self.is_running = False
