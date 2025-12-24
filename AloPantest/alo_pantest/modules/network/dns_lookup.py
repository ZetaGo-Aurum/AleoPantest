"""DNS Lookup Tool"""
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
            version="1.0.0",
            author="AloPantest",
            description="DNS lookup untuk mendapatkan IP address dari domain name",
            usage="dns = DNSLookup(); dns.run(domain='google.com')",
            requirements=["socket"],
            tags=["network", "dns", "domain", "lookup"]
        )
        super().__init__(metadata)
    
    def validate_input(self, domain: str, **kwargs) -> bool:
        """Validate input"""
        if not domain:
            self.add_error("Domain tidak boleh kosong")
            return False
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
            for mx in dns.resolver.resolve(domain, 'MX'):
                mx_records.append({
                    'exchange': str(mx.exchange),
                    'preference': mx.preference
                })
            return sorted(mx_records, key=lambda x: x['preference'])
        except:
            logger.warning("MX lookup requires dnspython library")
            return []
    
    def lookup_txt(self, domain: str) -> List[str]:
        """Lookup TXT records"""
        try:
            import dns.resolver
            txt_records = []
            for txt in dns.resolver.resolve(domain, 'TXT'):
                txt_records.append(str(txt))
            return txt_records
        except:
            logger.warning("TXT lookup requires dnspython library")
            return []
    
    def lookup_ns(self, domain: str) -> List[str]:
        """Lookup NS records"""
        try:
            import dns.resolver
            ns_records = []
            for ns in dns.resolver.resolve(domain, 'NS'):
                ns_records.append(str(ns))
            return ns_records
        except:
            logger.warning("NS lookup requires dnspython library")
            return []
    
    def reverse_lookup(self, ip: str) -> str:
        """Reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip)
            return hostname[0]
        except socket.herror as e:
            self.add_error(f"Reverse lookup failed: {e}")
            return None
    
    def run(self, domain: str = None, ip: str = None, lookup_type: str = 'all', **kwargs):
        """Execute DNS lookup"""
        if domain:
            if not self.validate_input(domain, **kwargs):
                return
            
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
                return result
                
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
                return result
                
            except Exception as e:
                self.add_error(f"Reverse DNS lookup failed: {e}")
            finally:
                self.is_running = False
        else:
            self.add_error("Domain atau IP harus disediakan")
