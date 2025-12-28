"""
XSS Vulnerability Detector

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import requests
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse, parse_qs

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class XSSDetector(BaseTool):
    """XSS (Cross-Site Scripting) vulnerability detector"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="XSS Detector",
            category=ToolCategory.WEB,
            version="3.0.0",
            author="Aleocrophic Team",
            description="XSS vulnerability detection dengan berbagai payload testing",
            usage="xss = XSSDetector(); xss.run(url='http://target.com')",
            requirements=["requests"],
            tags=["web", "xss", "vulnerability", "testing"],
            form_schema=[
                {
                    "name": "url",
                    "label": "Target URL",
                    "type": "text",
                    "placeholder": "http://example.com/page.php?id=1",
                    "required": True
                },
                {
                    "name": "parameter",
                    "label": "Specific Parameter (Optional)",
                    "type": "text",
                    "placeholder": "e.g. id",
                    "required": False
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        
        self.payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            '<body onload=alert("XSS")>',
            '"><script>alert("XSS")</script>',
            '<iframe src="javascript:alert(\'XSS\')">',
            '<input onfocus=alert("XSS")>',
            '<marquee onstart=alert("XSS")>',
            '<details open ontoggle=alert("XSS")>',
            'javascript:alert("XSS")',
            'data:text/html,<script>alert("XSS")</script>',
        ]
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input with auto-detection"""
        url = kwargs.get('url') or kwargs.get('target')
        if not url:
            self.add_error("URL tidak boleh kosong. Silakan masukkan secara manual.")
            return False
        
        if not url.startswith(('http://', 'https://')):
            # Try to fix URL if it's just a domain
            url = "http://" + url
            
        self.target_url = url
        return True
    
    def test_parameter(self, url: str, param: str, timeout: int = 10) -> Dict[str, Any]:
        """Test single parameter for XSS"""
        results = {
            'parameter': param,
            'vulnerable': False,
            'payloads_tested': 0,
            'successful_payloads': []
        }
        
        try:
            parsed = urlparse(url)
            
            for payload in self.payloads:
                results['payloads_tested'] += 1
                
                try:
                    if parsed.query:
                        # Test GET parameter
                        params = parse_qs(parsed.query)
                        params[param] = [payload]
                        
                        test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?"
                        test_url += '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                    else:
                        params = {param: payload}
                        test_url = url
                    
                    response = requests.get(test_url, params=params if not parsed.query else None, 
                                          timeout=timeout)
                    
                    # Check if payload reflected in response
                    if payload in response.text or payload.replace('"', '') in response.text:
                        results['vulnerable'] = True
                        results['successful_payloads'].append({
                            'payload': payload[:50],
                            'type': 'reflected'
                        })
                        logger.warning(f"Potential XSS found: {payload[:50]}")
                
                except requests.exceptions.RequestException:
                    pass
        
        except Exception as e:
            logger.error(f"Error testing parameter {param}: {e}")
        
        return results
    
    def run(self, **kwargs):
        """Test URL for XSS"""
        if not self.validate_input(**kwargs):
            return
        
        url = getattr(self, 'target_url', kwargs.get('url'))
        parameter = kwargs.get('parameter')
        timeout = kwargs.get('timeout', 10)
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Testing {url} for XSS vulnerabilities")
            
            parsed_url = urlparse(url)
            
            result = {
                'url': url,
                'vulnerable': False,
                'parameters': []
            }
            
            if parameter:
                param_result = self.test_parameter(url, parameter, timeout)
                result['parameters'].append(param_result)
                if param_result['vulnerable']:
                    result['vulnerable'] = True
            else:
                # Test all parameters
                params = parse_qs(parsed_url.query)
                for param in params.keys():
                    param_result = self.test_parameter(url, param, timeout)
                    result['parameters'].append(param_result)
                    if param_result['vulnerable']:
                        result['vulnerable'] = True
            
            self.add_result(result)
            logger.info(f"XSS test completed. Vulnerable: {result['vulnerable']}")
            return self.get_results()
            
        except Exception as e:
            self.add_error(f"XSS test failed: {e}")
        finally:
            self.is_running = False
