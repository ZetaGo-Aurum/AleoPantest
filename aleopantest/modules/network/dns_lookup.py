"""
DNS Lookup Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import socket
from typing import Dict, Any, List

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class DNSLookup(BaseTool):
    """DNS lookup tool untuk resolusi domain ke IP"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="DNS Lookup",
            category=ToolCategory.NETWORK,
            version="3.0.0",
            author="Aleocrophic Team",
            description="DNS lookup untuk mendapatkan IP address dari domain name",
            usage="dns = DNSLookup(); dns.run(domain='google.com')",
            requirements=["socket"],
            tags=["network", "dns", "domain", "lookup"],
            form_schema=[
                {
                    "name": "target",
                    "type": "text",
                    "label": "Target Domain",
                    "placeholder": "e.g. google.com",
                    "required": True
                },
                {
                    "name": "domain",
                    "type": "text",
                    "label": "Manual Domain (Optional)",
                    "placeholder": "Override domain here",
                    "required": False
                }
            ]
        )
        super().__init__(metadata)
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input with auto-detection"""
        domain = kwargs.get('domain') or kwargs.get('target')
        if not domain:
            # If we have IP, validation can still pass for reverse lookup
            if kwargs.get('ip'):
                return True
            self.add_error("Domain tidak boleh kosong. Silakan masukkan secara manual.")
            return False
        
        # Standardize
        if "://" in domain:
            domain = domain.split("://")[-1].split("/")[0]
            
        self.target_domain = domain
        return True
    
    def lookup_a(self, domain: str) -> List[str]:
        """Lookup A record"""
        try:
            ips = socket.gethostbyname_ex(domain)
            return ips[2]
        except socket.gaierror as e:
            self.add_error(f"A record lookup failed: {e}")
            return []
    
    def lookup_mx(self, domain: str) -> List[Dict[str, Any]]:
        """Lookup MX records"""
        try:
            import dns.resolver
            mx_records = []
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for mx in answers:
                    mx_records.append({
                        'exchange': str(mx.exchange).rstrip('.'),
                        'preference': mx.preference
                    })
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                logger.info(f"No MX records found for {domain}")
            except Exception as e:
                logger.error(f"MX lookup error for {domain}: {e}")
                self.add_error(f"MX lookup error: {e}")
                
            return sorted(mx_records, key=lambda x: x['preference'])
        except ImportError:
            logger.warning("MX lookup requires dnspython library")
            self.add_warning("MX lookup requires dnspython library. Install with 'pip install dnspython'")
            return []

    def lookup_txt(self, domain: str) -> List[str]:
        """Lookup TXT records"""
        try:
            import dns.resolver
            txt_records = []
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for txt in answers:
                    # TXT records can be multi-part
                    txt_records.append("".join([t.decode() if isinstance(t, bytes) else str(t) for t in txt.strings]))
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                logger.info(f"No TXT records found for {domain}")
            except Exception as e:
                logger.error(f"TXT lookup error for {domain}: {e}")
                self.add_error(f"TXT lookup error: {e}")
                
            return txt_records
        except ImportError:
            logger.warning("TXT lookup requires dnspython library")
            self.add_warning("TXT lookup requires dnspython library")
            return []

    def lookup_ns(self, domain: str) -> List[str]:
        """Lookup NS records"""
        try:
            import dns.resolver
            ns_records = []
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                for ns in answers:
                    ns_records.append(str(ns).rstrip('.'))
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                logger.info(f"No NS records found for {domain}")
            except Exception as e:
                logger.error(f"NS lookup error for {domain}: {e}")
                self.add_error(f"NS lookup error: {e}")
                
            return ns_records
        except ImportError:
            logger.warning("NS lookup requires dnspython library")
            self.add_warning("NS lookup requires dnspython library")
            return []
    
    def reverse_lookup(self, ip: str) -> str:
        """Reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)
            return hostname[0]
        except socket.herror as e:
            self.add_error(f"Reverse lookup failed: {e}")
            return None
    
    def run(self, **kwargs):
        """Execute DNS lookup"""
        if not self.validate_input(**kwargs):
            return
            
        domain = getattr(self, 'target_domain', kwargs.get('domain'))
        ip = kwargs.get('ip')
        lookup_type = kwargs.get('lookup_type', 'all')
        
        if domain:
            self.is_running = True
            self.clear_results()
            
            try:
                logger.info(f"Performing DNS lookup for {domain}")
                
                result = {
                    'domain': domain,
                    'lookup_type': lookup_type
                }
                
                if lookup_type in ['a', 'all']:
                    result['a_records'] = self.lookup_a(domain)
                
                if lookup_type in ['mx', 'all']:
                    result['mx_records'] = self.lookup_mx(domain)
                
                if lookup_type in ['txt', 'all']:
                    result['txt_records'] = self.lookup_txt(domain)
                
                if lookup_type in ['ns', 'all']:
                    result['ns_records'] = self.lookup_ns(domain)
                
                self.add_result(result)
                logger.info(f"DNS lookup completed: {result}")
                return self.get_results()
                
            except Exception as e:
                self.add_error(f"DNS lookup failed: {e}")
            finally:
                self.is_running = False
        
        elif ip:
            self.is_running = True
            self.clear_results()
            
            try:
                logger.info(f"Performing reverse DNS lookup for {ip}")
                
                result = {
                    'ip': ip,
                    'lookup_type': 'reverse'
                }
                
                hostname = self.reverse_lookup(ip)
                result['hostname'] = hostname
                
                self.add_result(result)
                logger.info(f"Reverse DNS lookup completed: {result}")
                return self.get_results()
                
            except Exception as e:
                self.add_error(f"Reverse DNS lookup failed: {e}")
            finally:
                self.is_running = False
        else:
            self.add_error("Domain atau IP harus disediakan")
