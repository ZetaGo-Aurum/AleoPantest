"""Port Scanner Tool"""
import socket
import threading
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger
from ...core.config import config


class PortScanner(BaseTool):
    """Advanced port scanner with multi-threading"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Port Scanner",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AloPantest",
            description="Fast port scanner dengan multi-threading untuk deteksi service yang berjalan",
            usage="scanner = PortScanner(); scanner.run(host='192.168.1.1', ports='1-65535')",
            requirements=["socket", "threading"],
            tags=["network", "scanner", "port", "reconnaissance"]
        )
        super().__init__(metadata)
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            3306: "MySQL", 5432: "PostgreSQL", 5984: "CouchDB", 6379: "Redis",
            8000: "HTTP-Alt", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 9200: "Elasticsearch",
            27017: "MongoDB", 50070: "Hadoop", 3389: "RDP"
        }
    
    def validate_input(self, host: str, ports: str = "1-1024", **kwargs) -> bool:
        """Validate input"""
        if not host:
            self.add_error("Host tidak boleh kosong")
            return False
        return True
    
    def parse_ports(self, port_spec: str) -> List[int]:
        """Parse port specification"""
        ports = []
        try:
            for part in port_spec.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    ports.extend(range(start, end + 1))
                else:
                    ports.append(int(part))
            return sorted(list(set(ports)))
        except Exception as e:
            self.add_error(f"Invalid port specification: {e}")
            return []
    
    def check_port(self, host: str, port: int, timeout: int = 3) -> Tuple[int, bool, str]:
        """Check single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            service = self.common_ports.get(port, "Unknown")
            is_open = result == 0
            
            return port, is_open, service
        except Exception as e:
            logger.debug(f"Error scanning port {port}: {e}")
            return port, False, "Unknown"
    
    def run(self, host: str, ports: str = "1-1024", timeout: int = 3, threads: int = 50, **kwargs):
        """Scan ports"""
        if not self.validate_input(host, ports, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            port_list = self.parse_ports(ports)
            if not port_list:
                return
            
            logger.info(f"Scanning {host} on {len(port_list)} ports dengan {threads} threads")
            
            open_ports = []
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [
                    executor.submit(self.check_port, host, port, timeout)
                    for port in port_list
                ]
                
                for future in as_completed(futures):
                    port, is_open, service = future.result()
                    if is_open:
                        result = {
                            'port': port,
                            'state': 'open',
                            'service': service
                        }
                        open_ports.append(result)
                        self.add_result(result)
                        logger.info(f"[+] Port {port}/{service} is OPEN")
            
            elapsed = time.time() - start_time
            summary = {
                'host': host,
                'total_ports_scanned': len(port_list),
                'open_ports': len(open_ports),
                'elapsed_time': round(elapsed, 2),
                'ports': open_ports
            }
            
            logger.info(f"Scan completed in {elapsed:.2f}s - Found {len(open_ports)} open ports")
            return summary
            
        except Exception as e:
            self.add_error(f"Scan failed: {e}")
        finally:
            self.is_running = False
