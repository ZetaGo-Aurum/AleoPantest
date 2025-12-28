"""
Subdomain Finder Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import requests
from typing import Dict, List, Any, Set
import socket

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class SubdomainFinder(BaseTool):
    """Subdomain finder untuk enumeration subdomain"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Subdomain Finder",
            category=ToolCategory.WEB,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Subdomain finder dengan brute force dan DNS enumeration",
            usage="finder = SubdomainFinder(); finder.run(domain='target.com')",
            requirements=["requests", "socket"],
            tags=["web", "subdomain", "enumeration", "reconnaissance"],
            form_schema=[
                {
                    "name": "domain",
                    "label": "Domain",
                    "type": "text",
                    "placeholder": "example.com",
                    "required": True
                },
                {
                    "name": "threads",
                    "label": "Threads",
                    "type": "number",
                    "default": 50,
                    "required": False
                }
            ]
        )
        super().__init__(metadata)
        
        # Common subdomain wordlist
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail',
            'smtp', 'pop', 'nameserver', 'vpn', 'admin', 'test',
            'portal', 'proxy', 'ssl', 'cdn', 'api', 'api-v1',
            'api-v2', 'beta', 'dev', 'development', 'staging',
            'production', 'backup', 'db', 'database', 'mail2',
            'ns1', 'ns2', 'cms', 'blog', 'forum', 'shop',
            'panel', 'cpanel', 'whm', 'autodiscover', 'autoconfig',
            'git', 'svn', 'jenkins', 'jira', 'wiki', 'docs',
            'downloads', 'files', 'images', 'upload', 'uploads',
            'shop', 'cart', 'checkout', 'account', 'accounts',
            'secure', 'payment', 'billing', 'invoice', 'support',
            'help', 'contact', 'info', 'about', 'news', 'events',
        ]
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input with auto-detection"""
        domain = kwargs.get('domain') or kwargs.get('target')
        if not domain:
            self.add_error("Domain tidak boleh kosong. Silakan masukkan secara manual.")
            return False
        
        # Standardize domain (remove protocol if present)
        if "://" in domain:
            domain = domain.split("://")[-1].split("/")[0]
        
        self.target_domain = domain
        return True
    
    def check_subdomain(self, subdomain: str, domain: str) -> bool:
        """Check if subdomain resolves"""
        try:
            full_domain = f"{subdomain}.{domain}"
            socket.gethostbyname(full_domain)
            return True
        except socket.gaierror:
            return False
    
    def run(self, **kwargs):
        """Find subdomains"""
        if not self.validate_input(**kwargs):
            return
        
        domain = getattr(self, 'target_domain', kwargs.get('domain'))
        timeout = kwargs.get('timeout', 10)
        threads = kwargs.get('threads', 50)
        
        # Clean domain
        domain = domain.rstrip('/')
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Starting subdomain enumeration for {domain}")
            
            found_subdomains = []
            
            # Brute force subdomains
            for subdomain in self.common_subdomains:
                if not self.is_running:
                    break
                
                if self.check_subdomain(subdomain, domain):
                    full_domain = f"{subdomain}.{domain}"
                    found_subdomains.append(full_domain)
                    
                    # Try to get IP
                    try:
                        ip = socket.gethostbyname(full_domain)
                        result = {'subdomain': full_domain, 'ip': ip}
                        self.add_result(result)
                        logger.info(f"[+] Found: {full_domain} ({ip})")
                    except:
                        result = {'subdomain': full_domain, 'ip': None}
                        self.add_result(result)
                        logger.info(f"[+] Found: {full_domain}")
            
            summary = {
                'domain': domain,
                'total_checked': len(self.common_subdomains),
                'subdomains_found': len(found_subdomains),
                'subdomains': found_subdomains,
                'details': self.results
            }
            
            logger.info(f"Subdomain enumeration completed. Found {len(found_subdomains)} subdomains")
            return summary
            
        except Exception as e:
            self.add_error(f"Subdomain enumeration failed: {e}")
        finally:
            self.is_running = False
            return self.get_results()