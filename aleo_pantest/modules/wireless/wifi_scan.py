from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import time
try:
    from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sniff
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class WifiScanner(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="WiFi Scanner",
            category=ToolCategory.WIRELESS,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Memindai jaringan WiFi di sekitar untuk mendapatkan SSID, BSSID, Signal, dan Security (Membutuhkan interface monitor mode)",
            usage="Aleocrophic run wifi-scan --iface wlan0mon --duration 10",
            example="Aleocrophic run wifi-scan --iface wlan0mon",
            requirements=["scapy", "monitor-mode interface"],
            tags=["wireless", "wifi", "recon"],
            form_schema=[
                {
                    "name": "iface",
                    "label": "Interface (Monitor Mode)",
                    "type": "text",
                    "default": "wlan0mon",
                    "required": True
                },
                {
                    "name": "duration",
                    "label": "Scan Duration (seconds)",
                    "type": "number",
                    "default": 10,
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, iface: str = "wlan0mon", duration: int = 10, **kwargs):
        self.audit_log(f"Starting WiFi Scan on {iface} for {duration}s")
        
        if not HAS_SCAPY:
            self.add_error("Library 'scapy' tidak ditemukan. Silakan jalankan: pip install scapy")
            return self.get_results()

        networks = {}

        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                if bssid not in networks:
                    ssid = pkt[Dot11Elt].info.decode() if pkt[Dot11Elt].info else "Hidden"
                    try:
                        dbm_signal = pkt.dBm_AntSignal
                    except:
                        dbm_signal = "N/A"
                    
                    stats = pkt[Dot11Beacon].network_stats()
                    crypto = stats.get("crypto")
                    
                    networks[bssid] = {
                        "ssid": ssid,
                        "bssid": bssid,
                        "signal": f"{dbm_signal}dBm",
                        "security": "/".join(crypto) if crypto else "Open"
                    }
                    self.add_result(f"[+] Found: {ssid} ({bssid}) - {dbm_signal}dBm - {networks[bssid]['security']}")

        self.add_result(f"[*] Memulai pemindaian pada {iface} selama {duration} detik...")
        try:
            sniff(iface=iface, prn=packet_handler, timeout=duration, store=False)
            self.add_result(f"[*] Pemindaian selesai. Menemukan {len(networks)} jaringan.")
        except Exception as e:
            self.add_error(f"Error during scan: {str(e)}")
            
        return self.get_results()

    def validate_input(self, **kwargs) -> bool: return True
