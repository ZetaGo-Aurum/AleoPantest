"""URL Shortener Tool with Custom Aliases"""
import json
import hashlib
import random
import string
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from alo_pantest.core.logger import logger


class URLShortener(BaseTool):
    """URL Shortener - Create short URLs with custom aliases"""
    
    # Simple URL shortening database (in-memory or file-based)
    STORAGE_FILE = Path('./output/url_shortener/urls.json')
    
    def __init__(self):
        metadata = ToolMetadata(
            name="URL Shortener",
            category=ToolCategory.UTILITIES,
            version="2.0.0",
            author="AloPantest Team",
            description="Create short URLs with custom aliases for tracking and redirection",
            usage="aleopantest run url-shorten --url https://example.com --alias mylink",
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
    
    def validate_input(self, url: str = None, alias: str = None, **kwargs) -> bool:
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
            
            if alias in self.url_database:
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
            base_url = kwargs.get('base_url', 'https://short.test')
            track = kwargs.get('track', True)
            
            # Create short URL
            short_url, short_code = self.create_short_url(url, alias, base_url)
            
            # Store in database
            self.url_database[short_code] = {
                'original_url': url,
                'short_url': short_url,
                'alias': alias,
                'created': datetime.now().isoformat(),
                'click_count': 0,
                'clicks': [],
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
            
            # Create tracking HTML if enabled
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
