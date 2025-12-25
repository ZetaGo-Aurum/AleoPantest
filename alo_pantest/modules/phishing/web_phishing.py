"""Web Phishing Detection and Analysis Tool"""
import json
import re
from typing import Dict, Any, List
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class WebPhishing(BaseTool):
    """Web Phishing Detection Tool - Detects phishing websites and suspicious URLs"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Web Phishing Detector",
            category=ToolCategory.PHISHING,
            version="2.0.0",
            author="AloPantest Team",
            description="Detects and analyzes phishing websites by checking suspicious characteristics",
            usage="aleopantest run web-phishing --url https://example.com",
            requirements=['requests', 'beautifulsoup4'],
            tags=['phishing', 'web', 'security', 'detection']
        )
        super().__init__(metadata)
        self.phishing_indicators = {
            'ip_based_url': r'^https?://\d+\.\d+\.\d+\.\d+',
            'long_url': lambda url: len(url) > 75,
            'url_shortener': r'(bit\.ly|tinyurl|short\.link|goo\.gl)',
            'suspicious_chars': r'[@%-._].*[@%-._]',
            'https_typo': r'http.*s://',
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
    
    def check_url_characteristics(self, url: str) -> Dict[str, Any]:
        """Check various URL characteristics for phishing indicators"""
        results = {
            'url': url,
            'checks': {},
            'risk_score': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Check 1: IP-based URL
        if re.match(self.phishing_indicators['ip_based_url'], url):
            results['checks']['ip_based_url'] = {'status': 'SUSPICIOUS', 'risk': 0.3}
            results['risk_score'] += 0.3
        else:
            results['checks']['ip_based_url'] = {'status': 'OK', 'risk': 0}
        
        # Check 2: URL length
        if self.phishing_indicators['long_url'](url):
            results['checks']['url_length'] = {'status': 'SUSPICIOUS', 'risk': 0.2}
            results['risk_score'] += 0.2
        else:
            results['checks']['url_length'] = {'status': 'OK', 'risk': 0}
        
        # Check 3: URL shortener
        if re.search(self.phishing_indicators['url_shortener'], url):
            results['checks']['url_shortener'] = {'status': 'SUSPICIOUS', 'risk': 0.25}
            results['risk_score'] += 0.25
        else:
            results['checks']['url_shortener'] = {'status': 'OK', 'risk': 0}
        
        # Check 4: Suspicious characters
        if re.search(self.phishing_indicators['suspicious_chars'], url):
            results['checks']['suspicious_chars'] = {'status': 'SUSPICIOUS', 'risk': 0.15}
            results['risk_score'] += 0.15
        else:
            results['checks']['suspicious_chars'] = {'status': 'OK', 'risk': 0}
        
        return results
    
    def check_page_content(self, url: str) -> Dict[str, Any]:
        """Check page content for phishing indicators"""
        results = {
            'url': url,
            'content_analysis': {},
            'risk_score': 0,
        }
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check 1: Presence of login forms
            forms = soup.find_all('form')
            login_forms = [f for f in forms if any(inp.get('type') == 'password' for inp in f.find_all('input'))]
            
            if login_forms:
                results['content_analysis']['login_forms'] = {
                    'count': len(login_forms),
                    'status': 'FOUND',
                    'risk': 0.2
                }
                results['risk_score'] += 0.2
            else:
                results['content_analysis']['login_forms'] = {'count': 0, 'status': 'NONE', 'risk': 0}
            
            # Check 2: Missing HTTPS
            if response.url.startswith('http://'):
                results['content_analysis']['missing_https'] = {'status': 'YES', 'risk': 0.3}
                results['risk_score'] += 0.3
            else:
                results['content_analysis']['missing_https'] = {'status': 'NO', 'risk': 0}
            
            # Check 3: External image/script sources
            external_resources = 0
            for tag in soup.find_all(['img', 'script']):
                src = tag.get('src') or tag.get('data')
                if src and not any(domain in src for domain in [response.netloc, 'localhost']):
                    external_resources += 1
            
            results['content_analysis']['external_resources'] = {
                'count': external_resources,
                'risk': min(external_resources * 0.05, 0.2)
            }
            results['risk_score'] += results['content_analysis']['external_resources']['risk']
            
            # Check 4: Title and content match (legitimate sites usually match)
            title = soup.find('title')
            results['content_analysis']['has_title'] = {'status': 'YES' if title else 'NO', 'risk': 0}
            
            results['status'] = 'SUCCESS'
            results['page_title'] = title.string if title else 'N/A'
            
        except Exception as e:
            results['status'] = 'FAILED'
            results['error'] = str(e)
            self.add_error(f"Failed to fetch page content: {e}")
        
        return results
    
    def run(self, url: str = None, **kwargs) -> Dict[str, Any]:
        """Run web phishing detection"""
        if not self.validate_input(url, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting Web Phishing detection for {url}")
        
        try:
            # Check URL characteristics
            url_analysis = self.check_url_characteristics(url)
            
            # Check page content
            content_analysis = self.check_page_content(url)
            
            # Combine results
            overall_risk = (url_analysis['risk_score'] + content_analysis['risk_score']) / 2
            
            result = {
                'tool': 'Web Phishing Detector',
                'timestamp': datetime.now().isoformat(),
                'url_analysis': url_analysis,
                'content_analysis': content_analysis,
                'overall_risk_score': round(overall_risk, 2),
                'verdict': 'PHISHING' if overall_risk > 0.6 else 'SUSPICIOUS' if overall_risk > 0.4 else 'LEGITIMATE',
                'recommendations': self._get_recommendations(overall_risk)
            }
            
            self.add_result(result)
            return result
            
        except Exception as e:
            logger.exception("Web Phishing detection failed")
            self.add_error(f"Detection failed: {e}")
            return None
    
    def _get_recommendations(self, risk_score: float) -> List[str]:
        """Get recommendations based on risk score"""
        recommendations = []
        
        if risk_score > 0.6:
            recommendations.extend([
                "⚠️ This URL appears to be phishing",
                "❌ Do NOT enter credentials on this site",
                "📢 Report this URL to your email provider",
                "🛡️ Use a password manager to prevent auto-fill"
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                "⚠️ This URL has suspicious characteristics",
                "✓ Verify the domain carefully",
                "📊 Check the certificate information",
                "💾 Use browser extensions to verify legitimacy"
            ])
        else:
            recommendations.extend([
                "✓ URL appears legitimate",
                "💡 Still exercise caution with personal information",
                "🔒 Use strong passwords",
                "🔐 Enable two-factor authentication when available"
            ])
        
        return recommendations
