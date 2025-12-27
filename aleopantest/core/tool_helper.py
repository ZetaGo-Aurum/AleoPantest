"""Utility functions for tool parameter handling and validation"""
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path

from ..core.logger import logger


class ToolParameterValidator:
    """Central validator for tool parameters"""
    
    @staticmethod
    def validate_ip(ip_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validate IP address format
        
        Returns:
            (is_valid, error_message)
        """
        if not ip_str:
            return False, "IP address cannot be empty"
        
        parts = ip_str.strip().split('.')
        if len(parts) != 4:
            return False, f"Invalid IP format: {ip_str} (expected 4 octets, got {len(parts)})"
        
        for i, part in enumerate(parts):
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False, f"Invalid IP octet at position {i+1}: {part} (must be 0-255)"
            except ValueError:
                return False, f"Invalid IP octet at position {i+1}: {part} (not a number)"
        
        return True, None
    
    @staticmethod
    def validate_url(url_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL format
        
        Returns:
            (is_valid, error_message)
        """
        if not url_str:
            return False, "URL cannot be empty"
        
        url = url_str.strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            return False, "URL must start with http:// or https://"
        
        if len(url) < 10:
            return False, "URL too short"
        
        return True, None
    
    @staticmethod
    def validate_domain(domain_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validate domain name format
        
        Returns:
            (is_valid, error_message)
        """
        if not domain_str:
            return False, "Domain cannot be empty"
        
        domain = domain_str.strip()
        
        if len(domain) < 3:
            return False, "Domain too short (minimum 3 characters)"
        
        if domain.count('.') < 1:
            return False, "Invalid domain format (must contain at least one dot)"
        
        # Check for valid characters
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
        if not all(c in valid_chars for c in domain):
            return False, "Domain contains invalid characters"
        
        return True, None
    
    @staticmethod
    def validate_port(port_val: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate port number
        
        Returns:
            (is_valid, error_message)
        """
        try:
            port = int(port_val)
            if port < 1 or port > 65535:
                return False, f"Port must be between 1 and 65535, got {port}"
            return True, None
        except (ValueError, TypeError):
            return False, f"Invalid port number: {port_val} (must be an integer)"
    
    @staticmethod
    def validate_duration(duration_val: Any, max_duration: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate duration in seconds
        
        Returns:
            (is_valid, error_message)
        """
        try:
            duration = int(duration_val)
            if duration < 1:
                return False, "Duration must be at least 1 second"
            if max_duration and duration > max_duration:
                return False, f"Duration exceeds maximum of {max_duration} seconds"
            return True, None
        except (ValueError, TypeError):
            return False, f"Invalid duration: {duration_val} (must be an integer)"
    
    @staticmethod
    def validate_threads(threads_val: Any, max_threads: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate thread count
        
        Returns:
            (is_valid, error_message)
        """
        try:
            threads = int(threads_val)
            if threads < 1:
                return False, "Thread count must be at least 1"
            if max_threads and threads > max_threads:
                return False, f"Thread count exceeds maximum of {max_threads}"
            return True, None
        except (ValueError, TypeError):
            return False, f"Invalid thread count: {threads_val} (must be an integer)"
    
    @staticmethod
    def validate_parameter(param_name: str, param_value: str, 
                          strict: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Generic parameter validation based on parameter name
        
        Args:
            param_name: Name of the parameter
            param_value: Value to validate
            strict: If True, be more strict about validation
        
        Returns:
            (is_valid, error_message)
        """
        if not param_value:
            return False, f"{param_name} cannot be empty"
        
        param_lower = param_name.lower()
        
        # IP/Host validation
        if any(x in param_lower for x in ['ip', 'host', 'address', 'server']):
            return ToolParameterValidator.validate_ip(param_value)
        
        # URL validation
        elif any(x in param_lower for x in ['url', 'website', 'link']):
            return ToolParameterValidator.validate_url(param_value)
        
        # Domain validation
        elif any(x in param_lower for x in ['domain', 'site']):
            return ToolParameterValidator.validate_domain(param_value)
        
        # Port validation
        elif 'port' in param_lower:
            return ToolParameterValidator.validate_port(param_value)
        
        return True, None


def robust_import(module_path: str, class_name: str):
    """
    Robustly import a tool class from a module.
    Prevents one bad module from crashing the entire system.
    """
    try:
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    except Exception as e:
        logger.error(f"FATAL: System Error while loading {class_name} from {module_path}: {str(e)}")
        return None
