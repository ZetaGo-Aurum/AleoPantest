"""Base tool framework untuk semua tools"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import json
import socket
import getpass
import platform
import time
import datetime
from pathlib import Path

from ..core.logger import logger


class ToolCategory(Enum):
    """Tool categories"""
    NETWORK = "Network"
    WEB = "Web"
    OSINT = "OSINT"
    CRYPTO = "Crypto"
    WIRELESS = "Wireless"
    DATABASE = "Database"
    UTILITIES = "Utilities"
    REVERSE = "Reverse Engineering"
    PHISHING = "Phishing"
    SECURITY = "Security"
    CLICKJACKING = "Clickjacking"


@dataclass
class ToolMetadata:
    """Metadata untuk setiap tool"""
    name: str
    category: ToolCategory
    version: str
    author: str
    description: str
    usage: str
    requirements: list
    tags: list
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    legal_disclaimer: str = ""
    example: str = ""
    parameters: Dict[str, str] = None
    form_schema: List[Dict[str, Any]] = None  # UI Form schema for web/TUI
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'category': self.category.value,
            'version': self.version,
            'author': self.author,
            'description': self.description,
            'usage': self.usage,
            'requirements': self.requirements,
            'tags': self.tags,
            'risk_level': self.risk_level,
            'legal_disclaimer': self.legal_disclaimer,
            'example': self.example,
            'parameters': self.parameters or {},
            'form_schema': self.form_schema or [],
        }


class BaseTool(ABC):
    """Base class untuk semua tools"""
    
    def __init__(self, metadata: Optional[ToolMetadata] = None):
        self.metadata = metadata
        self.results = []
        self.errors = []
        self.warnings = []
        self.is_running = False
        self.start_time = None
        
        # Core Parameters for v3.3
        self.timeout = 30
        self.headers = {
            "User-Agent": "AleoPantest/3.3.0",
            "Accept": "*/*"
        }
        self.auth = None
        self.proxy = None
        self.scan_options = {}

    @staticmethod
    def get_admin_info() -> Dict[str, str]:
        """Returns identification of the current admin/user"""
        try:
            return {
                "username": getpass.getuser(),
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_release": platform.release(),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except:
            return {"username": "unknown", "hostname": "unknown", "os": "unknown"}

    def check_safety(self, duration_seconds: int = 0) -> bool:
        """
        Safety check for high-risk tools.
        Enforces 1-hour limit for intensive tasks.
        """
        if self.metadata and self.metadata.risk_level in ["HIGH", "CRITICAL"]:
            MAX_DURATION = 3600  # 1 hour
            if duration_seconds > MAX_DURATION:
                self.add_error(f"Safety Limit: Durasi eksekusi {duration_seconds}s melebihi batas maksimal 1 jam.")
                return False
            
            # Additional safety logic can be added here
            self.audit_log("Safety check passed for high-risk execution.")
        return True

    def audit_log(self, action: str):
        """Log actions for auditing high-risk tools"""
        admin = self.get_admin_info()
        audit_msg = f"AUDIT | {admin['username']}@{admin['hostname']} | Tool: {self.metadata.name if self.metadata else 'Unknown'} | Action: {action}"
        logger.info(audit_msg)
        # In a real scenario, this could write to a separate secure audit file
        audit_file = Path("logs/audit.log")
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {audit_msg}\n")
    
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute tool"""
        pass
    
    def validate_input(self, *args, **kwargs) -> bool:
        """Validate input parameters (default implementation returns True)"""
        return True
    
    def add_result(self, result: Any):
        """Add result"""
        self.results.append(result)
    
    def add_error(self, error: str):
        """Add error"""
        self.errors.append(error)
        logger.error(f"[{self.metadata.name}] {error}")
    
    def add_warning(self, warning: str):
        """Add warning"""
        self.warnings.append(warning)
        logger.warning(f"[{self.metadata.name}] {warning}")
    
    def get_results(self) -> list:
        """Get all results"""
        return self.results
    
    def clear_results(self):
        """Clear results"""
        self.results.clear()
        self.errors.clear()
        self.warnings.clear()
    
    def set_core_params(self, **kwargs):
        """Helper to set common parameters for all tools"""
        if 'timeout' in kwargs and kwargs['timeout']: 
            self.timeout = int(kwargs['timeout'])
        if 'headers' in kwargs and kwargs['headers']: 
            if isinstance(kwargs['headers'], str):
                try: 
                    custom_headers = json.loads(kwargs['headers'])
                    self.headers.update(custom_headers)
                except: pass
            elif isinstance(kwargs['headers'], dict):
                self.headers.update(kwargs['headers'])
        if 'auth_user' in kwargs and 'auth_pass' in kwargs:
            if kwargs['auth_user'] and kwargs['auth_pass']:
                self.auth = (kwargs['auth_user'], kwargs['auth_pass'])
        if 'proxy' in kwargs and kwargs['proxy']: 
            self.proxy = kwargs['proxy']
        if 'scan_options' in kwargs and kwargs['scan_options']: 
            self.scan_options.update(kwargs['scan_options'])

    @staticmethod
    def get_common_form_schema() -> List[Dict[str, Any]]:
        """Returns common form fields for advanced settings"""
        return [
            {
                "name": "timeout",
                "label": "Timeout (seconds)",
                "type": "number",
                "default": 30,
                "required": False,
                "group": "Advanced"
            },
            {
                "name": "headers",
                "label": "Custom Headers (JSON)",
                "type": "textarea",
                "placeholder": '{"User-Agent": "Custom-Agent"}',
                "required": False,
                "group": "Advanced"
            },
            {
                "name": "proxy",
                "label": "Proxy (http://user:pass@host:port)",
                "type": "text",
                "placeholder": "http://127.0.0.1:8080",
                "required": False,
                "group": "Advanced"
            },
            {
                "name": "auth_user",
                "label": "Auth Username",
                "type": "text",
                "placeholder": "admin",
                "required": False,
                "group": "Advanced"
            },
            {
                "name": "auth_pass",
                "label": "Auth Password",
                "type": "password",
                "placeholder": "password",
                "required": False,
                "group": "Advanced"
            }
        ]
    
    def log(self, message: str):
        """Helper to log tool progress"""
        logger.info(f"[{self.metadata.name}] {message}")

    def export_json(self, filepath: str):
        """Export results to JSON"""
        try:
            name = self.metadata.name if self.metadata else "Unknown"
            version = self.metadata.version if self.metadata else "1.0.0"
            
            data = {
                'tool': name,
                'version': version,
                'timestamp': str(datetime.datetime.now()),
                'results': self.results or [],
                'errors': self.errors or [],
                'warnings': self.warnings or []
            }
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Results exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")

    def export_txt(self, filepath: str):
        """Export results to plain text"""
        try:
            name = self.metadata.name if self.metadata else "Unknown"
            version = self.metadata.version if self.metadata else "1.0.0"
            description = self.metadata.description if self.metadata else "No description"
            
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"=== {name} v{version} Report ===\n")
                f.write(f"Description: {description}\n\n")
                
                if self.results:
                    f.write("--- RESULTS ---\n")
                    for res in self.results:
                        f.write(f"{res}\n")
                
                if self.errors:
                    f.write("\n--- ERRORS ---\n")
                    for err in self.errors:
                        f.write(f"ERROR: {err}\n")
                
                if self.warnings:
                    f.write("\n--- WARNINGS ---\n")
                    for warn in self.warnings:
                        f.write(f"WARNING: {warn}\n")
                        
            logger.info(f"Results exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export TXT: {e}")
    
    def __repr__(self):
        return f"<{self.metadata.name} v{self.metadata.version}>"
