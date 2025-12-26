"""URL Masking and Spoofing Tool"""
import json
import hashlib
import base64
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleo_pantest.core.logger import logger
from .redirect_server import RedirectServer


class URLMasking(BaseTool):
    """URL Masking - Hide real URLs behind fake domain names (Educational)"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="URL Masking",
            category=ToolCategory.UTILITIES,
            version="2.1.0",
            author="AleoPantest Team",
            description="Mask real URLs behind fake domain names for phishing and social engineering tests",
            usage="""
URL MASKING - Hide real URLs behind fake domain names

USAGE:
  aleopantest run url-mask --url <real_url> --fake-domain <domain> [--serve] [--port <port>]

PARAMETERS:
  --url TEXT              Real/malicious URL to hide (required)
  --fake-domain TEXT      Domain/Path to display (required)
  --serve                 Start a local server to handle redirects (Recommended)
  --port INT             Port for the local server (default: 8080)
  --method TEXT          Legacy methods: redirect, iframe, obfuscation, encoding

EXAMPLES:
  # Start server to redirect /google to attacker.com
  aleopantest run url-mask --url https://attacker.com --fake-domain google --serve

  # Legacy file generation
  aleopantest run url-mask --url https://attacker.com --fake-domain google.com --method redirect
            """,
            requirements=['requests', 'validators', 'qrcode'],
            tags=['url-masking', 'phishing', 'social-engineering', 'education'],
            risk_level="HIGH",
            legal_disclaimer="EDUCATIONAL USE ONLY - Unauthorized URL masking for phishing is illegal"
        )
        super().__init__(metadata)
    
    def validate_input(self, real_url: str = None, url: str = None, fake_domain: str = None, 
                      method: str = None, serve: bool = False, **kwargs) -> bool:
        """Validate input parameters"""
        # Support both --real-url and --url parameters
        final_url = url or real_url
        
        if not final_url:
            self.add_error("--url parameter is required (e.g., https://attacker.com)")
            return False
        
        if not fake_domain:
            self.add_error("--fake-domain parameter is required (e.g., youtube.com, facebook.com)")
            return False
        
        # Validate URL format
        if not final_url.startswith(('http://', 'https://')):
            self.add_error("URL must start with http:// or https://")
            return False
        
        method = method or 'redirect'
        if method not in ['redirect', 'iframe', 'obfuscation', 'encoding']:
            self.add_error(f"Invalid method: {method}. Must be: redirect, iframe, obfuscation, encoding")
            return False
        
        # Store normalized URL for execute method
        self._normalized_url = final_url
        
        return True
    
    def create_redirect_html(self, real_url: str, fake_domain: str) -> str:
        """Create HTML with redirect"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting...</title>
            <meta charset="utf-8">
            <script>
                // Redirect after 1 second
                setTimeout(function() {{
                    window.location.href = '{real_url}';
                }}, 1000);
            </script>
        </head>
        <body>
            <h1>{fake_domain}</h1>
            <p>Please wait while we redirect you...</p>
            <p style="color: #888; font-size: 12px;">If you are not redirected automatically, click <a href="{real_url}">here</a>.</p>
            <script>
                // Log click if user clicks
                document.addEventListener('click', function(e) {{
                    console.log('User interacted with page');
                }});
            </script>
        </body>
        </html>
        """
        return html
    
    def create_iframe_html(self, real_url: str, fake_domain: str) -> str:
        """Create HTML with iframe embedding"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{fake_domain}</title>
            <meta charset="utf-8">
            <style>
                body {{ margin: 0; padding: 0; }}
                iframe {{ width: 100%; height: 100vh; border: none; }}
            </style>
        </head>
        <body>
            <iframe src="{real_url}"></iframe>
            <script>
                // Prevent iframe escape
                if (window.self !== window.top) {{
                    window.top.location = '{real_url}';
                }}
            </script>
        </body>
        </html>
        """
        return html
    
    def create_obfuscated_html(self, real_url: str, fake_domain: str) -> str:
        """Create HTML with obfuscated redirect"""
        # Encode URL in multiple layers
        encoded_url = base64.b64encode(real_url.encode()).decode()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{fake_domain}</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>{fake_domain}</h1>
            <p>Loading content...</p>
            <script>
                function decode(str) {{
                    return atob(str);
                }}
                function redirect() {{
                    var url = decode('{encoded_url}');
                    window.location.href = url;
                }}
                window.onload = function() {{
                    setTimeout(redirect, 2000);
                }};
            </script>
        </body>
        </html>
        """
        return html
    
    def create_encoded_url(self, real_url: str, fake_domain: str) -> str:
        """Create encoded masked URL"""
        # Multiple encoding layers
        layer1 = base64.b64encode(real_url.encode()).decode()
        layer2 = quote(layer1)
        
        # Create masked URL structure
        masked = f"https://{fake_domain}/?p={layer2}"
        return masked
    
    def generate_qr_masked(self, real_url: str, fake_domain: str) -> Optional[str]:
        """Generate QR code for masked URL"""
        try:
            import qrcode
            
            # Create QR for the real URL
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(real_url)
            qr.make(fit=True)
            
            # Save QR code
            output_dir = Path('./output/url_masking')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            qr_file = output_dir / f'qr_masked_{hashlib.md5(real_url.encode()).hexdigest()[:8]}.png'
            qr.make_image(fill_color="black", back_color="white").save(qr_file)
            
            return str(qr_file)
        except ImportError:
            return None
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute URL masking"""
        if not self.validate_input(**kwargs):
            return {
                'success': False,
                'errors': self.errors
            }
        
        try:
            # Support both --url and --real-url
            real_url = self._normalized_url
            fake_domain = kwargs.get('fake_domain')
            method = kwargs.get('method', 'redirect')
            serve = kwargs.get('serve', False)
            port = int(kwargs.get('port', 8080))
            
            if serve:
                server = RedirectServer(port=port)
                # Register route using fake_domain as path
                path = fake_domain.split('.')[0] # Use first part of domain as path
                server.add_route(path, real_url)
                
                masked_url = f"http://localhost:{port}/{path}"
                
                result = {
                    "Method": "server-redirect",
                    "Real URL": real_url,
                    "Fake Domain/Path": fake_domain,
                    "Server URL": masked_url,
                    "Status": "Running (Ctrl+C to stop)"
                }
                self.add_result(result)
                
                # Start server (blocking)
                print(f"\n[+] Masked URL active: {masked_url}")
                print(f"[+] Redirects to: {real_url}")
                server.start()
                
                return {
                    'success': True,
                    'results': self.results,
                    'masked_url': masked_url
                }

            # Create appropriate HTML/URL based on method
            if method == 'redirect':
                content = self.create_redirect_html(real_url, fake_domain)
                content_type = 'html'
            elif method == 'iframe':
                content = self.create_iframe_html(real_url, fake_domain)
                content_type = 'html'
            elif method == 'obfuscation':
                content = self.create_obfuscated_html(real_url, fake_domain)
                content_type = 'html'
            elif method == 'encoding':
                content = self.create_encoded_url(real_url, fake_domain)
                content_type = 'url'
            else:
                content = self.create_redirect_html(real_url, fake_domain)
                content_type = 'html'
            
            # Save content to file
            output_dir = Path('./output/url_masking')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if content_type == 'html':
                filename = f'mask_{method}_{hashlib.md5(real_url.encode()).hexdigest()[:8]}.html'
                output_file = output_dir / filename
                output_file.write_text(content)
            else:
                filename = f'masked_url_{hashlib.md5(real_url.encode()).hexdigest()[:8]}.txt'
                output_file = output_dir / filename
                output_file.write_text(f"Original URL: {real_url}\nMasked URL: {content}")
            
            # Generate QR code if requested
            qr_file = None
            if kwargs.get('generate_qr', False):
                qr_file = self.generate_qr_masked(real_url, fake_domain)
            
            result = {
                "Method": method,
                "Real URL": real_url,
                "Fake Domain": fake_domain,
                "Content Type": content_type,
                "Saved to": str(output_file),
                "Masked URL": content if content_type == 'url' else f"HTML file at {output_file}",
            }
            
            if qr_file:
                result["QR Code"] = qr_file
            
            self.add_result(result)
            
            return {
                'success': True,
                'results': self.results,
                'output_file': str(output_file),
                'method': method,
                'qr_code': qr_file
            }
            
        except Exception as e:
            self.add_error(f"Execution failed: {str(e)}")
            return {
                'success': False,
                'errors': self.errors
            }
    
    def run(self, **kwargs):
        """Run URL masking - alias for execute"""
        return self.execute(**kwargs)
