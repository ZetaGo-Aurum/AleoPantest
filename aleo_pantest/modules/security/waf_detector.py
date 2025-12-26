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
            author="Aleocrophic Team",
            description="Detects Web Application Firewalls (WAF) and analyzes their configuration and effectiveness",
            usage="Aleocrophic run waf-detect --url https://example.com",
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
            # Check if url is in kwargs (sometimes passed this way from web/cli)
            url = kwargs.get('url')
            
        if not url:
            self.add_error("URL is required")
            return False
        
        # Normalize URL
        url = str(url).strip()
        if not url:
            self.add_error("URL cannot be empty")
            return False
            
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        try:
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            if not parsed.netloc:
                self.add_error(f"Invalid URL format: {url}")
                return False
        except Exception as e:
            self.add_error(f"Failed to parse URL: {str(e)}")
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
        # Get URL from either positional or keyword arguments
        target_url = url or kwargs.get('url')
        
        # Ensure we don't keep running if validation fails repeatedly
        if not hasattr(self, '_fail_count'):
            self._fail_count = 0
            
        if not self.validate_input(target_url, **kwargs):
            self._fail_count += 1
            if self._fail_count > 3:
                logger.error(f"WAF Detector: Too many failed validation attempts ({self._fail_count})")
            
            # Return a clear error result instead of None to help with output consistency
            return {
                'tool': 'WAF Detector',
                'status': 'error',
                'message': self.errors[-1] if self.errors else "Validation failed",
                'results': None
            }
        
        # Reset fail count on success
        self._fail_count = 0
        
        # Use normalized URL
        if target_url and not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url
            
        self.clear_results()
        logger.info(f"Starting WAF detection for {target_url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(target_url, headers=headers, timeout=10)
            
            # Detect WAF by headers
            header_detection = self.detect_waf_by_headers(response)
            
            # Optional: Test with payloads
            payload_detection = {}
            if test_payloads:
                payload_detection = self.detect_waf_by_response_code(target_url)
            
            # Analyze rules
            rule_analysis = self.analyze_waf_rules(target_url)
            
            result = {
                'tool': 'WAF Detector',
                'timestamp': datetime.now().isoformat(),
                'url': target_url,
                'status_code': response.status_code,
                'header_analysis': header_detection,
                'payload_analysis': payload_detection if test_payloads else None,
                'rule_analysis': rule_analysis,
                'waf_detected': header_detection['confidence'] > 0 or (test_payloads and payload_detection.get('waf_detected', False))
            }
            
            self.results = [result]
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error connecting to {target_url}: {str(e)}"
            self.add_error(error_msg)
            return {
                'tool': 'WAF Detector',
                'status': 'error',
                'message': error_msg,
                'results': None
            }
        except Exception as e:
            error_msg = f"Unexpected error during WAF detection: {str(e)}"
            self.add_error(error_msg)
            import traceback
            logger.error(f"WAF Detector Error: {traceback.format_exc()}")
            return {
                'tool': 'WAF Detector',
                'status': 'error',
                'message': error_msg,
                'results': None
            }
    
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
