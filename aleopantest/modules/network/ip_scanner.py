"""
IP Scanner Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class IPScanner(BaseTool):
    """IP address scanner untuk subnet scanning"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="IP Scanner",
            category=ToolCategory.NETWORK,
            version="3.0.0",
            author="Aleocrophic Team",
            description="IP scanner untuk scanning subnet dan deteksi host yang aktif",
            usage="scanner = IPScanner(); scanner.run(network='192.168.1.0/24')",
            requirements=["socket", "ipaddress"],
            tags=["network", "scanner", "subnet", "host-discovery"]
        )
        super().__init__(metadata)
    
    def validate_input(self, network: str, **kwargs) -> bool:
        """Validate input"""
        if not network:
            self.add_error("Network tidak boleh kosong")
            return False
        try:
            ipaddress.ip_network(network, strict=False)
            return True
        except ValueError:
            self.add_error(f"Invalid network: {network}")
            return False
    
    def check_host(self, ip: str, timeout: int = 2) -> Dict[str, Any]:
        """Check if host is alive"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((str(ip), 445))  # SMB port
            sock.close()
            
            if result == 0:
                # Try to resolve hostname
                try:
                    hostname = socket.gethostbyaddr(str(ip))[0]
                except:
                    hostname = None
                
                return {
                    'ip': str(ip),
                    'alive': True,
                    'hostname': hostname
                }
            else:
                return {
                    'ip': str(ip),
                    'alive': False,
                    'hostname': None
                }
        except Exception:
            return {
                'ip': str(ip),
                'alive': False,
                'hostname': None
            }
    
    def run(self, network: str, timeout: int = 2, threads: int = 50, **kwargs):
        """Scan network"""
        if not self.validate_input(network, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            net = ipaddress.ip_network(network, strict=False)
            logger.info(f"Scanning network {network} ({net.num_addresses} addresses)")
            
            alive_hosts = []
            total_scanned = 0
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {
                    executor.submit(self.check_host, ip, timeout): ip
                    for ip in net.hosts()
                }
                
                for future in as_completed(futures):
                    result = future.result()
                    total_scanned += 1
                    
                    if result['alive']:
                        alive_hosts.append(result)
                        self.add_result(result)
                        logger.info(f"[+] Host found: {result['ip']} ({result['hostname'] or 'N/A'})")
            
            summary = {
                'network': network,
                'total_addresses': net.num_addresses,
                'scanned': total_scanned,
                'alive_hosts': len(alive_hosts),
                'hosts': alive_hosts
            }
            
            logger.info(f"Scan completed: {len(alive_hosts)} hosts found")
            return summary
            
        except Exception as e:
            self.add_error(f"Network scan failed: {e}")
        finally:
            self.is_running = False
            return self.get_results()