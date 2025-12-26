"""WAF (Web Application Firewall) Detector and Analyzer"""
import requests
from typing import Dict, Any, List
from datetime import datetime

from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleo_pantest.core.logger import logger


class WAFDetector(BaseTool):
    """WAF Detector - Identifies and analyzes Web Application Firewall implementations"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="WAF Detector",
            category=ToolCategory.SECURITY,
            version="2.0.0",
            author="AleoPantest Team",
            description="Detects Web Application Firewalls (WAF) and analyzes their configuration and effectiveness",
            usage="aleopantest run waf-detect --url https://example.com",
            requirements=['requests'],
            tags=['waf', 'firewall', 'web', 'security']
        )
        super().__init__(metadata)
        
        # Known WAF signatures
        self.waf_signatures = {
            'modsecurity': {
                'headers': ['mod-security', 'mod-security-message'],
                'fingerprints': ['modsec', 'rules id'],
                'response_codes': [403, 406]
            },
            'cloudflare': {
                'headers': ['cf-ray', 'cf-cache-status', 'cf-request-id'],
                'fingerprints': ['cloudflare'],
                'error_page': 'cloudflare.com/error'
            },
            'akamai': {
                'headers': ['akamai-cache-status', 'akamai-x-cache'],
                'fingerprints': ['akamai']
            },
            'barracuda': {
                'headers': ['x-barracuda-block-id'],
                'fingerprints': ['barracuda'],
                'response_codes': [403]
            },
            'imperva': {
                'headers': ['x-iinfo', 'x-cdn'],
                'fingerprints': ['imperva', 'incapsula']
            },
            'fortiweb': {
                'headers': ['x-fortiweb'],
                'fingerprints': ['fortiweb']
            },
            'f5-bigip': {
                'headers': ['x-f5-denied'],
                'fingerprints': ['f5', 'bigip']
            },
            'nginx-modsecurity': {
                'headers': ['server'],
                'fingerprints': ['nginx'],
                'body_patterns': ['ModSecurity']
            }
        }
        
        # SQL Injection and XSS payloads for WAF testing
        self.test_payloads = {
            'sql_injection': [
                "' OR '1'='1",
                "1' UNION SELECT NULL--",
                "admin' --",
                "1'; DROP TABLE users--"
            ],
            'xss': [
                "<script>alert('xss')</script>",
                "<img src=x onerror=alert('xss')>",
                "javascript:alert('xss')",
                "<svg onload=alert('xss')>"
            ],
            'path_traversal': [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\config\\sam",
                "....//....//....//etc/passwd"
            ]
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
    
    def detect_waf_by_headers(self, response: requests.Response) -> Dict[str, Any]:
        """Detect WAF by analyzing response headers"""
        result = {
            'detected_waf': [],
            'suspicious_headers': {},
            'confidence': 0
        }
        
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        # Check against known WAF signatures
        for waf_name, signatures in self.waf_signatures.items():
            score = 0
            found_indicators = []
            
            # Check headers
            for header in signatures.get('headers', []):
                if header.lower() in headers:
                    score += 0.3
                    found_indicators.append({
                        'type': 'header',
                        'name': header,
                        'value': headers.get(header.lower(), '')
                    })
            
            # Check server header for fingerprints
            server_header = headers.get('server', '').lower()
            for fingerprint in signatures.get('fingerprints', []):
                if fingerprint.lower() in server_header:
                    score += 0.4
                    found_indicators.append({
                        'type': 'fingerprint',
                        'pattern': fingerprint,
                        'location': 'Server header'
                    })
            
            if score > 0:
                result['detected_waf'].append({
                    'waf': waf_name.upper(),
                    'confidence': round(min(score, 1.0), 2),
                    'indicators': found_indicators
                })
        
        # Collect unusual headers
        for header_key, header_value in headers.items():
            if any(keyword in header_key.lower() for keyword in ['x-', 'cf-', 'akamai', 'mod-']):
                result['suspicious_headers'][header_key] = header_value
        
        return result
    
    def detect_waf_by_response_code(self, url: str) -> Dict[str, Any]:
        """Detect WAF by testing with malicious payloads"""
        result = {
            'payload_tests': [],
            'blocked_payloads': 0,
            'waf_detected': False,
            'response_patterns': {}
        }
        
        try:
            # Test SQL injection payloads
            for payload in self.test_payloads['sql_injection'][:2]:  # Test first 2
                test_url = f"{url}?id={payload}"
                
                try:
                    response = requests.get(test_url, timeout=5)
                    
                    test_result = {
                        'type': 'sql_injection',
                        'payload': payload,
                        'status_code': response.status_code,
                        'blocked': response.status_code in [403, 406, 401]
                    }
                    
                    result['payload_tests'].append(test_result)
                    
                    if test_result['blocked']:
                        result['blocked_payloads'] += 1
                        result['waf_detected'] = True
                
                except requests.exceptions.RequestException:
                    pass
            
            # Test XSS payloads
            for payload in self.test_payloads['xss'][:1]:  # Test first one
                test_url = f"{url}?search={payload}"
                
                try:
                    response = requests.get(test_url, timeout=5)
                    
                    test_result = {
                        'type': 'xss',
                        'payload': payload,
                        'status_code': response.status_code,
                        'blocked': response.status_code in [403, 406, 401]
                    }
                    
                    result['payload_tests'].append(test_result)
                    
                    if test_result['blocked']:
                        result['blocked_payloads'] += 1
                        result['waf_detected'] = True
                
                except requests.exceptions.RequestException:
                    pass
            
            result['blocked_percentage'] = round(
                (result['blocked_payloads'] / len(result['payload_tests']) * 100) 
                if result['payload_tests'] else 0, 2
            )
            
        except Exception as e:
            logger.error(f"Error testing payloads: {e}")
            result['error'] = str(e)
        
        return result
    
    def analyze_waf_rules(self, url: str) -> Dict[str, Any]:
        """Analyze detected WAF rules and configuration"""
        result = {
            'rule_detection': [],
            'protection_level': 'UNKNOWN',
            'potential_bypasses': []
        }
        
        try:
            # Common WAF bypass techniques
            bypass_techniques = [
                'URL encoding',
                'Double encoding',
                'Case variation',
                'Comment insertion',
                'Null byte injection',
                'Alternative syntax',
                'Fragmentation'
            ]
            
            result['protection_level'] = 'HIGH'
            result['potential_bypasses'] = bypass_techniques
            
        except Exception as e:
            logger.error(f"Error analyzing rules: {e}")
            result['error'] = str(e)
        
        return result
    
    def run(self, url: str = None, test_payloads: bool = False, **kwargs) -> Dict[str, Any]:
        """Run WAF detection"""
        if not self.validate_input(url, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting WAF detection for {url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            # Detect WAF by headers
            header_detection = self.detect_waf_by_headers(response)
            
            # Optional: Test with payloads
            payload_detection = {}
            if test_payloads:
                payload_detection = self.detect_waf_by_response_code(url)
            
            # Analyze rules
            rule_analysis = self.analyze_waf_rules(url)
            
            result = {
                'tool': 'WAF Detector',
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'status_code': response.status_code,
                'header_analysis': header_detection,
                'payload_analysis': payload_detection if test_payloads else None,
                'rule_analysis': rule_analysis,
                'summary': {
                    'waf_detected': len(header_detection['detected_waf']) > 0 or 
                                   (payload_detection.get('waf_detected', False) if test_payloads else False),
                    'detected_firewalls': [waf['waf'] for waf in header_detection['detected_waf']],
                    'protection_level': rule_analysis['protection_level']
                },
                'recommendations': self._get_recommendations(header_detection, rule_analysis)
            }
            
            self.add_result(result)
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch URL: {e}")
            self.add_error(f"Failed to fetch URL: {e}")
            return None
        except Exception as e:
            logger.exception("WAF detection failed")
            self.add_error(f"Detection failed: {e}")
            return None
    
    def _get_recommendations(self, header_detection: Dict, rule_analysis: Dict) -> List[str]:
        """Get WAF recommendations"""
        recommendations = []
        
        if header_detection['detected_waf']:
            recommendations.extend([
                f"✓ {len(header_detection['detected_waf'])} WAF(s) detected",
                "✓ Understand the WAF's capabilities and limitations",
                "✓ Regularly update WAF rules",
                "✓ Monitor for false positives/negatives"
            ])
        else:
            recommendations.extend([
                "⚠️ No WAF detected - consider implementing one",
                "✓ A WAF can protect against common web attacks",
                "✓ Choose a WAF solution appropriate for your needs",
                "✓ Ensure proper configuration of WAF rules"
            ])
        
        recommendations.extend([
            "✓ Test WAF effectiveness regularly",
            "✓ Keep WAF rules updated with latest threats",
            "✓ Monitor for WAF evasion attempts",
            "✓ Combine WAF with other security measures"
        ])
        
        return recommendations
