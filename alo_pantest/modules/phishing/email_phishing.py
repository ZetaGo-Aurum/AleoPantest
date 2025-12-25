"""Email Phishing Detection and Analysis Tool"""
import re
from typing import Dict, Any, List, Tuple
from datetime import datetime

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class EmailPhishing(BaseTool):
    """Email Phishing Detector - Analyzes emails for phishing indicators"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Email Phishing Detector",
            category=ToolCategory.PHISHING,
            version="2.0.0",
            author="AloPantest Team",
            description="Detects phishing emails by analyzing headers, content, and suspicious patterns",
            usage="aleopantest run email-phishing --email 'sender@example.com' --subject 'Verify Account'",
            requirements=['python'],
            tags=['phishing', 'email', 'security', 'detection']
        )
        super().__init__(metadata)
    
    def validate_input(self, email: str = None, **kwargs) -> bool:
        """Validate input"""
        if not email and not kwargs.get('subject'):
            self.add_error("Email address or subject is required")
            return False
        return True
    
    def analyze_sender(self, sender_email: str) -> Dict[str, Any]:
        """Analyze sender email address for phishing indicators"""
        results = {
            'sender': sender_email,
            'checks': {},
            'risk_score': 0,
            'issues': []
        }
        
        try:
            # Check 1: Email format validity
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, sender_email):
                results['checks']['valid_format'] = {'status': 'INVALID', 'risk': 0.4}
                results['risk_score'] += 0.4
                results['issues'].append("Invalid email format")
            else:
                results['checks']['valid_format'] = {'status': 'VALID', 'risk': 0}
            
            # Check 2: Domain spoofing indicators
            domain = sender_email.split('@')[1]
            
            # Common brand names that are often spoofed
            spoofed_brands = ['paypal', 'amazon', 'apple', 'google', 'microsoft', 'bank', 'netflix', 'facebook']
            
            suspicious_domain = False
            for brand in spoofed_brands:
                if brand in domain.lower():
                    if not domain.lower().endswith(f'{brand}.com') and not domain.lower().endswith(f'{brand}.co.uk'):
                        results['issues'].append(f"Domain mimics '{brand}' but doesn't match official domain")
                        suspicious_domain = True
            
            if suspicious_domain:
                results['checks']['domain_spoofing'] = {'status': 'SUSPICIOUS', 'risk': 0.35}
                results['risk_score'] += 0.35
            else:
                results['checks']['domain_spoofing'] = {'status': 'NORMAL', 'risk': 0}
            
            # Check 3: Free email providers impersonating organizations
            free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
            
            # Check if appears to be organization but using free provider
            if any(domain.endswith(provider) for provider in free_providers):
                if any(org in sender_email.lower() for org in ['support', 'admin', 'account', 'billing', 'noreply']):
                    results['checks']['free_provider_impersonation'] = {'status': 'SUSPICIOUS', 'risk': 0.25}
                    results['risk_score'] += 0.25
                    results['issues'].append("Organization-like name using free email provider")
                else:
                    results['checks']['free_provider_impersonation'] = {'status': 'OK', 'risk': 0}
            else:
                results['checks']['free_provider_impersonation'] = {'status': 'CUSTOM_DOMAIN', 'risk': 0}
            
        except Exception as e:
            logger.error(f"Error analyzing sender: {e}")
            results['error'] = str(e)
        
        return results
    
    def analyze_subject(self, subject: str) -> Dict[str, Any]:
        """Analyze email subject for phishing indicators"""
        results = {
            'subject': subject,
            'checks': {},
            'risk_score': 0,
            'issues': []
        }
        
        # Check 1: Urgency indicators
        urgency_keywords = ['urgent', 'immediate', 'verify now', 'confirm', 'action required', 
                           'activate', 'validate', 'click here', 'limited time', 'act now',
                           'expire', 'suspended', 'locked', 'compromised', 'unauthorized']
        
        urgency_found = sum(1 for keyword in urgency_keywords if keyword.lower() in subject.lower())
        if urgency_found > 0:
            results['checks']['urgency_indicators'] = {'count': urgency_found, 'status': 'FOUND', 'risk': 0.2}
            results['risk_score'] += 0.2
            results['issues'].append(f"Contains {urgency_found} urgency keywords")
        else:
            results['checks']['urgency_indicators'] = {'count': 0, 'status': 'NONE', 'risk': 0}
        
        # Check 2: Request for sensitive information
        sensitive_keywords = ['verify', 'confirm', 'password', 'credit card', 'ssn', 'bank',
                             'personal information', 'update payment', 'reactivate', 'update account']
        
        sensitive_found = sum(1 for keyword in sensitive_keywords if keyword.lower() in subject.lower())
        if sensitive_found > 0:
            results['checks']['sensitive_requests'] = {'count': sensitive_found, 'status': 'FOUND', 'risk': 0.3}
            results['risk_score'] += 0.3
            results['issues'].append(f"Contains {sensitive_found} sensitive information requests")
        else:
            results['checks']['sensitive_requests'] = {'count': 0, 'status': 'NONE', 'risk': 0}
        
        # Check 3: Unusual capitalization
        uppercase_ratio = sum(1 for c in subject if c.isupper()) / len(subject) if subject else 0
        if uppercase_ratio > 0.3:
            results['checks']['unusual_capitalization'] = {'ratio': round(uppercase_ratio, 2), 'risk': 0.1}
            results['risk_score'] += 0.1
            results['issues'].append("Unusual capitalization pattern")
        else:
            results['checks']['unusual_capitalization'] = {'ratio': 0, 'risk': 0}
        
        return results
    
    def run(self, email: str = None, subject: str = None, **kwargs) -> Dict[str, Any]:
        """Run email phishing detection"""
        if not self.validate_input(email, subject=subject, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Starting Email Phishing detection")
        
        try:
            result = {
                'tool': 'Email Phishing Detector',
                'timestamp': datetime.now().isoformat(),
                'analyses': []
            }
            
            total_risk = 0
            analysis_count = 0
            
            # Analyze sender if provided
            if email:
                sender_analysis = self.analyze_sender(email)
                result['analyses'].append(sender_analysis)
                total_risk += sender_analysis['risk_score']
                analysis_count += 1
            
            # Analyze subject if provided
            if subject:
                subject_analysis = self.analyze_subject(subject)
                result['analyses'].append(subject_analysis)
                total_risk += subject_analysis['risk_score']
                analysis_count += 1
            
            # Calculate overall risk
            overall_risk = total_risk / analysis_count if analysis_count > 0 else 0
            
            result['overall_risk_score'] = round(overall_risk, 2)
            result['verdict'] = 'PHISHING' if overall_risk > 0.6 else 'SUSPICIOUS' if overall_risk > 0.4 else 'LEGITIMATE'
            result['recommendations'] = self._get_recommendations(overall_risk)
            
            self.add_result(result)
            return result
            
        except Exception as e:
            logger.exception("Email Phishing detection failed")
            self.add_error(f"Detection failed: {e}")
            return None
    
    def _get_recommendations(self, risk_score: float) -> List[str]:
        """Get recommendations based on risk score"""
        recommendations = []
        
        if risk_score > 0.6:
            recommendations.extend([
                "🚨 This email is likely phishing",
                "❌ DO NOT click any links",
                "❌ DO NOT download attachments",
                "🗑️ Delete the email immediately",
                "📢 Report to your email provider",
                "🔍 Verify by contacting the company directly"
            ])
        elif risk_score > 0.4:
            recommendations.extend([
                "⚠️ This email has suspicious characteristics",
                "🔍 Verify the sender's email address carefully",
                "🔗 Hover over links to see the real URL",
                "📞 Call the organization directly to verify",
                "🛑 Don't click links, go directly to the website instead"
            ])
        else:
            recommendations.extend([
                "✓ Email appears legitimate",
                "🔐 Still be cautious with personal information",
                "🔗 Verify links before clicking",
                "💡 Keep software updated"
            ])
        
        return recommendations
