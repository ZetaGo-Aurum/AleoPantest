"""Email Finder Tool"""
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
            version="1.0.0",
            author="AloPantest",
            description="Email finder untuk mencari email addresses yang terkait dengan domain",
            usage="finder = EmailFinder(); finder.run(domain='target.com')",
            requirements=["requests"],
            tags=["osint", "email", "reconnaissance", "information-gathering"]
        )
        super().__init__(metadata)
    
    def validate_input(self, domain: str, **kwargs) -> bool:
        """Validate input"""
        if not domain:
            self.add_error("Domain tidak boleh kosong")
            return False
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
                if match.endswith(domain) or domain in match:
                    emails.add(match)
            else:
                emails.add(match)
        
        return emails
    
    def search_hunter_io(self, domain: str) -> List[str]:
        """Search using Hunter.io API (requires API key)"""
        emails = []
        try:
            # Note: Requires API key
            api_key = kwargs.get('hunter_api_key')
            if not api_key:
                return emails
            
            url = f"https://api.hunter.io/v2/domain-search"
            params = {'domain': domain, 'limit': 100, 'offset': 0}
            headers = {'X-API-Key': api_key}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for email_data in data.get('data', {}).get('emails', []):
                    emails.append(email_data['value'])
        except Exception as e:
            logger.debug(f"Hunter.io search error: {e}")
        
        return emails
    
    def run(self, domain: str, timeout: int = 10, **kwargs):
        """Find emails for domain"""
        if not self.validate_input(domain, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Searching for emails associated with {domain}")
            
            found_emails = set()
            
            # Try common URLs on domain
            urls_to_check = [
                f"http://{domain}",
                f"https://{domain}",
                f"https://www.{domain}",
                f"http://www.{domain}",
            ]
            
            for url in urls_to_check:
                try:
                    response = requests.get(url, timeout=timeout)
                    emails = self.extract_emails_from_html(response.text, domain)
                    found_emails.update(emails)
                except:
                    pass
            
            # Hunter.io jika ada API key
            if 'hunter_api_key' in kwargs:
                hunter_emails = self.search_hunter_io(domain, **kwargs)
                found_emails.update(hunter_emails)
            
            result = {
                'domain': domain,
                'emails_found': len(found_emails),
                'emails': list(found_emails)
            }
            
            for email in found_emails:
                self.add_result({'email': email, 'domain': domain})
                logger.info(f"[+] Found email: {email}")
            
            logger.info(f"Email search completed. Found {len(found_emails)} emails")
            return result
            
        except Exception as e:
            self.add_error(f"Email search failed: {e}")
        finally:
            self.is_running = False
