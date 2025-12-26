import http.server
import socketserver
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from aleo_pantest.core.session import SessionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/redirect_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for redirect requests"""
    
    # Static registry of routes shared across handlers
    # Structure: {path: {'target': url, 'callback': func}}
    routes: Dict[str, Dict[str, Any]] = {}
    session_manager: Optional[SessionManager] = None
    
    def do_GET(self):
        """Handle GET requests"""
        # Check session quota
        if self.session_manager and not self.session_manager.check_quota():
            logger.warning("Access denied: Session quota reached")
            self.send_error(403, "Session expired (10-minute limit reached)")
            return

        # Remove leading slash for key lookup
        path_key = self.path.lstrip('/')
        
        if path_key in self.routes:
            route_data = self.routes[path_key]
            target_url = route_data['target']
            callback = route_data.get('callback')
            
            # Log access
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            referrer = self.headers.get('Referer', 'Direct')
            
            logger.info(f"Access detected: Path='{path_key}' IP={client_ip} UA='{user_agent}'")
            
            # Execute callback if exists (e.g., for stats)
            if callback:
                try:
                    callback(path_key, {
                        'ip': client_ip,
                        'user_agent': user_agent,
                        'referrer': referrer,
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.error(f"Callback error: {e}")
            
            # Perform redirect
            self.send_response(302)
            self.send_header('Location', target_url)
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
            self.end_headers()
        else:
            # 404 Not Found
            self.send_error(404, "Link expired or invalid")
            
    def log_message(self, format, *args):
        """Suppress default logging to keep console clean"""
        pass

class RedirectServer:
    """Multi-threaded Redirect Server"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.server: Optional[socketserver.ThreadingTCPServer] = None
        self.session_manager = SessionManager()
        RedirectHandler.session_manager = self.session_manager
        self._setup_directories()
        
    def _setup_directories(self):
        """Ensure log directory exists"""
        Path('logs').mkdir(exist_ok=True)
        
    def add_route(self, path: str, target_url: str, callback: Optional[Callable] = None):
        """Register a route for redirection"""
        # Strip leading slash to normalize
        path = path.lstrip('/')
        RedirectHandler.routes[path] = {
            'target': target_url,
            'callback': callback
        }
        logger.info(f"Route registered: /{path} -> {target_url}")
        
    def start(self, blocking: bool = True):
        """Start the server"""
        try:
            # Use ThreadingTCPServer for concurrent requests
            self.server = socketserver.ThreadingTCPServer(("", self.port), RedirectHandler)
            self.server.daemon_threads = True
            
            print(f"\n[+] Server started at http://localhost:{self.port}")
            print(f"[+] Press Ctrl+C to stop the server and deactivate links\n")
            
            if blocking:
                self.server.serve_forever()
            else:
                threading.Thread(target=self.server.serve_forever, daemon=True).start()
                
        except OSError as e:
            logger.error(f"Failed to start server on port {self.port}: {e}")
            print(f"\n[!] Error: Port {self.port} is likely in use. Try a different port.")
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop the server"""
        if self.server:
            print("\nStopping server...")
            self.server.shutdown()
            self.server.server_close()
            print("Server stopped.")
