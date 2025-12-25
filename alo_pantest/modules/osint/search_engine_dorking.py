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
        """Search using Google - with fallback strategy"""
        results = []
        
        try:
            # Try googlesearch library first (more reliable)
            try:
                from googlesearch import search
                
                logger.info(f"Attempting Google search using googlesearch library...")
                results = []
                for url in search(query, num_results=5, sleep_interval=1):
                    results.append({
                        'title': url,
                        'url': url,
                        'source': 'Google (googlesearch)'
                    })
                    if len(results) >= 5:
                        break
                
                if results:
                    return results
                    
            except ImportError:
                logger.warning("googlesearch library not installed")
            except Exception as e:
                logger.warning(f"googlesearch failed: {e}")
            
            # Fallback: Try requests with headers
            url = "https://www.google.com/search"
            params = {'q': query, 'num': 10}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            
            logger.info("Attempting Google search using requests...")
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Parse search results - Google's HTML structure
                    for g in soup.find_all('div', class_='g'):
                        try:
                            title_element = g.find('h3')
                            link_element = g.find('a', href=True)
                            
                            if title_element and link_element:
                                title = title_element.text
                                link = link_element['href']
                                
                                # Filter out Google's redirect links
                                if '/url?q=' in link:
                                    link = link.split('/url?q=')[1].split('&')[0]
                                
                                if link and title:
                                    results.append({
                                        'title': title,
                                        'url': link,
                                        'source': 'Google (requests)'
                                    })
                        except:
                            pass
                except ImportError:
                    logger.warning("BeautifulSoup not installed for parsing")
            else:
                logger.warning(f"Google returned status {response.status_code} - likely rate limited")
                # Return informational result
                results.append({
                    'title': 'Google Search Rate Limited',
                    'url': f'https://www.google.com/search?q={requests.utils.quote(query)}',
                    'source': 'Google (Direct URL)',
                    'note': 'Google blocks automated requests. Use the URL directly or try --engine duckduckgo'
                })
        
        except Exception as e:
            logger.warning(f"Google search error: {e}")
            results.append({
                'title': 'Search Error - Try Alternative',
                'url': f'https://www.google.com/search?q={requests.utils.quote(query)}',
                'source': 'Manual Search',
                'note': f'Automated search failed: {e}. Use duckduckgo engine instead: --engine duckduckgo'
            })
        
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
            logger.info(f"📌 Note: Google blocks automated requests. For better results, use: --engine duckduckgo")
            
            results = self.search_google(search_query)
            
            result = {
                'query': search_query,
                'results_found': len(results),
                'results': results,
                'note': 'Google search may be rate-limited. For better results, use advanced-dorking tool with --engine duckduckgo or --engine github'
            }
            
            for res in results:
                self.add_result(res)
                logger.info(f"[+] {res.get('title', 'N/A')[:60]}")
            
            logger.info(f"Search completed. Found {len(results)} results")
            return result
            
        except Exception as e:
            self.add_error(f"Search dorking failed: {e}")
        finally:
            self.is_running = False
