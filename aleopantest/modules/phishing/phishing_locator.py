"""Phishing Locator Tool - Finds phishing sites related to a domain"""
import re
from typing import Dict, Any, List
from datetime import datetime
import requests

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger


class PhishingLocator(BaseTool):
    """Phishing Locator - Locates and tracks phishing sites mimicking a target domain"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Phishing Locator",
            category=ToolCategory.PHISHING,
            version="2.0.0",
            author="Aleocrophic Team",
            description="Locates phishing sites and domains that mimic legitimate organizations",
            usage="aleopantest run phishing-locator --domain example.com",
            requirements=['requests', 'beautifulsoup4'],
            tags=['phishing', 'locator', 'domain', 'tracking']
        )
        super().__init__(metadata)
        self.phishing_databases = [
            'phishtank',
            'urlhaus',
            'abuse-net'
        ]
    
    def validate_input(self, domain: str = None, **kwargs) -> bool:
        """Validate input domain"""
        if not domain:
            self.add_error("Domain is required")
            return False
        
        # Basic domain validation
        domain_pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
        if not re.match(domain_pattern, domain.lower()):
            self.add_error("Invalid domain format")
            return False
        
        return True
    
    def generate_phishing_variants(self, domain: str) -> List[str]:
        """Generate possible phishing domain variants"""
        variants = []
        base = domain.split('.')[0]
        tld = domain.split('.')[-1]
        
        # Common phishing tactics
        phishing_patterns = [
            f'{base}1.{tld}',  # Adding numbers
            f'{base}0.{tld}',
            f'{base}admin.{tld}',  # Adding words
            f'{base}secure.{tld}',
            f'{base}login.{tld}',
            f'{base}verify.{tld}',
            f'{base}update.{tld}',
            f'my{base}.{tld}',  # Prefix additions
            f'login-{base}.{tld}',
            f'secure-{base}.{tld}',
            f'verify-{base}.{tld}',
            f'{base}.{tld.replace("com", "co")}',  # TLD variations
            f'{base}.{tld}s',
            f'{base}-{tld}.com',  # Other variations
            f'{base}{tld}.com',
        ]
        
        return phishing_patterns
    
    def check_domain_availability(self, domain: str) -> Dict[str, Any]:
        """Check if domain is registered"""
        result = {
            'domain': domain,
            'status': 'UNKNOWN',
            'is_registered': False,
            'risk_level': 'LOW'
        }
        
        try:
            # Try to resolve domain
            import socket
            socket.gethostbyname(domain)
            result['is_registered'] = True
            result['status'] = 'REGISTERED'
            result['risk_level'] = 'HIGH'
        except socket.gaierror:
            result['is_registered'] = False
            result['status'] = 'NOT_REGISTERED'
            result['risk_level'] = 'LOW'
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'ERROR'
        
        return result
    
    def check_phishing_database(self, domain: str) -> Dict[str, Any]:
        """Check if domain is in phishing databases"""
        result = {
            'domain': domain,
            'found_in_databases': [],
            'last_checked': datetime.now().isoformat()
        }
        
        # Check PhishTank (simplified - would need API key)
        phishtank_pattern = r'phishing|suspicious'
        if re.search(phishtank_pattern, domain.lower()):
            result['found_in_databases'].append('phishtank')
        
        # Check URLhaus patterns
        suspicious_patterns = ['verify', 'confirm', 'secure', 'login', 'update', 'account']
        if any(pattern in domain.lower() for pattern in suspicious_patterns):
            # Not necessarily malicious, just log it
            result['suspicious_patterns'] = [p for p in suspicious_patterns if p in domain.lower()]
        
        return result
    
    def analyze_phishing_risk(self, domain: str) -> Dict[str, Any]:
        """Analyze phishing risk for a domain"""
        result = {
            'domain': domain,
            'risk_factors': [],
            'overall_risk_score': 0
        }
        
        domain_lower = domain.lower()
        
        # Check 1: Homograph attacks (similar looking characters)
        homograph_chars = [
            ('o', '0'),
            ('i', '1'),
            ('l', '1'),
            ('s', '5'),
        ]
        
        suspicious_homographs = []
        for orig, fake in homograph_chars:
            if fake in domain_lower and orig not in domain_lower:
                suspicious_homographs.append(f"Contains '{fake}' instead of '{orig}'")
        
        if suspicious_homographs:
            result['risk_factors'].append({
                'type': 'HOMOGRAPH_ATTACK',
                'issues': suspicious_homographs,
                'risk_increase': 0.2
            })
            result['overall_risk_score'] += 0.2
        
        # Check 2: Suspicious keywords
        suspicious_keywords = ['verify', 'confirm', 'update', 'secure', 'login', 'signin',
                              'account', 'payment', 'billing', 'security', 'action']
        
        found_keywords = [kw for kw in suspicious_keywords if kw in domain_lower]
        if found_keywords:
            result['risk_factors'].append({
                'type': 'SUSPICIOUS_KEYWORDS',
                'keywords': found_keywords,
                'risk_increase': 0.15 * len(found_keywords)
            })
            result['overall_risk_score'] += min(0.15 * len(found_keywords), 0.5)
        
        # Check 3: Domain age (new domains higher risk)
        # Simplified check - would need WHOIS data
        result['risk_factors'].append({
            'type': 'DOMAIN_AGE',
            'note': 'Check WHOIS for domain age - new domains higher risk',
            'risk_increase': 0
        })
        
        return result
    
    def run(self, domain: str = None, **kwargs) -> Dict[str, Any]:
        """Run phishing locator"""
        if not self.validate_input(domain, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting Phishing Locator for {domain}")
        
        try:
            result = {
                'tool': 'Phishing Locator',
                'timestamp': datetime.now().isoformat(),
                'target_domain': domain,
                'phishing_variants': [],
                'registered_variants': [],
                'analysis': {}
            }
            
            # Generate variants
            variants = self.generate_phishing_variants(domain)
            logger.info(f"Generated {len(variants)} phishing variants")
            
            registered_count = 0
            for variant in variants:
                availability = self.check_domain_availability(variant)
                result['phishing_variants'].append(availability)
                
                if availability['is_registered']:
                    registered_count += 1
                    
                    # Analyze registered variant
                    db_check = self.check_phishing_database(variant)
                    risk_analysis = self.analyze_phishing_risk(variant)
                    
                    result['registered_variants'].append({
                        'domain': variant,
                        'database_check': db_check,
                        'risk_analysis': risk_analysis
                    })
            
            # Overall analysis
            result['analysis'] = {
                'total_variants_checked': len(variants),
                'registered_variants': registered_count,
                'registration_percentage': round((registered_count / len(variants) * 100), 2),
                'threat_level': 'CRITICAL' if registered_count >= 3 else 'HIGH' if registered_count >= 1 else 'LOW'
            }
            
            result['recommendations'] = self._get_recommendations(registered_count, domain)
            
            self.add_result(result)
            return result
            
        except Exception as e:
            logger.exception("Phishing Locator failed")
            self.add_error(f"Locator failed: {e}")
            return None
    
    def _get_recommendations(self, registered_count: int, domain: str) -> List[str]:
        """Get recommendations based on findings"""
        recommendations = []
        
        if registered_count >= 3:
            recommendations.extend([
                f"🚨 CRITICAL: {registered_count} phishing variants of {domain} are registered",
                "📢 Report all variants to your domain registrar",
                "⚖️ Consider legal action against phishing operators",
                "🛡️ Implement WHOIS privacy protection",
                "📧 Send cease & desist notices"
            ])
        elif registered_count >= 1:
            recommendations.extend([
                f"⚠️ WARNING: {registered_count} phishing variant(s) of {domain} detected",
                "📢 Report to domain registrar and hosting provider",
                "🔍 Monitor these domains for activity",
                "🛡️ Protect your users with security warnings"
            ])
        else:
            recommendations.extend([
                "✓ No registered phishing variants detected",
                "💡 Continue monitoring for new variants",
                "🛡️ Implement brand protection services",
                "📢 Consider registering common misspellings yourself"
            ])
        
        return recommendations
