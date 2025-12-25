"""Advanced Search Engine Dorking Tool"""
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class AdvancedDorking(BaseTool):
    """Advanced Search Engine Dorking - Multiple engines and custom queries"""
    
    SEARCH_ENGINES = {
        'google': {
            'url': 'https://www.google.com/search',
            'param': 'q',
            'operators': ['site:', 'inurl:', 'intitle:', 'intext:', 'filetype:', 'cache:', 'related:']
        },
        'bing': {
            'url': 'https://www.bing.com/search',
            'param': 'q',
            'operators': ['site:', 'url:', 'title:', 'contains:', 'filetype:']
        },
        'duckduckgo': {
            'url': 'https://duckduckgo.com/',
            'param': 'q',
            'operators': ['site:', 'inurl:', 'intitle:']
        },
        'github': {
            'url': 'https://github.com/search',
            'param': 'q',
            'operators': ['repo:', 'user:', 'language:', 'stars:', 'filename:']
        },
        'shodan': {
            'url': 'https://www.shodan.io/search',
            'param': 'query',
            'operators': ['port:', 'country:', 'city:', 'os:', 'product:', 'http.title:']
        }
    }
    
    DORK_TEMPLATES = {
        'exposed_configs': [
            'site:{domain} filetype:conf OR filetype:config OR filetype:yaml OR filetype:yml',
            'site:{domain} "api_key" OR "API_KEY" OR "password" OR "secret"',
            'site:{domain} ".env" OR ".htaccess" OR "web.config"'
        ],
        'admin_panels': [
            'site:{domain} inurl:/admin OR inurl:/administrator OR inurl:/wp-admin',
            'site:{domain} intitle:"admin" OR intitle:"control panel"',
            'site:{domain} inurl:/dashboard OR inurl:/management'
        ],
        'backup_files': [
            'site:{domain} filetype:sql OR filetype:bak OR filetype:backup',
            'site:{domain} "backup" OR ".sql" OR ".tar.gz" OR ".zip"',
            'site:{domain} inurl:backup OR inurl:backups OR inurl:downloads'
        ],
        'source_code': [
            'site:{domain} filetype:php OR filetype:py OR filetype:java',
            'site:{domain} ".git" OR ".gitconfig" OR "package.json"',
            'site:{domain} "source" OR "src" inurl:download'
        ],
        'user_data': [
            'site:{domain} filetype:pdf OR filetype:docx OR filetype:xlsx',
            'site:{domain} "user" OR "email" OR "phone" inurl:export',
            'site:{domain} filetype:csv intext:password'
        ],
        'ssl_certs': [
            'site:{domain} ".crt" OR ".pem" OR ".key"',
            'site:{domain} "certificate" OR "ssl" filetype:txt',
        ],
        'logs': [
            'site:{domain} filetype:log',
            'site:{domain} "error" OR "debug" OR "warning" filetype:txt',
        ]
    }
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Advanced Search Engine Dorking",
            category=ToolCategory.OSINT,
            version="2.0.0",
            author="AloPantest Team",
            description="Multi-engine search dorking with templates and custom queries",
            usage="aleopantest run advanced-dorking --engine google --domain target.com --template exposed_configs",
            requirements=['requests', 'beautifulsoup4', 'duckduckgo-search'],
            tags=['dorking', 'osint', 'reconnaissance', 'google-dork'],
            risk_level="MEDIUM"
        )
        super().__init__(metadata)
    
    def validate_input(self, engine: str = None, domain: str = None, template: str = None, 
                      query: str = None, **kwargs) -> bool:
        """Validate input parameters"""
        if not domain and not query:
            self.add_error("Either domain or query is required")
            return False
        
        engine = engine or 'google'
        if engine not in self.SEARCH_ENGINES:
            self.add_error(f"Invalid engine. Available: {list(self.SEARCH_ENGINES.keys())}")
            return False
        
        if template and template not in self.DORK_TEMPLATES:
            self.add_error(f"Invalid template. Available: {list(self.DORK_TEMPLATES.keys())}")
            return False
        
        return True
    
    def build_dork_queries(self, domain: str, template: str) -> List[str]:
        """Build dork queries from templates"""
        queries = []
        if template in self.DORK_TEMPLATES:
            for q in self.DORK_TEMPLATES[template]:
                queries.append(q.replace('{domain}', domain))
        return queries
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search using Google"""
        try:
            from googlesearch import search
            
            results = []
            for url in search(query, num_results=num_results):
                results.append({
                    'engine': 'google',
                    'url': url,
                    'timestamp': datetime.now().isoformat()
                })
                time.sleep(0.5)  # Rate limiting
            
            return results
        except Exception as e:
            self.add_error(f"Google search failed: {str(e)}")
            return []
    
    def search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search using DuckDuckGo"""
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=num_results):
                    results.append({
                        'engine': 'duckduckgo',
                        'url': result.get('href', ''),
                        'title': result.get('title', ''),
                        'body': result.get('body', ''),
                        'timestamp': datetime.now().isoformat()
                    })
            
            return results
        except Exception as e:
            self.add_error(f"DuckDuckGo search failed: {str(e)}")
            return []
    
    def search_github(self, query: str) -> List[Dict]:
        """Search using GitHub API"""
        try:
            import requests
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'AloPantest'
            }
            
            results = []
            url = 'https://api.github.com/search/repositories'
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            for repo in data.get('items', []):
                results.append({
                    'engine': 'github',
                    'name': repo['name'],
                    'url': repo['html_url'],
                    'description': repo['description'],
                    'stars': repo['stargazers_count'],
                    'timestamp': datetime.now().isoformat()
                })
            
            return results
        except Exception as e:
            self.add_error(f"GitHub search failed: {str(e)}")
            return []
    
    def search_shodan(self, query: str, api_key: str = None) -> List[Dict]:
        """Search using Shodan API"""
        try:
            import requests
            
            if not api_key:
                self.add_warning("Shodan API key not provided. Register at https://www.shodan.io/")
                return []
            
            headers = {'X-Shodan-Key': api_key}
            url = 'https://api.shodan.io/shodan/host/search'
            params = {'query': query}
            
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            results = []
            for host in data.get('matches', []):
                results.append({
                    'engine': 'shodan',
                    'ip': host['ip_str'],
                    'port': host['port'],
                    'org': host.get('org', 'N/A'),
                    'os': host.get('os', 'N/A'),
                    'data': host.get('data', ''),
                    'timestamp': datetime.now().isoformat()
                })
            
            return results
        except Exception as e:
            self.add_error(f"Shodan search failed: {str(e)}")
            return []
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute dorking search"""
        if not self.validate_input(**kwargs):
            return self.format_output()
        
        try:
            engine = kwargs.get('engine', 'google')
            domain = kwargs.get('domain', '')
            template = kwargs.get('template', '')
            custom_query = kwargs.get('query', '')
            num_results = kwargs.get('num_results', 10)
            
            all_results = []
            queries_to_run = []
            
            # Build queries
            if template and domain:
                queries_to_run = self.build_dork_queries(domain, template)
                self.add_success(f"Built {len(queries_to_run)} dork queries from template")
            elif custom_query:
                queries_to_run = [custom_query]
                self.add_success(f"Using custom query")
            elif domain:
                # Default queries
                queries_to_run = [f"site:{domain}"]
            
            # Execute searches
            for query in queries_to_run:
                self.add_output("Searching", {"Query": query, "Engine": engine})
                
                if engine == 'google':
                    results = self.search_google(query, num_results)
                elif engine == 'duckduckgo':
                    results = self.search_duckduckgo(query, num_results)
                elif engine == 'github':
                    results = self.search_github(query)
                elif engine == 'shodan':
                    api_key = kwargs.get('shodan_api_key')
                    results = self.search_shodan(query, api_key)
                else:
                    results = self.search_google(query, num_results)
                
                all_results.extend(results)
                time.sleep(1)  # Rate limiting between queries
            
            # Save results
            output_dir = Path('./output/dorking')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = output_dir / f'dork_{engine}_{int(time.time())}.json'
            with open(output_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'engine': engine,
                    'domain': domain,
                    'template': template,
                    'results_count': len(all_results),
                    'results': all_results
                }, f, indent=2)
            
            self.add_output("Search Results", {
                "Engine": engine,
                "Domain": domain,
                "Template": template,
                "Total Results": len(all_results),
                "Saved to": str(output_file),
                "Sample Results": all_results[:3] if all_results else []
            })
            
            self.add_recommendation(
                "Available Engines",
                [
                    "• google - Google search with site: operator",
                    "• duckduckgo - Privacy-focused search",
                    "• github - Source code and repo discovery",
                    "• shodan - IoT and server discovery (requires API key)",
                    "• bing - Microsoft search engine"
                ]
            )
            
            self.add_recommendation(
                "Available Templates",
                [
                    "• exposed_configs - Find configuration files",
                    "• admin_panels - Discover admin interfaces",
                    "• backup_files - Locate backup files",
                    "• source_code - Find source code exposure",
                    "• user_data - Discover user data leaks",
                    "• ssl_certs - Find SSL certificates",
                    "• logs - Discover log files"
                ]
            )
            
            self.success = True
            
        except Exception as e:
            self.add_error(f"Execution failed: {str(e)}")
        
        return self.format_output()
