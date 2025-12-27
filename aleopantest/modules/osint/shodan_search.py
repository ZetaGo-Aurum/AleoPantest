try:
    import shodan
    HAS_SHODAN = True
except ImportError:
    HAS_SHODAN = False

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class ShodanSearch(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Shodan Search",
            category=ToolCategory.OSINT,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Melakukan pencarian pada Shodan menggunakan API Key.",
            usage="aleopantest run shodan-search --query <query> --api_key <key>",
            example="aleopantest run shodan-search --query 'apache' --api_key 'YOUR_API_KEY'",
            parameters={"query": "Shodan search query", "api_key": "Shodan API Key"},
            requirements=["shodan"],
            tags=["osint", "shodan", "recon"],
            risk_level="LOW",
            form_schema=[
                {
                    "name": "query",
                    "label": "Search Query",
                    "type": "text",
                    "placeholder": "e.g. apache, product:nginx, port:22",
                    "required": True
                },
                {
                    "name": "api_key",
                    "label": "Shodan API Key",
                    "type": "password",
                    "placeholder": "Enter your Shodan API Key",
                    "required": True
                },
                {
                    "name": "limit",
                    "label": "Results Limit",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 100
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)

    def run(self, query: str = "", api_key: str = "", limit: int = 10, **kwargs):
        self.set_core_params(**kwargs)
        self.clear_results()
        
        if not HAS_SHODAN:
            self.add_error("Library 'shodan' tidak terinstal. Silakan jalankan: pip install shodan")
            return self.get_results()
            
        if not api_key:
            self.add_error("Shodan API Key is required")
            return self.get_results()
        if not query:
            self.add_error("Search query is required")
            return self.get_results()

        self.log(f"Searching Shodan for: {query}")
        
        try:
            api = shodan.Shodan(api_key)
            results = api.search(query, limit=int(limit))
            
            self.add_result({
                "total": results['total'],
                "matches_count": len(results['matches'])
            })
            
            for result in results['matches']:
                self.add_result({
                    "ip": result['ip_str'],
                    "port": result['port'],
                    "org": result.get('org', 'Unknown'),
                    "hostnames": result.get('hostnames', []),
                    "location": f"{result.get('location', {}).get('city', 'Unknown')}, {result.get('location', {}).get('country_name', 'Unknown')}"
                })
                
            return self.get_results()
        except shodan.APIError as e:
            self.add_error(f"Shodan API Error: {str(e)}")
            return self.get_results()
        except Exception as e:
            self.add_error(f"Search failed: {str(e)}")
            return self.get_results()

    def validate_input(self, query: str = "", api_key: str = "", **kwargs) -> bool:
        return bool(query.strip()) and bool(api_key.strip())
