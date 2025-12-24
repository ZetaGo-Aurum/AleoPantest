"""Packet Sniffer Tool"""
import socket
import struct
import textwrap
from typing import Optional, Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class PacketSniffer(BaseTool):
    """Network packet sniffer untuk analisis network traffic"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Packet Sniffer",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AloPantest",
            description="Packet sniffer untuk capture dan analisis network traffic secara real-time",
            usage="sniffer = PacketSniffer(); sniffer.run(interface='eth0', packet_count=10)",
            requirements=["socket", "struct"],
            tags=["network", "sniffer", "traffic", "analysis", "packet"]
        )
        super().__init__(metadata)
        self.packet_count = 0
    
    def validate_input(self, interface: Optional[str] = None, packet_count: int = 10, **kwargs) -> bool:
        """Validate input"""
        if packet_count < 1:
            self.add_error("Packet count must be >= 1")
            return False
        return True
    
    def format_ipv4(self, bytes_addr):
        """Format IPv4 address"""
        bytes_str = map(str, bytes_addr)
        return '.'.join(bytes_str)
    
    def format_multi_byte_field(self, bytes_field):
        """Format multi-byte field"""
        bytes_str = map('{:02x}'.format, bytes_field)
        bytes_str = ' '.join(bytes_str)
        return bytes_str
    
    def format_ipv4_packet(self, data):
        """Format IPv4 packet info"""
        version_packet_length = data[0]
        version = version_packet_length >> 4
        packet_length = (version_packet_length & 15) * 4
        ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
        
        return version, packet_length, ttl, proto, self.format_ipv4(src), self.format_ipv4(target)
    
    def format_icmp_packet(self, data):
        """Format ICMP packet"""
        icmp_type, code, checksum = struct.unpack('! B B 2x', data[:4])
        return icmp_type, code, checksum
    
    def format_tcp_segment(self, data):
        """Format TCP segment"""
        (src_port, dest_port, sequence, acknowledgment, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        flag_urg = (offset_reserved_flags & 32) >> 5
        flag_ack = (offset_reserved_flags & 16) >> 4
        flag_psh = (offset_reserved_flags & 8) >> 3
        flag_rst = (offset_reserved_flags & 4) >> 2
        flag_syn = (offset_reserved_flags & 2) >> 1
        flag_fin = offset_reserved_flags & 1
        
        return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin
    
    def run(self, interface: Optional[str] = None, packet_count: int = 10, **kwargs):
        """Start packet sniffing"""
        if not self.validate_input(interface, packet_count, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            # Create raw socket
            if interface:
                conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            else:
                conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                conn.bind((socket.gethostbyname(socket.gethostname()), 0))
                conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            
            logger.info(f"Starting packet sniffer - capturing {packet_count} packets")
            
            for i in range(packet_count):
                if not self.is_running:
                    break
                
                try:
                    raw_buffer = conn.recv(65536)
                    
                    if interface:
                        dest_mac, src_mac, eth_proto, data = self.format_ethernet_frame(raw_buffer)
                        packet_info = {
                            'frame': i + 1,
                            'dest_mac': dest_mac,
                            'src_mac': src_mac,
                            'proto': eth_proto
                        }
                    else:
                        # IPv4
                        version, packet_length, ttl, proto, src, target = self.format_ipv4_packet(raw_buffer)
                        packet_info = {
                            'frame': i + 1,
                            'version': version,
                            'packet_length': packet_length,
                            'ttl': ttl,
                            'protocol': proto,
                            'src': src,
                            'target': target
                        }
                    
                    self.add_result(packet_info)
                    logger.debug(f"Packet {i+1}: {packet_info}")
                
                except KeyboardInterrupt:
                    logger.info("Sniffer stopped by user")
                    break
            
            if interface:
                conn.close()
            else:
                conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
            logger.info(f"Captured {len(self.results)} packets")
            return self.results
            
        except Exception as e:
            self.add_error(f"Sniffing failed: {e}")
        finally:
            self.is_running = False
    
    def format_ethernet_frame(self, data):
        """Format ethernet frame"""
        dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
        return self.format_multi_byte_field(dest_mac), self.format_multi_byte_field(src_mac), proto
    
    def stop(self):
        """Stop sniffing"""
        self.is_running = False
        logger.info("Packet sniffer stopped")
