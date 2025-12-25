"""Interactive CLI handler for user-friendly tool interaction"""
import sys
from typing import Dict, Any, Optional, List, Callable, Tuple
from pathlib import Path

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.syntax import Syntax
except ImportError:
    Console = None
    Prompt = None

from ..core.logger import logger


class ParameterMapper:
    """Map parameter aliases to canonical names"""
    
    # Define parameter aliases for flexibility
    PARAMETER_ALIASES = {
        # IP/Host parameters
        'ip': ['host', 'address', 'target_ip'],
        'host': ['ip', 'address', 'target_ip'],
        'domain': ['target_domain', 'site'],
        'url': ['target_url', 'website'],
        'target': ['target_host', 'destination'],
        'port': ['target_port', 'listening_port'],
        'email': ['email_address', 'sender_email'],
        'duration': ['timeout', 'time_limit'],
        'threads': ['thread_count', 'workers', 'connections'],
        'type': ['attack_type', 'method', 'mode'],
        # Hash tool aliases
        'text': ['input', 'data', 'hash_input'],
        'algorithm': ['hash_type', 'method'],
        # Method parameter
        'method': ['attack_method', 'type', 'algorithm'],
    }
    
    @staticmethod
    def normalize_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize parameters by resolving aliases to canonical names"""
        normalized = {}
        processed_keys = set()
        
        # First pass: identify canonical parameters
        canonical_params = {}
        for key, value in params.items():
            if value is None:
                continue
                
            canonical = None
            # Check if this key is a canonical parameter
            if key in ParameterMapper.PARAMETER_ALIASES:
                canonical = key
            else:
                # Find which canonical parameter this is an alias for
                for canonical_key, aliases in ParameterMapper.PARAMETER_ALIASES.items():
                    if key in aliases:
                        canonical = canonical_key
                        break
            
            if canonical:
                if canonical not in processed_keys:
                    canonical_params[canonical] = value
                    processed_keys.add(canonical)
            else:
                # Keep unknown parameters as-is
                normalized[key] = value
        
        # Add canonical parameters
        normalized.update(canonical_params)
        return normalized
    
    @staticmethod
    def get_aliases(param_name: str) -> List[str]:
        """Get all aliases for a parameter"""
        if param_name in ParameterMapper.PARAMETER_ALIASES:
            return [param_name] + ParameterMapper.PARAMETER_ALIASES[param_name]
        
        for canonical, aliases in ParameterMapper.PARAMETER_ALIASES.items():
            if param_name in aliases:
                return [canonical] + aliases
        
        return [param_name]


class InteractivePrompt:
    """Interactive prompt handler for tool parameters"""
    
    def __init__(self, tool_name: str, tool_metadata: Any):
        self.tool_name = tool_name
        self.metadata = tool_metadata
        self.console = Console() if Console else None
    
    def prompt_for_parameters(self, required_params: List[str], 
                             param_hints: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Interactively prompt user for required parameters
        
        Args:
            required_params: List of required parameter names
            param_hints: Optional dict with parameter descriptions/examples
        
        Returns:
            Dictionary of parameter values
        """
        if not self.console:
            return {}
        
        result = {}
        param_hints = param_hints or {}
        
        self.console.print(f"\n[bold cyan]📋 {self.tool_name} - Parameter Setup[/bold cyan]\n")
        self.console.print(f"Please provide the following information:\n")
        
        for param in required_params:
            hint = param_hints.get(param, "")
            hint_text = f" ({hint})" if hint else ""
            
            # Prompt for the parameter
            value = Prompt.ask(f"[cyan]{param}[/cyan]{hint_text}")
            
            if value.strip():
                result[param] = value.strip()
            else:
                self.console.print(f"[yellow]⚠️  {param} cannot be empty[/yellow]")
                # Retry
                return self.prompt_for_parameters([param], {param: hint})
        
        return result
    
    def show_usage_help(self, examples: Optional[List[str]] = None,
                       usage_notes: Optional[str] = None):
        """Display usage help and examples"""
        if not self.console:
            return
        
        self.console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
        self.console.print(f"[bold cyan]🛠️  {self.metadata.name}[/bold cyan]")
        self.console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
        
        self.console.print(f"[yellow]📝 Description:[/yellow]\n{self.metadata.description}\n")
        
        if usage_notes:
            self.console.print(f"[yellow]📚 Usage Notes:[/yellow]\n{usage_notes}\n")
        
        if examples:
            self.console.print(f"[yellow]💡 Examples:[/yellow]")
            for example in examples:
                self.console.print(f"  • {example}")
            self.console.print()
        
        if self.metadata.risk_level and self.metadata.risk_level != "LOW":
            self.console.print(f"[bold red]⚠️  Risk Level: {self.metadata.risk_level}[/bold red]\n")
        
        if self.metadata.legal_disclaimer:
            self.console.print(f"[bold red]⚖️  Legal: {self.metadata.legal_disclaimer}[/bold red]\n")
    
    def confirm_action(self, message: str = "Proceed with this action?") -> bool:
        """Confirm user action with safety prompt"""
        if not self.console:
            return True
        
        return Confirm.ask(f"[yellow]{message}[/yellow]", default=False)


class SafeParameterHandler:
    """Handle parameter validation and transformation safely"""
    
    @staticmethod
    def validate_ip(ip_str: str) -> bool:
        """Validate IP address format"""
        parts = ip_str.strip().split('.')
        if len(parts) != 4:
            return False
        
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        
        return True
    
    @staticmethod
    def validate_url(url_str: str) -> bool:
        """Validate URL format"""
        url = url_str.strip()
        return url.startswith('http://') or url.startswith('https://')
    
    @staticmethod
    def validate_domain(domain_str: str) -> bool:
        """Validate domain format"""
        domain = domain_str.strip()
        # Basic domain validation
        if not domain or len(domain) < 3:
            return False
        if domain.count('.') < 1:
            return False
        return True
    
    @staticmethod
    def validate_port(port_val: Any) -> bool:
        """Validate port number"""
        try:
            port = int(port_val)
            return 1 <= port <= 65535
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_parameter(param_name: str, param_value: str) -> Tuple[bool, Optional[str]]:
        """
        Validate parameter value
        
        Returns:
            (is_valid, error_message)
        """
        if not param_value:
            return False, f"{param_name} cannot be empty"
        
        param_lower = param_name.lower()
        
        if 'ip' in param_lower or 'host' in param_lower:
            if not SafeParameterHandler.validate_ip(param_value):
                return False, f"Invalid IP address format: {param_value}"
        
        elif 'url' in param_lower or 'website' in param_lower:
            if not SafeParameterHandler.validate_url(param_value):
                return False, f"Invalid URL format. Must start with http:// or https://"
        
        elif 'domain' in param_lower or 'site' in param_lower:
            if not SafeParameterHandler.validate_domain(param_value):
                return False, f"Invalid domain format: {param_value}"
        
        elif 'port' in param_lower:
            if not SafeParameterHandler.validate_port(param_value):
                return False, f"Invalid port number. Must be between 1-65535"
        
        return True, None


class InteractiveCliBuilder:
    """Build complete interactive CLI flows"""
    
    @staticmethod
    def build_tool_runner(tool_id: str, tool_instance, tool_metadata, 
                         provided_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build an interactive tool execution flow
        
        Returns:
            Dictionary of parameters ready for tool.run()
        """
        from ..core.interactive_handler import ParameterMapper
        
        console = Console() if Console else None
        
        # Normalize provided parameters
        normalized = ParameterMapper.normalize_params(provided_params)
        
        # Show tool info
        if console:
            console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
            console.print(f"[bold cyan]🛠️  {tool_metadata.name} (v{tool_metadata.version})[/bold cyan]")
            console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
            console.print(f"[yellow]📝 Description:[/yellow]\n{tool_metadata.description}\n")
            console.print(f"[yellow]📚 Usage:[/yellow]\n{tool_metadata.usage}\n")
        
        # Filter out None values
        final_params = {k: v for k, v in normalized.items() if v is not None}
        
        return final_params


def create_parameter_hints() -> Dict[str, Dict[str, str]]:
    """Create parameter hints for different tool types"""
    return {
        'ip_geolocation': {
            'ip': 'e.g., 8.8.8.8, 1.1.1.1',
            'host': 'e.g., 8.8.8.8, 1.1.1.1',
        },
        'dns': {
            'domain': 'e.g., google.com, example.org',
        },
        'port_scan': {
            'host': 'e.g., 192.168.1.1 or google.com',
            'port': 'e.g., 80 or 80-443',
        },
        'web_phishing': {
            'url': 'e.g., http://example.com',
        },
        'ddos_sim': {
            'target': 'e.g., example.com (authorized only)',
            'type': 'http, dns, slowloris, syn, udp',
            'duration': 'seconds (max 120)',
            'threads': 'number of connections (max 50)',
        },
    }
