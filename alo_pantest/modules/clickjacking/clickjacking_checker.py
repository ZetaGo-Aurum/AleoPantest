"""Clickjacking Checker - Detects if a website is vulnerable to clickjacking"""
import requests
from typing import Dict, Any, List
from datetime import datetime
from bs4 import BeautifulSoup

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class ClickjackingChecker(BaseTool):
    """Clickjacking Checker - Detects clickjacking vulnerabilities"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Clickjacking Checker",
            category=ToolCategory.WEB,
            version="2.0.0",
            author="AloPantest Team",
            description="Checks if a website is vulnerable to clickjacking attacks by analyzing security headers",
            usage="aleopantest run clickjacking-check --url https://example.com",
            requirements=['requests', 'beautifulsoup4'],
            tags=['clickjacking', 'web', 'security', 'headers']
        )
        super().__init__(metadata)
    
    def validate_input(self, url: str = None, **kwargs) -> bool:
        """Validate input URL"""
        if not url:
            self.add_error("URL is required")
            return False
        
        if not url.startswith(('http://', 'https://')):
            self.add_error("URL must start with http:// or https://")
            return False
        
        return True
    
    def check_headers(self, response: requests.Response) -> Dict[str, Any]:
        """Check security headers that prevent clickjacking"""
        headers_analysis = {
            'headers_present': {},
            'headers_missing': [],
            'vulnerability_score': 0,
            'issues': []
        }
        
        headers = response.headers
        
        # Check 1: X-Frame-Options header
        x_frame_options = headers.get('X-Frame-Options', '').upper()
        
        if x_frame_options:
            headers_analysis['headers_present']['X-Frame-Options'] = x_frame_options
            
            if x_frame_options == 'DENY':
                headers_analysis['headers_present']['X-Frame-Options-Status'] = 'SECURE'
                headers_analysis['headers_present']['X-Frame-Options-Risk'] = 0
            elif x_frame_options in ['SAMEORIGIN', 'SAME-ORIGIN']:
                headers_analysis['headers_present']['X-Frame-Options-Status'] = 'MODERATELY SECURE'
                headers_analysis['headers_present']['X-Frame-Options-Risk'] = 0.1
                headers_analysis['issues'].append("X-Frame-Options set to SAMEORIGIN - allows framing on same domain")
            elif x_frame_options.startswith('ALLOW-FROM'):
                headers_analysis['headers_present']['X-Frame-Options-Status'] = 'WEAK'
                headers_analysis['headers_present']['X-Frame-Options-Risk'] = 0.3
                headers_analysis['issues'].append("X-Frame-Options ALLOW-FROM is deprecated, use CSP instead")
            
            headers_analysis['vulnerability_score'] += headers_analysis['headers_present'].get('X-Frame-Options-Risk', 0)
        else:
            headers_analysis['headers_missing'].append('X-Frame-Options')
            headers_analysis['vulnerability_score'] += 0.4
            headers_analysis['issues'].append("X-Frame-Options header is missing - site is vulnerable to clickjacking")
        
        # Check 2: Content-Security-Policy header
        csp = headers.get('Content-Security-Policy', '')
        
        if csp:
            headers_analysis['headers_present']['Content-Security-Policy'] = 'Present'
            
            if 'frame-ancestors' in csp:
                headers_analysis['headers_present']['CSP-frame-ancestors'] = 'CONFIGURED'
                
                if "'none'" in csp:
                    headers_analysis['headers_present']['CSP-frame-ancestors-Risk'] = 0
                elif "'self'" in csp:
                    headers_analysis['headers_present']['CSP-frame-ancestors-Risk'] = 0.1
                else:
                    headers_analysis['headers_present']['CSP-frame-ancestors-Risk'] = 0.2
                    headers_analysis['issues'].append("CSP frame-ancestors allows multiple sources")
            else:
                headers_analysis['headers_missing'].append('CSP frame-ancestors directive')
                headers_analysis['vulnerability_score'] += 0.2
        else:
            headers_analysis['headers_missing'].append('Content-Security-Policy')
            headers_analysis['vulnerability_score'] += 0.3
        
        # Check 3: X-Content-Type-Options
        xcto = headers.get('X-Content-Type-Options', '').lower()
        
        if xcto == 'nosniff':
            headers_analysis['headers_present']['X-Content-Type-Options'] = 'PRESENT (nosniff)'
        elif not xcto:
            headers_analysis['headers_missing'].append('X-Content-Type-Options')
        
        return headers_analysis
    
    def check_html_content(self, response: requests.Response) -> Dict[str, Any]:
        """Check HTML content for iframe usage"""
        content_analysis = {
            'iframes_found': [],
            'forms_found': 0,
            'buttons_found': 0,
            'risk_indicators': []
        }
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for iframes
            iframes = soup.find_all('iframe')
            content_analysis['iframes_found'] = [
                {
                    'src': iframe.get('src', 'Not specified'),
                    'name': iframe.get('name', 'Not specified'),
                    'id': iframe.get('id', 'Not specified')
                }
                for iframe in iframes
            ]
            
            if iframes:
                content_analysis['risk_indicators'].append(f"{len(iframes)} iframe(s) found - could be used for clickjacking")
            
            # Check for sensitive interactive elements
            forms = soup.find_all('form')
            content_analysis['forms_found'] = len(forms)
            
            buttons = soup.find_all('button')
            content_analysis['buttons_found'] = len(buttons)
            
            if forms or buttons:
                content_analysis['risk_indicators'].append("Sensitive interactive elements found (forms/buttons)")
            
        except Exception as e:
            logger.error(f"Error analyzing HTML content: {e}")
            content_analysis['error'] = str(e)
        
        return content_analysis
    
    def run(self, url: str = None, **kwargs) -> Dict[str, Any]:
        """Run clickjacking vulnerability check"""
        if not self.validate_input(url, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting clickjacking check for {url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            headers_analysis = self.check_headers(response)
            content_analysis = self.check_html_content(response)
            
            # Calculate overall vulnerability
            vulnerability_score = min(headers_analysis['vulnerability_score'], 1.0)
            
            result = {
                'tool': 'Clickjacking Checker',
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'final_url': response.url,
                'status_code': response.status_code,
                'headers_analysis': headers_analysis,
                'content_analysis': content_analysis,
                'vulnerability_score': round(vulnerability_score, 2),
                'verdict': 'VULNERABLE' if vulnerability_score > 0.6 else 'POTENTIALLY_VULNERABLE' if vulnerability_score > 0.3 else 'PROTECTED',
                'recommendations': self._get_recommendations(vulnerability_score, headers_analysis)
            }
            
            self.add_result(result)
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch URL: {e}")
            self.add_error(f"Failed to fetch URL: {e}")
            return None
        except Exception as e:
            logger.exception("Clickjacking check failed")
            self.add_error(f"Check failed: {e}")
            return None
    
    def _get_recommendations(self, score: float, headers_analysis: Dict) -> List[str]:
        """Get recommendations based on vulnerability analysis"""
        recommendations = []
        
        if score > 0.6:
            recommendations.extend([
                "🚨 VULNERABLE: Site is susceptible to clickjacking attacks",
                "✓ Add X-Frame-Options: DENY header",
                "✓ Implement Content-Security-Policy with frame-ancestors 'none'",
                "✓ Add X-Content-Type-Options: nosniff header"
            ])
        elif score > 0.3:
            recommendations.extend([
                "⚠️ PARTIALLY PROTECTED: Some protections in place",
                "✓ Review and strengthen X-Frame-Options",
                "✓ Implement or enhance Content-Security-Policy",
                "✓ Consider adding additional security headers"
            ])
        else:
            recommendations.extend([
                "✓ PROTECTED: Good clickjacking protections in place",
                "💡 Regularly test security headers",
                "🔄 Keep security policy up to date",
                "📊 Monitor for new attack vectors"
            ])
        
        # Add specific fixes
        if 'X-Frame-Options' in headers_analysis['headers_missing']:
            recommendations.append("ADD: X-Frame-Options: DENY")
        
        if 'Content-Security-Policy' in headers_analysis['headers_missing']:
            recommendations.append("ADD: Content-Security-Policy: frame-ancestors 'none';")
        
        return recommendations
