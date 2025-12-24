"""Ping Tool"""
import subprocess
import platform
import re
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class PingTool(BaseTool):
    """ICMP Ping tool untuk deteksi host"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Ping Tool",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AloPantest",
            description="Ping tool untuk deteksi apakah host aktif atau tidak",
            usage="ping = PingTool(); ping.run(host='8.8.8.8', count=4)",
            requirements=["subprocess", "platform"],
            tags=["network", "ping", "icmp", "host-detection"]
        )
        super().__init__(metadata)
    
    def validate_input(self, host: str, count: int = 4, **kwargs) -> bool:
        """Validate input"""
        if not host:
            self.add_error("Host tidak boleh kosong")
            return False
        if count < 1:
            self.add_error("Count harus >= 1")
            return False
        return True
    
    def run(self, host: str, count: int = 4, timeout: int = 30, **kwargs):
        """Execute ping"""
        if not self.validate_input(host, count, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                cmd = ['ping', '-n', str(count), '-w', str(timeout * 1000), host]
            else:  # Linux/Mac
                cmd = ['ping', '-c', str(count), '-W', str(timeout), host]
            
            logger.info(f"Pinging {host}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            output = result.stdout
            is_reachable = result.returncode == 0
            
            # Parse output
            lines = output.split('\n')
            stats = {
                'host': host,
                'reachable': is_reachable,
                'raw_output': output,
            }
            
            # Extract statistics
            if system == 'windows':
                for line in lines:
                    if 'packets' in line and 'sent' in line:
                        # Parse Windows ping output
                        match = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)', line)
                        if match:
                            stats['sent'] = int(match.group(1))
                            stats['received'] = int(match.group(2))
                            stats['lost'] = int(match.group(3))
                    
                    if 'Minimum' in line and 'Maximum' in line:
                        match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', line)
                        if match:
                            stats['min_ms'] = int(match.group(1))
                            stats['max_ms'] = int(match.group(2))
                            stats['avg_ms'] = int(match.group(3))
            else:
                for line in lines:
                    if 'packets transmitted' in line:
                        match = re.search(r'(\d+) packets transmitted, (\d+) (?:packets )?received', line)
                        if match:
                            stats['sent'] = int(match.group(1))
                            stats['received'] = int(match.group(2))
                    
                    if 'min/avg/max' in line:
                        match = re.search(r'min/avg/max[/stddev]* = ([\d.]+)/([\d.]+)/([\d.]+)', line)
                        if match:
                            stats['min_ms'] = float(match.group(1))
                            stats['avg_ms'] = float(match.group(2))
                            stats['max_ms'] = float(match.group(3))
            
            self.add_result(stats)
            logger.info(f"Ping result: {stats}")
            return stats
            
        except subprocess.TimeoutExpired:
            self.add_error(f"Ping timeout for {host}")
        except Exception as e:
            self.add_error(f"Ping failed: {e}")
        finally:
            self.is_running = False
