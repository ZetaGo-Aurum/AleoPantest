"""
Anti-Clickjacking Header Generator - Generates security headers to prevent clickjacking

V3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output.
"""
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger


class AntiClickjackingGenerator(BaseTool):
    """Anti-Clickjacking Generator - Creates security headers and code to prevent clickjacking"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Anti-Clickjacking Generator",
            category=ToolCategory.CLICKJACKING,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Generates anti-clickjacking security headers and JavaScript code for protection",
            usage="aleopantest run anti-clickjacking --framework nginx --output security.conf",
            requirements=['python'],
            tags=['clickjacking', 'security', 'headers', 'protection']
        )
        super().__init__(metadata)
        self.output_dir = Path('output/anti_clickjacking')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_input(self, framework: str = None, **kwargs) -> bool:
        """Validate input"""
        if not framework:
            self.add_error("Framework is required (nginx, apache, nodejs, python, java, etc)")
            return False
        
        return True
    
    def generate_nginx_config(self) -> str:
        """Generate Nginx security configuration"""
        config = """# Nginx Anti-Clickjacking Configuration
# Add these headers to your Nginx configuration

# In your server block:
server {
    listen 80;
    server_name example.com;

    # 1. X-Frame-Options Header - Prevents clickjacking
    # Options: DENY (no framing), SAMEORIGIN (same origin only), ALLOW-FROM uri (deprecated)
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # 2. Content-Security-Policy - Modern approach
    # frame-ancestors 'none' = prevents any framing
    add_header Content-Security-Policy "frame-ancestors 'none';" always;
    
    # 3. Additional security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Example location block
    location / {
        proxy_pass http://backend;
    }
}

# Alternative: Stricter CSP for sensitive pages
server {
    listen 443 ssl http2;
    server_name secure.example.com;

    # Strictest protection
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none';" always;
    add_header X-Frame-Options "DENY" always;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
"""
        return config
    
    def generate_apache_config(self) -> str:
        """Generate Apache security configuration"""
        config = """# Apache Anti-Clickjacking Configuration
# Add these lines to your Apache configuration (.htaccess or httpd.conf)

# In .htaccess file or VirtualHost configuration:
<IfModule mod_headers.c>
    # 1. X-Frame-Options Header
    Header always set X-Frame-Options "SAMEORIGIN"
    
    # 2. Content-Security-Policy
    Header always set Content-Security-Policy "frame-ancestors 'none';"
    
    # 3. Additional security headers
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "no-referrer-when-downgrade"
</IfModule>

# For maximum protection:
<IfModule mod_headers.c>
    <Directory /var/www/sensitive>
        # Strictest policy for sensitive areas
        Header always set X-Frame-Options "DENY"
        Header always set Content-Security-Policy "default-src 'self'; frame-ancestors 'none';"
    </Directory>
</IfModule>

# Alternative method using mod_rewrite:
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteRule ^ - [E=HTTP_X_FRAME_OPTIONS:SAMEORIGIN]
    Header set X-Frame-Options "%{HTTP_X_FRAME_OPTIONS}e"
</IfModule>
"""
        return config
    
    def generate_nodejs_code(self) -> str:
        """Generate Node.js/Express security code"""
        code = """// Node.js / Express Anti-Clickjacking Protection

// 1. Using helmet.js (recommended)
const helmet = require('helmet');
const express = require('express');
const app = express();

// Helmet sets security headers automatically
app.use(helmet());

// 2. Manual header configuration
app.use((req, res, next) => {
    // X-Frame-Options header
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    
    // Content-Security-Policy
    res.setHeader(
        'Content-Security-Policy',
        "frame-ancestors 'none';"
    );
    
    // Additional security headers
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Referrer-Policy', 'no-referrer-when-downgrade');
    
    next();
});

// 3. Sensitive endpoints - stricter policy
app.use('/admin', (req, res, next) => {
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self'; frame-ancestors 'none';"
    );
    next();
});

// 4. Route example
app.get('/', (req, res) => {
    res.send('Protected page');
});

// 5. Helmet configuration with custom options
const helmetConfig = {
    frameguard: {
        action: 'deny'
    },
    contentSecurityPolicy: {
        directives: {
            frameAncestors: ["'none'"],
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", 'data:', 'https:']
        }
    }
};

app.use(helmet(helmetConfig));

// Start server
app.listen(3000, () => {
    console.log('Server running with anti-clickjacking protection');
});
"""
        return code
    
    def generate_python_code(self) -> str:
        """Generate Python (Flask/Django) security code"""
        code = """# Python Anti-Clickjacking Protection

# === FLASK ===
from flask import Flask

app = Flask(__name__)

# 1. Using Flask-Talisman (recommended)
from flask_talisman import Talisman

Talisman(app)  # Enables security headers by default

# 2. Manual header configuration
@app.after_request
def set_security_headers(response):
    # X-Frame-Options header
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # Content-Security-Policy
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none';"
    
    # Additional security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    
    return response

# 3. Sensitive routes decorator
def require_strict_security(f):
    def decorated_function(*args, **kwargs):
        from flask import make_response
        response = make_response(f(*args, **kwargs))
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'none';"
        return response
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin')
@require_strict_security
def admin():
    return 'Admin Panel'

@app.route('/')
def index():
    return 'Welcome'

if __name__ == '__main__':
    app.run()

# === DJANGO ===
# Add to middleware in settings.py:

MIDDLEWARE = [
    # ... existing middleware ...
    'django.middleware.security.SecurityMiddleware',
]

# Configure security settings:
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "DEFAULT_SRC": ("'self'",),
    "FRAME_ANCESTORS": ("'none'",),
    "SCRIPT_SRC": ("'self'",),
}

# Create custom middleware
from django.http import HttpResponse

class AntiClickjackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Content-Security-Policy'] = "frame-ancestors 'none';"
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response

# Add to MIDDLEWARE in settings.py:
MIDDLEWARE = [
    # ... existing middleware ...
    'yourapp.middleware.AntiClickjackingMiddleware',
]
"""
        return code
    
    def generate_javascript_framebuster(self) -> str:
        """Generate JavaScript frame-busting code"""
        code = """// JavaScript Anti-Clickjacking Protection (Frame Busting)

// 1. Simple frame buster
if (self !== top) {
    top.location = self.location;
}

// 2. More robust frame buster
if (top.location.href !== self.location.href) {
    if (document.referrer && document.referrer.length > 0) {
        // Referrer exists, might be in an iframe
        top.location = self.location;
    }
}

// 3. Advanced frame buster with checks
(function() {
    // Check if page is framed
    var inFrame = window !== window.top;
    
    if (inFrame) {
        try {
            window.top.location.href = window.self.location.href;
        } catch (e) {
            // Framing protection on parent
            console.warn('Cannot break out of frame: ' + e);
        }
    }
})();

// 4. Check for X-Frame-Options bypass (for testing)
function checkFramingProtection() {
    var framingDetected = false;
    
    // Method 1: Check window hierarchy
    try {
        if (window !== window.top) {
            framingDetected = true;
            console.warn('Page is being framed');
        }
    } catch (e) {
        // Accessed
        console.log('Frame busting protection active');
    }
    
    // Method 2: Attempt to access top location
    try {
        var topLocation = top.location.href;
        if (topLocation !== window.location.href) {
            console.warn('Page is framed - different origin');
        }
    } catch (e) {
        // Can't access top.location (different origin)
        console.log('Cross-origin framing detected');
    }
    
    return framingDetected;
}

// 5. Disable context menu (prevents right-click inspection)
document.addEventListener('contextmenu', function(e) {
    // Only for sensitive content
    if (window.location.pathname.includes('/admin')) {
        e.preventDefault();
        alert('Context menu disabled on this page');
    }
});

// 6. Prevent drag operations on sensitive areas
document.addEventListener('dragstart', function(e) {
    e.preventDefault();
    return false;
});

// 7. Monitor for changes in window top
setInterval(function() {
    if (window !== window.top && top.location.href !== self.location.href) {
        console.warn('Frame protection bypass attempt detected');
    }
}, 100);

// Run frame buster on page load
window.addEventListener('load', function() {
    if (self !== top) {
        top.location = self.location;
    }
});
"""
        return code
    
    def run(self, framework: str = None, output: str = None, **kwargs) -> Dict[str, Any]:
        """Run anti-clickjacking generator"""
        if not self.validate_input(framework, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Generating anti-clickjacking code for {framework}")
        
        try:
            result = {
                'tool': 'Anti-Clickjacking Generator',
                'timestamp': datetime.now().isoformat(),
                'framework': framework,
                'generated_code': {},
                'all_headers': {
                    'X-Frame-Options': 'SAMEORIGIN or DENY',
                    'Content-Security-Policy': "frame-ancestors 'none';",
                    'X-Content-Type-Options': 'nosniff',
                    'X-XSS-Protection': '1; mode=block',
                    'Referrer-Policy': 'no-referrer-when-downgrade'
                }
            }
            
            # Generate code for selected framework
            framework_lower = framework.lower()
            
            if framework_lower == 'nginx':
                code = self.generate_nginx_config()
                file_ext = 'conf'
            elif framework_lower == 'apache':
                code = self.generate_apache_config()
                file_ext = 'conf'
            elif framework_lower in ['nodejs', 'node', 'express']:
                code = self.generate_nodejs_code()
                file_ext = 'js'
            elif framework_lower in ['python', 'flask', 'django']:
                code = self.generate_python_code()
                file_ext = 'py'
            elif framework_lower in ['javascript', 'js']:
                code = self.generate_javascript_framebuster()
                file_ext = 'js'
            else:
                # Generate all
                result['generated_code']['nginx'] = self.generate_nginx_config()
                result['generated_code']['apache'] = self.generate_apache_config()
                result['generated_code']['nodejs'] = self.generate_nodejs_code()
                result['generated_code']['python'] = self.generate_python_code()
                result['generated_code']['javascript'] = self.generate_javascript_framebuster()
                code = None
            
            # Save to file if specific framework
            if code:
                if not output:
                    output = f'anti-clickjacking.{file_ext}'
                
                output_path = self.output_dir / output
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                result['generated_code'][framework] = code
                result['output_file'] = str(output_path)
            
            result['implementation_steps'] = [
                "1. Copy the generated code to your application",
                "2. Test with a clickjacking PoC to verify protection",
                "3. Use browser developer tools to confirm headers are set",
                "4. Test with multiple browsers for compatibility",
                "5. Monitor for any functional issues with legitimate iframes",
                "6. Document your security configuration"
            ]
            
            result['testing_recommendations'] = [
                "Use aleopantest run clickjacking-check --url YOUR_URL to verify",
                "Test with the aleopantest run clickjacking-make tool",
                "Verify headers with curl: curl -I YOUR_URL",
                "Use online header checkers like securityheaders.com"
            ]
            
            self.add_result(result)
            return self.get_results()
            
        except Exception as e:
            logger.exception("Code generation failed")
            self.add_error(f"Generation failed: {e}")
            return None
