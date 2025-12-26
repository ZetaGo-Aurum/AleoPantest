"""CSRF Vulnerability Detector"""
import requests
from typing import Dict, List, Any
from bs4 import BeautifulSoup

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class CSRFDetector(BaseTool):
    """CSRF (Cross-Site Request Forgery) vulnerability detector"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="CSRF Detector",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="CSRF vulnerability detection dengan analisis form token",
            usage="csrf = CSRFDetector(); csrf.run(url='http://target.com/form')",
            requirements=["requests", "beautifulsoup4"],
            tags=["web", "csrf", "vulnerability", "testing"]
        )
        super().__init__(metadata)
    
    def validate_input(self, url: str, **kwargs) -> bool:
        """Validate input"""
        if not url:
            self.add_error("URL tidak boleh kosong")
            return False
        if not url.startswith(('http://', 'https://')):
            self.add_error("Invalid URL format")
            return False
        return True
    
    def check_csrf_protection(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Check if URL has CSRF protection"""
        result = {
            'url': url,
            'has_csrf_token': False,
            'token_names': [],
            'forms': [],
            'vulnerable': False
        }
        
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Common CSRF token names
            token_names = [
                'csrf', 'csrf_token', 'csrftoken', '_csrf', '__csrf__',
                'token', 'nonce', 'authenticity_token', '_token'
            ]
            
            # Find all forms
            forms = soup.find_all('form')
            
            for form in forms:
                form_info = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET').upper(),
                    'has_token': False,
                    'token_field': None
                }
                
                # Check for CSRF token in form
                for token_name in token_names:
                    # Check input fields
                    csrf_input = form.find('input', {'name': token_name})
                    if csrf_input:
                        form_info['has_token'] = True
                        form_info['token_field'] = token_name
                        result['has_csrf_token'] = True
                        result['token_names'].append(token_name)
                        break
                    
                    # Check hidden fields
                    hidden = form.find('input', {'type': 'hidden', 'name': token_name})
                    if hidden:
                        form_info['has_token'] = True
                        form_info['token_field'] = token_name
                        result['has_csrf_token'] = True
                        result['token_names'].append(token_name)
                        break
                
                # Forms without POST method without CSRF token are vulnerable
                if form_info['method'] == 'POST' and not form_info['has_token']:
                    result['vulnerable'] = True
                
                result['forms'].append(form_info)
            
            # If no CSRF token found in POST forms, likely vulnerable
            if forms and result['vulnerable']:
                logger.warning(f"Potential CSRF vulnerability in {url}")
        
        except Exception as e:
            logger.error(f"Error checking CSRF: {e}")
        
        return result
    
    def run(self, url: str, timeout: int = 10, **kwargs):
        """Test URL for CSRF"""
        if not self.validate_input(url, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Testing {url} for CSRF vulnerabilities")
            
            result = self.check_csrf_protection(url, timeout)
            
            self.add_result(result)
            logger.info(f"CSRF test completed. Vulnerable: {result['vulnerable']}")
            return result
            
        except Exception as e:
            self.add_error(f"CSRF test failed: {e}")
        finally:
            self.is_running = False
