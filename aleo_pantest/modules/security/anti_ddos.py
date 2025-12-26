"""Anti-DDoS Protection Analysis Tool"""
import requests
from typing import Dict, Any, List
from datetime import datetime
import socket

from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleo_pantest.core.logger import logger


class AntiDDoS(BaseTool):
    """Anti-DDoS Detection - Detects and analyzes DDoS protection mechanisms"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Anti-DDoS Detector",
            category=ToolCategory.SECURITY,
            version="2.0.0",
            author="AleoPantest Team",
            description="Detects and analyzes DDoS protection mechanisms like Cloudflare, Akamai, AWS Shield",
            usage="aleopantest run anti-ddos --url https://example.com",
            requirements=['requests'],
            tags=['ddos', 'protection', 'security', 'detection']
        )
        super().__init__(metadata)
        
        # Known DDoS protection providers
        self.ddos_providers = {
            'cloudflare': ['cf-ray', 'cf-cache-status', 'cf-request-id'],
            'akamai': ['akamai-cache-status', 'akamai-x-cache', 'akamai-x-cache-key'],
            'cloudfront': ['x-amz-cf-id', 'x-amz-cf-pop'],
            'aws-shield': ['x-amzn-requestid'],
            'sucuri': ['sucuri-cloudproxy'],
            'incapsula': ['x-iinfo', 'x-cdn'],
            'imperva': ['set-cookie', 'x-iinfo'],
            'modsecurity': ['mod-security-message'],
        }
    
    def validate_input(self, url: str = None, **kwargs) -> bool:
        """Validate input URL"""
        if not url:
            self.add_error("URL is required")
            return False
        
        if not url.startswith(('http://', 'https://')):
            self.add_error("URL must start with http:// or https://")
            return False
        
        return True
    
    def detect_cdnandddos(self, url: str) -> Dict[str, Any]:
        """Detect CDN and DDoS protection providers"""
        result = {
            'url': url,
            'detected_providers': [],
            'headers_analysis': {},
            'confidence_score': 0
        }
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response_headers = {k.lower(): v for k, v in response.headers.items()}
            
            # Check for each DDoS provider
            for provider, indicators in self.ddos_providers.items():
                found_indicators = []
                
                for indicator in indicators:
                    indicator_lower = indicator.lower()
                    if indicator_lower in response_headers:
                        found_indicators.append({
                            'indicator': indicator,
                            'value': response_headers.get(indicator_lower, 'N/A')
                        })
                
                if found_indicators:
                    result['detected_providers'].append({
                        'provider': provider.upper(),
                        'confidence': 'HIGH' if len(found_indicators) >= 2 else 'MEDIUM',
                        'indicators': found_indicators
                    })
            
            # Check for server header fingerprinting
            server_header = response_headers.get('server', '').lower()
            if server_header:
                result['headers_analysis']['server'] = server_header
                
                if 'cloudflare' in server_header:
                    result['detected_providers'].append({
                        'provider': 'CLOUDFLARE',
                        'confidence': 'HIGH',
                        'method': 'Server Header Analysis'
                    })
            
            # Check for suspicious headers
            suspicious_headers = ['x-protected-by', 'x-guarded-by', 'x-scanner-detection']
            for header in suspicious_headers:
                if header in response_headers:
                    result['headers_analysis'][header] = response_headers[header]
            
            # Calculate confidence
            if result['detected_providers']:
                result['confidence_score'] = 0.8
            else:
                result['confidence_score'] = 0.2
            
            result['status'] = 'SUCCESS'
            
        except Exception as e:
            logger.error(f"Error detecting DDoS protection: {e}")
            result['error'] = str(e)
            result['status'] = 'FAILED'
        
        return result
    
    def analyze_ddos_protection(self, url: str) -> Dict[str, Any]:
        """Analyze DDoS protection effectiveness"""
        result = {
            'url': url,
            'protection_levels': {},
            'recommendations': [],
            'risk_assessment': {}
        }
        
        try:
            # Try basic connectivity tests
            from urllib.parse import urlparse
            parsed = urlparse(url)
            host = parsed.netloc
            
            # Check DNS resolution
            dns_result = self._check_dns(host)
            result['dns_check'] = dns_result
            
            # Check response times (indicator of DDoS protection)
            response_times = self._measure_response_times(url)
            result['response_times'] = response_times
            
            # Analyze protection levels
            result['protection_levels']['layer3-4'] = {
                'description': 'Network/Transport layer protection',
                'capabilities': ['IP flooding', 'SYN floods', 'UDP floods'],
                'estimated': 'Likely if CDN detected'
            }
            
            result['protection_levels']['layer7'] = {
                'description': 'Application layer protection',
                'capabilities': ['HTTP floods', 'Slowloris attacks', 'Bot filtering'],
                'estimated': 'Likely if WAF detected'
            }
            
            # Generate recommendations
            result['recommendations'] = self._get_ddos_recommendations(dns_result)
            
        except Exception as e:
            logger.error(f"Error analyzing DDoS protection: {e}")
            result['error'] = str(e)
        
        return result
    
    def _check_dns(self, host: str) -> Dict[str, Any]:
        """Check DNS configuration"""
        result = {
            'host': host,
            'dns_records': {},
            'indicators': []
        }
        
        try:
            # Get A records
            ip_list = socket.gethostbyname_ex(host)
            result['dns_records']['a_records'] = ip_list[2]
            
            # Check for multiple IPs (indicator of load balancing)
            if len(ip_list[2]) > 1:
                result['indicators'].append("Multiple DNS A records (load balancing detected)")
            
            # Geo-distributed IP check (simplified)
            result['dns_records']['ip_count'] = len(ip_list[2])
            
        except socket.gaierror as e:
            result['error'] = f"DNS resolution failed: {e}"
        
        return result
    
    def _measure_response_times(self, url: str) -> Dict[str, float]:
        """Measure response times"""
        times = {
            'min': float('inf'),
            'max': 0,
            'avg': 0,
            'measurements': []
        }
        
        attempts = 3
        for _ in range(attempts):
            try:
                import time
                start = time.time()
                requests.get(url, timeout=5)
                elapsed = (time.time() - start) * 1000  # Convert to ms
                times['measurements'].append(elapsed)
            except:
                pass
        
        if times['measurements']:
            times['min'] = min(times['measurements'])
            times['max'] = max(times['measurements'])
            times['avg'] = sum(times['measurements']) / len(times['measurements'])
        
        return times
    
    def _get_ddos_recommendations(self, dns_result: Dict) -> List[str]:
        """Get DDoS protection recommendations"""
        recommendations = []
        
        recommendations.extend([
            "✓ Implement rate limiting on your servers",
            "✓ Use a reputable CDN or DDoS protection service",
            "✓ Configure firewall rules to block obvious attack patterns",
            "✓ Implement CAPTCHA for suspicious traffic",
            "✓ Set up alerts for unusual traffic patterns",
            "✓ Maintain updated WAF rules",
            "✓ Keep infrastructure patched and updated",
            "✓ Monitor for zero-day attacks",
            "✓ Have an incident response plan"
        ])
        
        return recommendations
    
    def run(self, url: str = None, **kwargs) -> Dict[str, Any]:
        """Run Anti-DDoS detection"""
        if not self.validate_input(url, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting Anti-DDoS detection for {url}")
        
        try:
            detection = self.detect_cdnandddos(url)
            analysis = self.analyze_ddos_protection(url)
            
            result = {
                'tool': 'Anti-DDoS Detector',
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'detection': detection,
                'analysis': analysis,
                'summary': {
                    'providers_detected': len(detection['detected_providers']),
                    'protection_status': 'LIKELY PROTECTED' if detection['detected_providers'] else 'UNKNOWN',
                    'confidence': detection['confidence_score']
                },
                'next_steps': [
                    "1. Verify detected protection with provider",
                    "2. Review DDoS protection policies",
                    "3. Test protection effectiveness (with authorization only)",
                    "4. Consider additional protection layers if needed"
                ]
            }
            
            self.add_result(result)
            return result
            
        except Exception as e:
            logger.exception("Anti-DDoS detection failed")
            self.add_error(f"Detection failed: {e}")
            return None
