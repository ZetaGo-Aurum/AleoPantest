"""
URL Shortener Tool with Custom Aliases

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import json
import hashlib
import random
import string
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger
from .redirect_server import RedirectServer


class URLShortener(BaseTool):
    """URL Shortener - Create short URLs with custom aliases"""
    
    # Simple URL shortening database (in-memory or file-based)
    STORAGE_FILE = Path('./output/url_shortener/urls.json')
    
    def __init__(self):
        metadata = ToolMetadata(
            name="URL Shortener",
            category=ToolCategory.UTILITIES,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Create short URLs with custom aliases for tracking and redirection",
            usage="""
URL SHORTENER - Create short URLs with custom aliases and click tracking

USAGE:
  aleopantest run url-shorten --url <target_url> [--alias <name>] [--serve] [--port <port>]

PARAMETERS:
  --url TEXT              Target URL to shorten (required)
  --alias TEXT            Custom alias for short URL (optional)
  --serve                 Start a local server to handle redirects (Recommended)
  --port INT             Port for the local server (default: 8080)
  --tracking TEXT         Legacy: Enable click tracking (default: true)
  --base-url TEXT        Legacy: Base URL for shortened links

OUTPUT:
  - Server URL: http://localhost:<port>/<alias>
  - Database: ./output/url_shortener/urls.json

FEATURES:
  - Real-time redirection with local server
  - Live click tracking and statistics
  - Persistent JSON database
  - Session-based link validity

EXAMPLES:
  # Create short link and start server
  aleopantest run url-shorten --url https://example.com --serve

  # Custom alias with server
  aleopantest run url-shorten --url https://example.com --alias mylink --serve --port 9000
            """,
            requirements=['requests', 'validators'],
            tags=['url-shortening', 'tracking', 'phishing', 'education']
        )
        super().__init__(metadata)
        self.url_database = self._load_database()
    
    def _load_database(self) -> Dict[str, Any]:
        """Load URL database from file"""
        self.STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if self.STORAGE_FILE.exists():
            try:
                with open(self.STORAGE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_database(self):
        """Save URL database to file"""
        self.STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.STORAGE_FILE, 'w') as f:
            json.dump(self.url_database, f, indent=2)
    
    def validate_input(self, url: str = None, alias: str = None, serve: bool = False, **kwargs) -> bool:
        """Validate input parameters"""
        if not url:
            self.add_error("url is required")
            return False
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            self.add_error("URL must start with http:// or https://")
            return False
        
        # Validate alias if provided
        if alias:
            if len(alias) < 3:
                self.add_error("Alias must be at least 3 characters")
                return False
            
            if not alias.isalnum() and alias not in ['-', '_']:
                self.add_error("Alias must contain only alphanumeric, dash, and underscore")
                return False
            
            if alias in self.url_database and not serve:
                self.add_error(f"Alias '{alias}' already exists. Use unique alias.")
                return False
        
        return True
    
    def generate_short_code(self, length: int = 6) -> str:
        """Generate random short code"""
        chars = string.ascii_letters + string.digits
        
        # Ensure uniqueness
        while True:
            code = ''.join(random.choices(chars, k=length))
            if code not in self.url_database:
                return code
        
    def create_short_url(self, url: str, alias: Optional[str] = None, base_url: str = "https://short.test") -> str:
        """Create shortened URL"""
        if alias:
            short_code = alias
        else:
            short_code = self.generate_short_code()
        
        short_url = f"{base_url}/{short_code}"
        return short_url, short_code
    
    def track_clicks(self, short_code: str, referrer: Optional[str] = None, ip: Optional[str] = None) -> bool:
        """Track click on shortened URL"""
        if short_code in self.url_database:
            entry = self.url_database[short_code]
            
            if 'clicks' not in entry:
                entry['clicks'] = []
            
            entry['clicks'].append({
                'timestamp': datetime.now().isoformat(),
                'referrer': referrer,
                'ip': ip
            })
            
            entry['click_count'] = len(entry['clicks'])
            self._save_database()
            return True
        
        return False
    
    def get_url_stats(self, short_code: str) -> Optional[Dict]:
        """Get statistics for shortened URL"""
        if short_code in self.url_database:
            entry = self.url_database[short_code]
            return {
                'original_url': entry.get('original_url'),
                'short_code': short_code,
                'created': entry.get('created'),
                'click_count': entry.get('click_count', 0),
                'clicks': entry.get('clicks', [])
            }
        return None
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute URL shortening"""
        if not self.validate_input(**kwargs):
            return {
                'success': False,
                'errors': self.errors
            }
        
        try:
            url = kwargs.get('url')
            alias = kwargs.get('alias')
            serve = kwargs.get('serve', False)
            port = int(kwargs.get('port', 8080))
            
            # Determine base URL
            if serve:
                default_base = f"http://localhost:{port}"
            else:
                default_base = "https://short.test"
                
            base_url = kwargs.get('base_url', default_base)
            track = kwargs.get('track', True)
            
            # Create/Update short URL entry
            if alias:
                short_code = alias
            else:
                short_code = self.generate_short_code()
            
            short_url = f"{base_url}/{short_code}"
            
            # Store in database
            self.url_database[short_code] = {
                'original_url': url,
                'short_url': short_url,
                'alias': short_code,
                'created': datetime.now().isoformat(),
                'click_count': self.url_database.get(short_code, {}).get('click_count', 0),
                'clicks': self.url_database.get(short_code, {}).get('clicks', []),
                'tracking_enabled': track
            }
            self._save_database()
            
            result = {
                "Original URL": url,
                "Short URL": short_url,
                "Short Code": short_code,
                "Alias": alias if alias else "auto-generated",
                "Tracking": "Enabled" if track else "Disabled",
                "Created": datetime.now().isoformat(),
                "Database Location": str(self.STORAGE_FILE)
            }
            
            self.add_result(result)
            
            if serve:
                server = RedirectServer(port=port)
                
                # Callback to update stats
                def tracking_callback(path, meta):
                    if path in self.url_database:
                        self.track_clicks(path, meta.get('referrer'), meta.get('ip'))
                
                # Register ALL existing routes from database
                print(f"\n[+] Loading {len(self.url_database)} links from database...")
                for code, data in self.url_database.items():
                    server.add_route(code, data['original_url'], callback=tracking_callback)
                
                result['Status'] = "Server Running (Ctrl+C to stop)"
                
                print(f"[+] Short URL active: {short_url}")
                print(f"[+] Redirects to: {url}")
                server.start()
                
                return {
                    'success': True,
                    'results': self.results,
                    'short_url': short_url
                }
            
            # Create tracking HTML if enabled (Legacy mode)
            if track:
                tracker_html = self._create_tracker_html(short_code, url)
                tracker_file = self.STORAGE_FILE.parent / f'track_{short_code}.html'
                tracker_file.write_text(tracker_html)
                result["Tracker HTML"] = str(tracker_file)
            
            return {
                'success': True,
                'results': self.results,
                'short_url': short_url,
                'short_code': short_code,
                'tracking_enabled': track
            }
            
        except Exception as e:
            self.add_error(f"Execution failed: {str(e)}")
            return {
                'success': False,
                'errors': self.errors
            }
    
    def _create_tracker_html(self, short_code: str, redirect_url: str) -> str:
        """Create HTML with tracking pixel"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting...</title>
            <meta charset="utf-8">
            <script>
                // Capture data before redirect
                var trackingData = {{
                    timestamp: new Date().toISOString(),
                    referrer: document.referrer,
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    platform: navigator.platform
                }};
                
                // Send tracking data
                fetch('/track/{short_code}', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(trackingData)
                }}).catch(e => console.log('Track'));
                
                // Redirect
                setTimeout(function() {{
                    window.location.href = '{redirect_url}';
                }}, 100);
            </script>
        </head>
        <body>
            <h1>Redirecting...</h1>
            <p>If not redirected, click <a href="{redirect_url}">here</a>.</p>
        </body>
        </html>
        """
        return html
    
    def run(self, **kwargs):
        """Run URL shortening - alias for execute"""
        return self.execute(**kwargs)
