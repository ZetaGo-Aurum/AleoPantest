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
        
        # Default: accept if not empty
        return True, None


class ToolParameterHelper:
    """Helper for tool parameter handling"""
    
    # Define required parameters for common tools
    TOOL_REQUIRED_PARAMS = {
        'ip-geo': ['ip', 'host'],  # Either one required
        'dns': ['domain'],
        'port-scan': ['host'],
        'web-phishing': ['url'],
        'email-phishing': ['email', 'subject'],
        'ddos-sim': ['target', 'type'],
        'url-mask': ['url', 'fake_domain', 'method'],
        'url-shorten': ['url'],
        'sql-inject': ['url'],
        'xss-detect': ['url'],
    }
    
    TOOL_PARAM_HINTS = {
        'ip-geo': {
            'ip': 'Enter IP address (e.g., 8.8.8.8)',
            'host': 'Enter IP address (e.g., 1.1.1.1)',
        },
        'dns': {
            'domain': 'Enter domain name (e.g., google.com)',
        },
        'port-scan': {
            'host': 'Enter host/domain (e.g., target.com or 192.168.1.1)',
            'port': 'Enter port or range (e.g., 80 or 80-443)',
        },
        'web-phishing': {
            'url': 'Enter URL to test (e.g., http://example.com)',
        },
        'ddos-sim': {
            'target': 'Enter target domain/IP (authorized only)',
            'type': 'Enter attack type: http, dns, slowloris, syn, udp',
            'duration': 'Enter duration in seconds (1-120)',
            'threads': 'Enter number of threads (1-50)',
        },
        'url-mask': {
            'url': 'Enter original URL (e.g., https://attacker.com)',
            'fake_domain': 'Enter fake domain (e.g., google.com)',
            'method': 'Enter method: redirect, iframe, meta',
        },
    }
    
    @staticmethod
    def get_required_params(tool_id: str) -> List[str]:
        """Get required parameters for a tool"""
        return ToolParameterHelper.TOOL_REQUIRED_PARAMS.get(tool_id, [])
    
    @staticmethod
    def get_param_hints(tool_id: str) -> Dict[str, str]:
        """Get parameter hints for a tool"""
        return ToolParameterHelper.TOOL_PARAM_HINTS.get(tool_id, {})
    
    @staticmethod
    def get_param_hint(tool_id: str, param_name: str) -> str:
        """Get hint for a specific parameter"""
        hints = ToolParameterHelper.get_param_hints(tool_id)
        return hints.get(param_name, "")
    
    @staticmethod
    def filter_none_values(params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values from parameters"""
        return {k: v for k, v in params.items() if v is not None}
    
    @staticmethod
    def prepare_tool_kwargs(provided_params: Dict[str, Any], 
                           allowed_params: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Prepare kwargs for tool.run()
        
        Args:
            provided_params: Raw parameters from CLI
            allowed_params: List of allowed parameters (if None, all accepted)
        
        Returns:
            Cleaned parameters ready for tool.run()
        """
        # Filter None values
        filtered = ToolParameterHelper.filter_none_values(provided_params)
        
        # Filter by allowed params if specified
        if allowed_params:
            filtered = {k: v for k, v in filtered.items() if k in allowed_params}
        
        return filtered


class ToolOutputFormatter:
    """Format and export tool output"""
    
    @staticmethod
    def format_json(data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        import json
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def export_to_file(data: Dict[str, Any], filepath: str, format: str = 'json') -> bool:
        """
        Export data to file
        
        Args:
            data: Data to export
            filepath: Output file path
            format: Output format (json, txt)
        
        Returns:
            True if successful
        """
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            if format == 'json':
                import json
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            elif format == 'txt':
                with open(filepath, 'w') as f:
                    f.write(str(data))
            
            logger.info(f"Results exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
            return False
