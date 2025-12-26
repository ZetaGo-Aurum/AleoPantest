"""Web Crawler Tool"""
import requests
from typing import Dict, List, Any, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class WebCrawler(BaseTool):
    """Web crawler untuk mapping website structure"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Web Crawler",
            category=ToolCategory.WEB,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Web crawler untuk mapping struktur website dan discovery URL",
            usage="crawler = WebCrawler(); crawler.run(url='http://target.com', depth=2)",
            requirements=["requests", "beautifulsoup4"],
            tags=["web", "crawler", "mapping", "reconnaissance"]
        )
        super().__init__(metadata)
        self.visited_urls: Set[str] = set()
        self.urls_to_visit: List[str] = []
    
    def validate_input(self, url: str, depth: int = 1, **kwargs) -> bool:
        """Validate input"""
        if not url:
            self.add_error("URL tidak boleh kosong")
            return False
        if not url.startswith(('http://', 'https://')):
            self.add_error("Invalid URL format")
            return False
        if depth < 0 or depth > 5:
            self.add_error("Depth harus antara 0-5")
            return False
        return True
    
    def get_same_domain_urls(self, url: str, base_domain: str) -> List[str]:
        """Extract URLs from page that belong to same domain"""
        urls = []
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Skip anchors and javascript
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                
                # Convert relative URLs to absolute
                absolute_url = urljoin(url, href)
                
                # Check if same domain
                if urlparse(absolute_url).netloc == base_domain:
                    # Remove fragments
                    absolute_url = absolute_url.split('#')[0]
                    
                    if absolute_url not in self.visited_urls:
                        urls.append(absolute_url)
            
            # Also find forms
            for form in soup.find_all('form'):
                action = form.get('action', '')
                if action:
                    form_url = urljoin(url, action)
                    if urlparse(form_url).netloc == base_domain:
                        if form_url not in self.visited_urls:
                            urls.append(form_url)
        
        except Exception as e:
            logger.debug(f"Error crawling {url}: {e}")
        
        return urls
    
    def crawl(self, url: str, depth: int, current_depth: int = 0, base_domain: str = None):
        """Recursively crawl website"""
        if current_depth > depth or not self.is_running:
            return
        
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            logger.info(f"Crawling {url} (depth: {current_depth})")
            
            # Get page info
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            page_info = {
                'url': url,
                'status': response.status_code,
                'size': len(response.text),
                'depth': current_depth
            }
            
            self.add_result(page_info)
            
            # Find more URLs
            if current_depth < depth:
                new_urls = self.get_same_domain_urls(url, base_domain)
                for new_url in new_urls:
                    if new_url not in self.visited_urls:
                        self.crawl(new_url, depth, current_depth + 1, base_domain)
        
        except Exception as e:
            logger.debug(f"Error processing {url}: {e}")
    
    def run(self, url: str, depth: int = 1, **kwargs):
        """Start crawling"""
        if not self.validate_input(url, depth, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        self.visited_urls.clear()
        
        try:
            base_domain = urlparse(url).netloc
            logger.info(f"Starting web crawler on {url} (depth: {depth})")
            
            self.crawl(url, depth, 0, base_domain)
            
            result = {
                'url': url,
                'depth': depth,
                'urls_found': len(self.results),
                'unique_urls': list(self.visited_urls),
                'details': self.results
            }
            
            logger.info(f"Crawling completed. Found {len(self.results)} URLs")
            return result
            
        except Exception as e:
            self.add_error(f"Crawling failed: {e}")
        finally:
            self.is_running = False
