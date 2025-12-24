"""Search Engine Dorking Tool"""
import requests
from typing import Dict, List, Any
from urllib.parse import urlencode

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class SearchEngineDorking(BaseTool):
    """Search engine dorking untuk advanced search dan information gathering"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Search Engine Dorking",
            category=ToolCategory.OSINT,
            version="1.0.0",
            author="AloPantest",
            description="Search engine dorking untuk advanced search queries dan OSINT",
            usage="dorking = SearchEngineDorking(); dorking.run(query='site:target.com filetype:pdf')",
            requirements=["requests"],
            tags=["osint", "dorking", "search", "reconnaissance"]
        )
        super().__init__(metadata)
        
        # Common dork patterns
        self.dork_templates = {
            'exposed_admin': 'site:{domain} inurl:admin',
            'exposed_backup': 'site:{domain} filetype:sql OR filetype:bak',
            'exposed_config': 'site:{domain} filetype:conf OR filetype:config',
            'exposed_doc': 'site:{domain} filetype:pdf OR filetype:doc OR filetype:docx',
            'exposed_credentials': 'site:{domain} password OR username',
            'exposed_git': 'site:{domain} .git OR .gitconfig',
            'exposed_db': 'site:{domain} database OR db_config',
            'wordpress_admin': 'site:{domain} /wp-admin',
            'joomla_admin': 'site:{domain} /administrator',
            'cache_pages': 'cache:{domain}',
            'similar_sites': 'related:{domain}',
        }
    
    def validate_input(self, query: str = None, domain: str = None, **kwargs) -> bool:
        """Validate input"""
        if not query and not domain:
            self.add_error("Query atau domain harus disediakan")
            return False
        return True
    
    def build_dork_query(self, domain: str, dork_type: str) -> str:
        """Build dork query from template"""
        if dork_type in self.dork_templates:
            return self.dork_templates[dork_type].format(domain=domain)
        return f"site:{domain}"
    
    def search_google(self, query: str) -> List[Dict[str, Any]]:
        """Search using Google (simulated with requests)"""
        results = []
        
        try:
            # Note: Google may block automated requests
            # This is a simplified implementation
            url = "https://www.google.com/search"
            params = {'q': query, 'num': 10}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Parse search results
                for g in soup.find_all('div', class_='g'):
                    try:
                        title_element = g.find('h3')
                        link_element = g.find('a', href=True)
                        
                        if title_element and link_element:
                            title = title_element.text
                            link = link_element['href']
                            
                            results.append({
                                'title': title,
                                'url': link,
                                'source': 'Google'
                            })
                    except:
                        pass
        
        except Exception as e:
            logger.warning(f"Google search limited: {e}")
        
        return results
    
    def run(self, query: str = None, domain: str = None, dork_type: str = None, **kwargs):
        """Perform search engine dorking"""
        if not self.validate_input(query, domain, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            # Build query
            if domain and dork_type:
                search_query = self.build_dork_query(domain, dork_type)
                logger.info(f"Using dork query: {search_query}")
            elif domain:
                search_query = f"site:{domain}"
            else:
                search_query = query
            
            logger.info(f"Performing search: {search_query}")
            
            results = self.search_google(search_query)
            
            result = {
                'query': search_query,
                'results_found': len(results),
                'results': results
            }
            
            for res in results:
                self.add_result(res)
                logger.info(f"[+] {res['title'][:60]}")
            
            logger.info(f"Search completed. Found {len(results)} results")
            return result
            
        except Exception as e:
            self.add_error(f"Search dorking failed: {e}")
        finally:
            self.is_running = False
