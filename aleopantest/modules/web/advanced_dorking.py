"""Advanced Search Engine Dorking Tool"""
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger


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
            version="3.3.0",
            author="Aleocrophic Team",
            description="Multi-engine search dorking with templates and custom queries for advanced reconnaissance.",
            usage="aleopantest run advanced-dorking --engine google --domain target.com --template exposed_configs",
            requirements=['requests', 'beautifulsoup4', 'duckduckgo-search'],
            tags=['dorking', 'osint', 'reconnaissance', 'google-dork'],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "engine",
                    "label": "Search Engine",
                    "type": "select",
                    "options": ["google", "bing", "duckduckgo", "github", "shodan"],
                    "default": "google"
                },
                {
                    "name": "domain",
                    "label": "Target Domain",
                    "type": "text",
                    "placeholder": "e.g. example.com",
                    "required": False
                },
                {
                    "name": "template",
                    "label": "Dork Template",
                    "type": "select",
                    "options": ["none", "exposed_configs", "admin_panels", "backup_files", "source_code", "user_data", "ssl_certs", "logs"],
                    "default": "none"
                },
                {
                    "name": "query",
                    "label": "Custom Dork Query",
                    "type": "textarea",
                    "placeholder": "Enter custom dork query...",
                    "required": False
                },
                {
                    "name": "api_key",
                    "label": "API Key (Optional)",
                    "type": "text",
                    "placeholder": "Shodan/GitHub API Key",
                    "required": False
                },
                {
                    "name": "num_results",
                    "label": "Number of Results",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 100
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)

    def run(self, engine: str = "google", domain: str = None, template: str = "none", 
            query: str = None, api_key: str = None, num_results: int = 10, **kwargs):
        if not domain and not query:
            self.add_error("Either domain or query is required")
            return self.get_results()

        self.audit_log(f"Starting Advanced Dorking: Engine={engine}, Domain={domain}, Template={template}")
        self.add_result(f"[*] Memulai dorking menggunakan engine: {engine.upper()}")

        queries = []
        if query:
            queries.append(query)
        elif domain and template != "none":
            queries = self.build_dork_queries(domain, template)
        elif domain:
            queries.append(f"site:{domain}")

        for q in queries:
            self.add_result(f"[*] Menjalankan query: {q}")
            results = []
            if engine == "google":
                results = self.search_google(q, num_results)
            elif engine == "duckduckgo":
                results = self.search_duckduckgo(q, num_results)
            elif engine == "github":
                results = self.search_github(q)
            elif engine == "shodan":
                results = self.search_shodan(q, api_key)
            
            if results:
                for res in results:
                    self.add_result(f"[+] Found: {res.get('url') or res.get('name')}")
                    if res.get('title'): self.add_result(f"    Title: {res.get('title')}")
            else:
                self.add_result("[-] Tidak ada hasil yang ditemukan untuk query ini.")

        return self.get_results()

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
                'User-Agent': 'Aleopantest'
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

    def run(self, engine: str = "google", domain: str = "", template: str = "", query: str = "", **kwargs):
        """Execute dorking search"""
        self.set_core_params(**kwargs)
        self.clear_results()
        
        if not self.validate_input(engine=engine, domain=domain, template=template, query=query, **kwargs):
            return self.get_results()
        
        try:
            num_results = int(kwargs.get('num_results', 10))
            all_results = []
            queries_to_run = []
            
            # Build queries
            if template and domain:
                queries_to_run = self.build_dork_queries(domain, template)
                self.log(f"Built {len(queries_to_run)} dork queries from template")
            elif query:
                queries_to_run = [query]
                self.log(f"Using custom query")
            elif domain:
                # Default queries
                queries_to_run = [f"site:{domain}"]
            
            # Execute searches
            for q in queries_to_run:
                self.log(f"Searching with {engine}: {q}")
                
                results = []
                if engine == 'google':
                    results = self.search_google(q, num_results)
                elif engine == 'duckduckgo':
                    results = self.search_duckduckgo(q, num_results)
                elif engine == 'github':
                    results = self.search_github(q)
                elif engine == 'shodan':
                    api_key = kwargs.get('shodan_api_key') or kwargs.get('api_key')
                    results = self.search_shodan(q, api_key)
                
                all_results.extend(results)
                time.sleep(1)  # Rate limiting between queries
            
            for res in all_results:
                self.add_result(res)

            return self.get_results()
        except Exception as e:
            self.add_error(f"Dorking failed: {str(e)}")
            return self.get_results()

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Legacy execute method for backward compatibility"""
        return self.run(**kwargs)
