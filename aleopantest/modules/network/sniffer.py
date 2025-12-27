"""
Packet Sniffer Tool

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
from typing import Optional, Dict, Any, List
import time

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class PacketSniffer(BaseTool):
    """Network packet sniffer untuk analisis network traffic menggunakan Scapy"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Packet Sniffer",
            category=ToolCategory.NETWORK,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Packet sniffer untuk capture dan analisis network traffic secara real-time menggunakan Scapy.",
            usage="aleopantest run sniffer --interface eth0 --count 10",
            requirements=["scapy"],
            tags=["network", "sniffer", "traffic", "analysis", "packet"],
            risk_level="HIGH",
            form_schema=[
                {
                    "name": "interface",
                    "label": "Network Interface",
                    "type": "text",
                    "placeholder": "e.g. eth0, wlan0, or leave empty for default",
                    "required": False
                },
                {
                    "name": "count",
                    "label": "Packet Count",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 1000
                },
                {
                    "name": "filter",
                    "label": "BPF Filter",
                    "type": "text",
                    "placeholder": "e.g. tcp, udp, port 80, host 1.1.1.1",
                    "required": False
                },
                {
                    "name": "timeout",
                    "label": "Timeout (seconds)",
                    "type": "number",
                    "default": 30,
                    "min": 1,
                    "max": 3600
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
    
    def packet_callback(self, packet):
        """Callback function for each captured packet"""
        if packet.haslayer(IP):
            src = packet[IP].src
            dst = packet[IP].dst
            proto = packet[IP].proto
            
            summary = f"[IP] {src} -> {dst} (Proto: {proto})"
            
            if packet.haslayer(TCP):
                summary += f" [TCP] Port: {packet[TCP].sport} -> {packet[TCP].dport}"
            elif packet.haslayer(UDP):
                summary += f" [UDP] Port: {packet[UDP].sport} -> {packet[UDP].dport}"
            elif packet.haslayer(ICMP):
                summary += f" [ICMP] Type: {packet[ICMP].type}"
            
            self.add_result(summary)

    def run(self, interface: Optional[str] = None, count: Any = 10, filter: str = "", timeout: Any = 30, **kwargs):
        """Start packet sniffing"""
        self.start_time = time.time()
        
        # Ensure count and timeout are integers
        try:
            count = int(count)
            timeout = int(timeout)
        except (ValueError, TypeError):
            self.add_error(f"Invalid parameters: count ({count}) and timeout ({timeout}) must be integers.")
            return self.get_results()

        if not HAS_SCAPY:
            self.add_error("Library 'scapy' tidak ditemukan. Silakan jalankan: pip install scapy")
            return self.get_results()

        if not self.check_safety(timeout):
            return self.get_results()

        self.audit_log(f"Starting Packet Sniffer: Interface={interface or 'default'}, Count={count}, Filter={filter}")
        self.add_result(f"[*] Memulai sniffing pada {interface or 'default interface'}...")
        self.add_result(f"[*] Filter: {filter if filter else 'None'}")
        
        try:
            sniff(
                iface=interface if interface else None,
                count=count,
                filter=filter,
                prn=self.packet_callback,
                timeout=timeout,
                store=0
            )
            self.add_result(f"[+] Sniffing selesai. Berhasil menangkap paket.")
        except Exception as e:
            self.add_error(f"Error during sniffing: {str(e)}")
            if "Permission denied" in str(e):
                self.add_error("Memerlukan hak akses ROOT/ADMIN untuk sniffing paket.")
        
        return self.get_results()
