from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import socket
try:
    from scapy.all import ARP, Ether, srp
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class ArpScanner(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="ARP Scanner",
            category=ToolCategory.NETWORK,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Melakukan ARP scanning untuk menemukan perangkat di jaringan lokal",
            usage="aleopantest run arp-scan --range 192.168.1.0/24",
            example="aleopantest run arp-scan --range 192.168.1.0/24",
            requirements=["scapy"],
            tags=["network", "arp", "recon", "local"],
            form_schema=[
                {
                    "name": "range",
                    "label": "IP Range (CIDR)",
                    "type": "text",
                    "placeholder": "192.168.1.0/24",
                    "required": True
                },
                {
                    "name": "timeout",
                    "label": "Timeout (seconds)",
                    "type": "number",
                    "default": 2
                }
            ]
        )
        super().__init__(metadata)

    def run(self, range: str = "192.168.1.0/24", timeout: int = 2, **kwargs):
        if not HAS_SCAPY:
            self.add_error("Library 'scapy' tidak ditemukan. Silakan jalankan: pip install scapy")
            return self.get_results()

        self.add_result(f"[*] Memulai ARP scan pada range: {range}")
        
        try:
            # Create ARP request packet
            arp = ARP(pdst=range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp

            result = srp(packet, timeout=timeout, verbose=0)[0]

            devices = []
            for sent, received in result:
                device = {
                    "ip": received.psrc,
                    "mac": received.hwsrc
                }
                devices.append(device)
                self.add_result(f"[+] Found: {device['ip']} at {device['mac']}")

            self.add_result(f"\n[*] Scan selesai. Menemukan {len(devices)} perangkat.")
            
        except Exception as e:
            self.add_error(f"Error during ARP scan: {str(e)}")
            if "Permission denied" in str(e):
                self.add_error("Hint: ARP scanning membutuhkan hak akses root/administrator.")

        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        return True
