"""Base tool framework untuk semua tools"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import json
import socket
import getpass
import platform
import os
import time
import datetime
from pathlib import Path

from ..core.logger import logger
from ..core.platform import EnvironmentAdapter


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
        self.status = "idle" # idle, running, completed, failed
        self.is_running = False
        self.start_time = None
        
        # Core Parameters for v3.3
        self.timeout = 30
        self.headers = {
            "User-Agent": "Aleopantest/3.3.5",
            "Accept": "*/*"
        }
        self.auth = None
        self.proxy = None
        self.scan_options = {}

    @staticmethod
    def get_admin_info() -> Dict[str, str]:
        """Returns identification of the current admin/user with environment-aware detection"""
        admin_data = {
            "username": "admin",
            "hostname": "localhost",
            "os": platform.system(),
            "os_release": platform.release(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "env": EnvironmentAdapter.get_env()
        }
        
        try:
            # 1. Try environment variables first (most reliable for staging/prod)
            env_user = os.environ.get("ALEO_ADMIN_USER") or os.environ.get("USER") or os.environ.get("USERNAME")
            env_host = os.environ.get("ALEO_ADMIN_HOST") or os.environ.get("HOSTNAME") or os.environ.get("COMPUTERNAME")
            
            if env_user:
                admin_data["username"] = env_user
            else:
                # 2. Try getpass as fallback
                try:
                    admin_data["username"] = getpass.getuser()
                except:
                    pass
            
            if env_host:
                admin_data["hostname"] = env_host
            else:
                # 3. Try socket as fallback
                try:
                    admin_data["hostname"] = socket.gethostname()
                except:
                    pass
                    
            # 4. Final safety check - if still empty, use defaults
            if not admin_data["username"]: admin_data["username"] = "admin"
            if not admin_data["hostname"]: admin_data["hostname"] = "localhost"
            
        except Exception as e:
            logger.warning(f"Admin detection failed, using defaults: {e}")
            
        return admin_data

    def check_safety(self, duration_seconds: Any = 0) -> bool:
        """
        Safety check for high-risk tools.
        Enforces 1-hour limit for intensive tasks.
        
        Args:
            duration_seconds (int/str): Duration in seconds to check against safety limits.
            
        Returns:
            bool: True if safety check passes, False otherwise.
        """
        try:
            # Type validation and conversion
            if duration_seconds is None:
                duration = 0
            else:
                duration = int(duration_seconds)
                
            if duration < 0:
                self.add_error(f"Invalid Duration: Nilai durasi ({duration}s) tidak boleh negatif.")
                return False
                
        except (ValueError, TypeError):
            self.add_error(f"Type Error: Format durasi '{duration_seconds}' tidak valid. Harus berupa angka (integer).")
            return False

        if self.metadata and self.metadata.risk_level in ["HIGH", "CRITICAL"]:
            MAX_DURATION = 3600  # 1 hour
            if duration > MAX_DURATION:
                self.add_error(f"Safety Limit: Durasi eksekusi {duration}s melebihi batas maksimal 1 jam.")
                return False
            
            # Additional safety logic can be added here
            self.audit_log(f"Safety check passed for high-risk execution (Duration: {duration}s).")
            
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
        if result is not None:
            # If the result is a string, it's often a progress message, log it
            if isinstance(result, str):
                logger.info(f"[{self.metadata.name if self.metadata else 'Unknown'}] {result}")
            
            self.results.append(result)
            # If we have at least one valid result, status can be completed
            # even if there were some minor errors/warnings
            if self.status != "failed":
                self.status = "completed"

    def add_error(self, error: str):
        """Add error"""
        self.errors.append(error)
        # Only set to failed if we don't have results yet
        # If we have results, it might be a partial failure
        if not self.results:
            self.status = "failed"
        logger.error(f"[{self.metadata.name if self.metadata else 'Unknown'}] {error}")

    def add_warning(self, warning: str):
        """Add warning"""
        self.warnings.append(warning)
        logger.warning(f"[{self.metadata.name if self.metadata else 'Unknown'}] {warning}")

    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        return {
            "status": self.status,
            "results_count": len(self.results),
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "duration": (time.time() - self.start_time) if self.start_time else 0
        }
    
    def get_json_output(self) -> Dict[str, Any]:
        """
        Returns a standardized JSON output for all modules.
        Includes status, error messages, and detailed execution info.
        """
        summary = self.get_summary()
        return {
            "status": summary["status"],
            "tool_metadata": self.metadata.to_dict() if self.metadata else {},
            "results": self.results,
            "error_message": self.errors[0] if self.errors else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "execution_details": {
                "duration_seconds": round(summary["duration"], 2),
                "results_count": summary["results_count"],
                "errors_count": summary["errors_count"],
                "warnings_count": summary["warnings_count"],
                "timestamp": datetime.datetime.now().isoformat(),
                "admin_info": self.get_admin_info()
            }
        }

    def get_results(self) -> Any:
        """Get all results - defaults to returning standardized JSON output"""
        return self.get_json_output()
    
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
