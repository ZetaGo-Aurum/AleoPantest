"""
WHOIS Lookup Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import socket
import subprocess
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class WhoisLookup(BaseTool):
    """WHOIS lookup tool untuk mendapatkan informasi registrasi domain"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="WHOIS Lookup",
            category=ToolCategory.NETWORK,
            version="3.0.0",
            author="Aleocrophic Team",
            description="WHOIS lookup untuk mendapatkan informasi registrasi domain dan IP ownership",
            usage="whois = WhoisLookup(); whois.run(domain='google.com')",
            requirements=["socket", "subprocess"],
            tags=["network", "whois", "domain-info", "osint"]
        )
        super().__init__(metadata)
    
    def validate_input(self, domain: str = None, ip: str = None, **kwargs) -> bool:
        """Validate input"""
        if not domain and not ip:
            self.add_error("Domain atau IP harus disediakan")
            return False
        return True
    
    def run(self, domain: str = None, ip: str = None, **kwargs):
        """Execute WHOIS lookup"""
        if not self.validate_input(domain, ip, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            query = domain or ip
            logger.info(f"Performing WHOIS lookup for {query}")
            
            # Try using whois command
            try:
                result = subprocess.run(
                    ['whois', query],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout
            except FileNotFoundError:
                # Fallback to Python whois library if available
                try:
                    import whois
                    w = whois.whois(query)
                    output = str(w)
                except ImportError:
                    self.add_error("whois command not found and whois library not installed")
                    return
            
            # Parse output
            result_data = {
                'query': query,
                'type': 'domain' if domain else 'ip',
                'raw_output': output
            }
            
            # Extract key information
            lines = output.split('\n')
            for line in lines:
                if 'Registrar:' in line:
                    result_data['registrar'] = line.split(':', 1)[1].strip()
                elif 'Created Date:' in line or 'Creation Date:' in line:
                    result_data['created'] = line.split(':', 1)[1].strip()
                elif 'Updated Date:' in line or 'Updated:' in line:
                    result_data['updated'] = line.split(':', 1)[1].strip()
                elif 'Expiry Date:' in line or 'Expiration Date:' in line:
                    result_data['expiry'] = line.split(':', 1)[1].strip()
                elif 'Admin Name:' in line or 'Admin:' in line:
                    result_data['admin'] = line.split(':', 1)[1].strip()
                elif 'Name Server:' in line or 'Nameserver:' in line:
                    if 'nameservers' not in result_data:
                        result_data['nameservers'] = []
                    result_data['nameservers'].append(line.split(':', 1)[1].strip())
            
            self.add_result(result_data)
            logger.info(f"WHOIS lookup completed")
            return result_data
            
        except subprocess.TimeoutExpired:
            self.add_error(f"WHOIS lookup timeout for {domain or ip}")
        except Exception as e:
            self.add_error(f"WHOIS lookup failed: {e}")
        finally:
            self.is_running = False
            return self.get_results()