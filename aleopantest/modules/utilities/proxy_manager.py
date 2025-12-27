"""Proxy Manager Tool"""
from typing import Dict, List, Any
import requests

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class ProxyManager(BaseTool):
    """Proxy manager untuk manage dan test proxy servers"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Proxy Manager",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Proxy manager untuk manage, test, dan rotate proxy servers",
            usage="pm = ProxyManager(); pm.run(test_url='http://httpbin.org/ip')",
            requirements=["requests"],
            tags=["utilities", "proxy", "anonymity", "network"]
        )
        super().__init__(metadata)
        self.proxies = []
        self.working_proxies = []
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input"""
        return True
    
    def add_proxy(self, proxy: str, proxy_type: str = 'http'):
        """Add proxy to list"""
        if proxy not in [p.get('proxy') for p in self.proxies]:
            self.proxies.append({
                'proxy': proxy,
                'type': proxy_type,
                'working': None
            })
    
    def test_proxy(self, proxy: str, test_url: str = 'http://httpbin.org/ip', 
                   timeout: int = 10) -> Dict[str, Any]:
        """Test single proxy"""
        result = {'proxy': proxy, 'status': 'unknown'}
        
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }
            
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            
            if response.status_code == 200:
                result['status'] = 'working'
                result['response_time'] = response.elapsed.total_seconds()
                logger.info(f"[+] Proxy working: {proxy}")
            else:
                result['status'] = 'slow'
                logger.warning(f"[-] Proxy slow/unresponsive: {proxy}")
        
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            logger.debug(f"Proxy timeout: {proxy}")
        except:
            result['status'] = 'dead'
            logger.debug(f"Proxy dead: {proxy}")
        
        return result
    
    def get_free_proxies(self) -> List[str]:
        """Get free proxies dari public source"""
        proxies = []
        
        try:
            # Attempt to get free proxies
            url = 'https://free-proxy-list.net/'
            response = requests.get(url, timeout=10)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table', {'class': 'table'})
            if table:
                for row in table.find_all('tr')[1:6]:  # Get first 5
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.append(f"{ip}:{port}")
        except:
            logger.warning("Could not retrieve free proxies")
        
        return proxies
    
    def run(self, test_url: str = 'http://httpbin.org/ip', proxy_list: List[str] = None, 
            get_free: bool = False, **kwargs):
        """Test and manage proxies"""
        if not self.validate_input(**kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            # Get proxies
            if get_free:
                logger.info("Fetching free proxies...")
                free_proxies = self.get_free_proxies()
                for proxy in free_proxies:
                    self.add_proxy(proxy)
            
            if proxy_list:
                for proxy in proxy_list:
                    self.add_proxy(proxy)
            
            logger.info(f"Testing {len(self.proxies)} proxies")
            
            working = []
            
            for proxy_info in self.proxies:
                result = self.test_proxy(proxy_info['proxy'], test_url)
                
                if result['status'] == 'working':
                    working.append(result)
                    self.working_proxies.append(proxy_info['proxy'])
                
                self.add_result(result)
            
            summary = {
                'total_proxies': len(self.proxies),
                'working_proxies': len(working),
                'working_list': self.working_proxies,
                'details': self.results
            }
            
            logger.info(f"Proxy test completed: {len(working)} working out of {len(self.proxies)}")
            return summary
            
        except Exception as e:
            self.add_error(f"Proxy test failed: {e}")
        finally:
            self.is_running = False
