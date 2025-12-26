"""Traceroute Tool"""
import subprocess
import platform
import re
from typing import Dict, Any, List

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class TraceRoute(BaseTool):
    """Traceroute tool untuk melacak jalur paket ke tujuan"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Traceroute",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AleoPantest",
            description="Traceroute untuk melacak jalur paket melalui berbagai hop ke host tujuan",
            usage="trace = TraceRoute(); trace.run(host='8.8.8.8', max_hops=30)",
            requirements=["subprocess", "platform"],
            tags=["network", "traceroute", "routing", "path-analysis"]
        )
        super().__init__(metadata)
    
    def validate_input(self, host: str, max_hops: int = 30, **kwargs) -> bool:
        """Validate input"""
        if not host:
            self.add_error("Host tidak boleh kosong")
            return False
        if max_hops < 1 or max_hops > 255:
            self.add_error("Max hops harus antara 1-255")
            return False
        return True
    
    def run(self, host: str, max_hops: int = 30, timeout: int = 30, **kwargs):
        """Execute traceroute"""
        if not self.validate_input(host, max_hops, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                cmd = ['tracert', '-h', str(max_hops), '-w', str(timeout * 1000), host]
            else:  # Linux/Mac
                cmd = ['traceroute', '-m', str(max_hops), '-w', str(timeout), host]
            
            logger.info(f"Tracing route to {host} (max {max_hops} hops)...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
            
            output = result.stdout
            hops = []
            
            # Parse output
            lines = output.split('\n')
            
            for line in lines:
                if not line.strip():
                    continue
                
                hop_info = {}
                
                if system == 'windows':
                    # Windows tracert format
                    match = re.match(r'\s*(\d+)\s+(<1|[\d]+)\s+ms.*\[([\d.]+)\]', line)
                    if match:
                        hop_info['hop'] = int(match.group(1))
                        hop_info['time_ms'] = match.group(2)
                        hop_info['ip'] = match.group(3)
                        hops.append(hop_info)
                else:
                    # Linux/Mac traceroute format
                    match = re.match(r'\s*(\d+)\s+([\w.-]+)\s+\(([\d.]+)\)\s+(.*)', line)
                    if match:
                        hop_info['hop'] = int(match.group(1))
                        hop_info['hostname'] = match.group(2)
                        hop_info['ip'] = match.group(3)
                        
                        # Parse latencies
                        latencies = re.findall(r'([\d.]+)\s*ms', match.group(4))
                        if latencies:
                            hop_info['times_ms'] = [float(x) for x in latencies]
                        
                        hops.append(hop_info)
            
            result_data = {
                'target': host,
                'max_hops': max_hops,
                'hops_count': len(hops),
                'hops': hops,
                'raw_output': output
            }
            
            self.add_result(result_data)
            logger.info(f"Traceroute completed: {len(hops)} hops")
            return result_data
            
        except subprocess.TimeoutExpired:
            self.add_error(f"Traceroute timeout for {host}")
        except Exception as e:
            self.add_error(f"Traceroute failed: {e}")
        finally:
            self.is_running = False
