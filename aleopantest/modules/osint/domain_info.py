"""
Domain Information Gatherer

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import requests
from typing import Dict, Any
import socket

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class DomainInfo(BaseTool):
    """Domain information gatherer untuk kumpulkan informasi tentang domain"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Domain Information Gatherer",
            category=ToolCategory.OSINT,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Gather informasi komprehensif tentang domain termasuk DNS, IP, dan metadata",
            usage="info = DomainInfo(); info.run(domain='target.com')",
            requirements=["requests", "socket"],
            tags=["osint", "domain", "information-gathering", "reconnaissance"],
            form_schema=[
                {
                    "name": "target",
                    "type": "text",
                    "label": "Target Domain / URL",
                    "placeholder": "e.g. example.com",
                    "required": True
                },
                {
                    "name": "domain",
                    "type": "text",
                    "label": "Manual Domain (Optional)",
                    "placeholder": "Override target domain here if needed",
                    "required": False,
                    "description": "Biarkan kosong untuk menggunakan target di atas"
                },
                {
                    "name": "timeout",
                    "type": "number",
                    "label": "Timeout (seconds)",
                    "default": 10,
                    "required": False
                }
            ]
        )
        super().__init__(metadata)
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input with auto-detection of domain from target or manual input"""
        # Auto-detect domain from kwargs (domain or target)
        domain = kwargs.get('domain') or kwargs.get('target')
        
        if not domain:
            self.add_error("Parameter 'domain' atau 'target' tidak ditemukan. Silakan masukkan domain secara manual.")
            return False
            
        # Standardize domain (remove protocol if present)
        if "://" in domain:
            domain = domain.split("://")[-1].split("/")[0]
        
        # Save to instance variable for run() to use
        self.target_domain = domain
        return True
    
    def get_dns_records(self, domain: str) -> Dict[str, Any]:
        """Get DNS records"""
        dns_info = {}
        try:
            import dns.resolver
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
            
            for rtype in record_types:
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    dns_info[rtype] = [str(rdata) for rdata in answers]
                except:
                    pass
        except ImportError:
            logger.warning("dnspython not available, DNS lookup skipped")
        
        return dns_info
    
    def get_ip_info(self, domain: str) -> Dict[str, Any]:
        """Get IP information"""
        ip_info = {}
        try:
            # Get primary IP
            ip = socket.gethostbyname(domain)
            ip_info['primary_ip'] = ip
            
            # Get all IPs
            try:
                _, _, ips = socket.gethostbyname_ex(domain)
                ip_info['all_ips'] = ips
            except:
                pass
        except socket.gaierror as e:
            logger.error(f"Cannot resolve domain: {e}")
        
        return ip_info
    
    def check_http_headers(self, domain: str) -> Dict[str, Any]:
        """Check HTTP headers"""
        header_info = {}
        
        for scheme in ['https', 'http']:
            try:
                url = f"{scheme}://{domain}"
                response = requests.head(url, timeout=5, allow_redirects=True)
                
                header_info[f'{scheme}_status'] = response.status_code
                header_info[f'{scheme}_headers'] = dict(response.headers)
                
                # Extract useful info
                if 'Server' in response.headers:
                    header_info['server'] = response.headers['Server']
                if 'X-Powered-By' in response.headers:
                    header_info['powered_by'] = response.headers['X-Powered-By']
                
                break
            except:
                pass
        
        return header_info
    
    def run(self, **kwargs):
        """Gather domain information"""
        if not self.validate_input(**kwargs):
            return
        
        # Use domain from instance variable (populated by validate_input)
        domain = getattr(self, 'target_domain', kwargs.get('domain'))
        timeout = kwargs.get('timeout', 10)
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Gathering information for domain: {domain}")
            
            result = {
                'domain': domain,
                'dns_records': self.get_dns_records(domain),
                'ip_info': self.get_ip_info(domain),
                'http_info': self.check_http_headers(domain),
            }
            
            self.add_result(result)
            logger.info(f"Domain information gathering completed")
            return self.get_results()
            
        except Exception as e:
            self.add_error(f"Domain information gathering failed: {e}")
        finally:
            self.is_running = False
