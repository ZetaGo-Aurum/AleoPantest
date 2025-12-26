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
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Search engine dorking untuk advanced search queries dan OSINT menggunakan Google dan DuckDuckGo",
            usage="Aleocrophic run search-engine-dorking --query 'site:target.com filetype:pdf' --engine duckduckgo",
            requirements=["requests", "beautifulsoup4", "duckduckgo-search"],
            tags=["osint", "dorking", "search", "reconnaissance"],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "query",
                    "label": "Search Query / Dork",
                    "type": "textarea",
                    "placeholder": "e.g. site:example.com filetype:php",
                    "required": False
                },
                {
                    "name": "domain",
                    "label": "Target Domain (Optional)",
                    "type": "text",
                    "placeholder": "e.g. example.com",
                    "required": False
                },
                {
                    "name": "dork_type",
                    "label": "Dork Template",
                    "type": "select",
                    "options": ["none", "exposed_admin", "exposed_backup", "exposed_config", "exposed_doc", "exposed_credentials", "exposed_git", "exposed_db", "wordpress_admin", "joomla_admin"],
                    "default": "none"
                },
                {
                    "name": "engine",
                    "label": "Search Engine",
                    "type": "select",
                    "options": ["google", "duckduckgo"],
                    "default": "duckduckgo"
                },
                {
                    "name": "num_results",
                    "label": "Number of Results",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 50
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        
        # Common dork patterns
        self.dork_templates = {
            'exposed_admin': 'site:{domain} inurl:admin',
            'exposed_backup': 'site:{domain} filetype:sql OR filetype:bak OR filetype:old',
            'exposed_config': 'site:{domain} filetype:conf OR filetype:config OR filetype:env OR filetype:ini',
            'exposed_doc': 'site:{domain} filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx',
            'exposed_credentials': 'site:{domain} "password" OR "username" OR "login" OR "credentials"',
            'exposed_git': 'site:{domain} inurl:".git" OR inurl:".gitconfig"',
            'exposed_db': 'site:{domain} "database" OR "db_config" OR "sql dump"',
            'wordpress_admin': 'site:{domain} inurl:/wp-admin OR inurl:/wp-login.php',
            'joomla_admin': 'site:{domain} inurl:/administrator',
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
    
    def search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo (More reliable for automation)"""
        results = []
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                ddgs_gen = ddgs.text(query, max_results=num_results)
                for r in ddgs_gen:
                    results.append({
                        'title': r.get('title', 'No Title'),
                        'url': r.get('href', ''),
                        'description': r.get('body', ''),
                        'source': 'DuckDuckGo'
                    })
        except Exception as e:
            self.add_warning(f"DuckDuckGo search failed: {e}")
        return results

    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Google - with fallback strategy"""
        results = []
        
        try:
            # Try googlesearch library first
            try:
                from googlesearch import search
                for url in search(query, num_results=num_results, sleep_interval=2):
                    results.append({
                        'title': url,
                        'url': url,
                        'source': 'Google (googlesearch)'
                    })
                    if len(results) >= num_results:
                        break
                if results:
                    return results
            except ImportError:
                pass
            except Exception as e:
                logger.debug(f"googlesearch failed: {e}")
            
            # Fallback: Try requests with headers
            url = "https://www.google.com/search"
            params = {'q': query, 'num': num_results}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                for g in soup.find_all('div', class_='g'):
                    try:
                        title_element = g.find('h3')
                        link_element = g.find('a', href=True)
                        if title_element and link_element:
                            link = link_element['href']
                            if '/url?q=' in link:
                                link = link.split('/url?q=')[1].split('&')[0]
                            results.append({
                                'title': title_element.text,
                                'url': link,
                                'source': 'Google (requests)'
                            })
                    except:
                        pass
            else:
                self.add_warning(f"Google rate limited (Status {response.status_code}). Try DuckDuckGo engine.")
        
        except Exception as e:
            self.add_error(f"Google search error: {e}")
        
        return results
    
    def run(self, query: str = None, domain: str = None, dork_type: str = "none", engine: str = "duckduckgo", num_results: int = 10, **kwargs):
        """Perform search engine dorking"""
        self.set_core_params(**kwargs)
        if not self.validate_input(query, domain, **kwargs):
            return self.get_results()
        
        self.is_running = True
        self.clear_results()
        self.audit_log(f"Starting Search Engine Dorking: Engine={engine}, Domain={domain}, Type={dork_type}")
        
        try:
            # Build query
            if domain and dork_type != "none":
                search_query = self.build_dork_query(domain, dork_type)
            elif domain:
                search_query = f"site:{domain}"
            else:
                search_query = query
            
            self.add_result(f"[*] Melakukan pencarian ({engine}): {search_query}")
            
            if engine.lower() == "google":
                results = self.search_google(search_query, num_results)
            else:
                results = self.search_duckduckgo(search_query, num_results)
            
            if not results:
                self.add_result("[-] Tidak ada hasil yang ditemukan.")
            else:
                for res in results:
                    self.add_result(f"[+] {res['title']}")
                    self.add_result(f"    URL: {res['url']}")
                    if res.get('description'):
                        self.add_result(f"    Desc: {res['description'][:100]}...")
            
            return self.get_results()
            
        except Exception as e:
            self.add_error(f"Search dorking failed: {e}")
            return self.get_results()
        finally:
            self.is_running = False
