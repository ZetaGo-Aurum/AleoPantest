"""Interactive CLI module for user-friendly tool interaction"""
from typing import Dict, Any, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint

console = Console()

# Parameter aliases for different tools - maps CLI param names to tool param names
PARAMETER_ALIASES = {
    'ip-geo': {
        'host': 'ip',  # ip-geo expects 'ip' parameter
        'ip': 'ip'
    },
    'port-scan': {
        'host': 'host',
        'target': 'host',
        'ip': 'host',
        'port': 'port',
        'ports': 'port'
    },
    'dns': {
        'domain': 'domain',
        'host': 'domain',
        'url': 'domain'
    },
    'ddos-sim': {
        'target': 'target',
        'host': 'target',
        'url': 'target',
        'type': 'type',
        'duration': 'duration',
        'threads': 'threads',
        'preset': 'preset'
    },
    'sql-inject': {
        'url': 'url',
        'target': 'url',
        'host': 'url'
    },
    'dorking': {
        'query': 'query',
        'search': 'query',
        'keyword': 'query',
        'search-engine': 'engine',
        'engine': 'engine'
    }
}

def normalize_parameters(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize parameter names based on tool aliases
    Maps CLI parameter names to actual tool parameter names
    """
    if tool_id not in PARAMETER_ALIASES:
        return params
    
    aliases = PARAMETER_ALIASES[tool_id]
    normalized = {}
    
    for key, value in params.items():
        # Map parameter name through aliases
        actual_key = aliases.get(key, key)
        normalized[actual_key] = value
    
    return normalized

def prompt_for_parameters(tool_id: str, metadata: Any) -> Dict[str, Any]:
    """
    Interactively prompt user for required parameters based on tool type
    """
    console.print()
    console.print(f"[bold cyan]📋 Setup {metadata.name}[/bold cyan]")
    console.print(f"[cyan]{metadata.description}[/cyan]\n")
    
    params = {}
    
    # Show common examples
    if "Example:" in metadata.usage:
        examples = [line.strip() for line in metadata.usage.split('\n') if line.strip().startswith('aleopantest')]
        if examples:
            console.print("[yellow]💡 Common Usage Examples:[/yellow]")
            for i, example in enumerate(examples[:3], 1):
                console.print(f"  {i}. {example}")
            console.print()
    
    # Determine which parameters to ask for based on tool type
    if tool_id == 'ip-geo':
        ip = Prompt.ask("Enter target IP address", default="8.8.8.8")
        params['ip'] = ip
        
    elif tool_id == 'port-scan':
        host = Prompt.ask("Enter target host/IP")
        port = Prompt.ask("Enter port or port range", default="1-1000")
        params['host'] = host
        params['port'] = port
        params['threads'] = int(Prompt.ask("Number of threads", default="5"))
        
    elif tool_id == 'dns':
        domain = Prompt.ask("Enter domain to lookup")
        params['domain'] = domain
        
    elif tool_id == 'ddos-sim':
        target = Prompt.ask("Enter target URL/IP")
        params['target'] = target
        
        console.print("\n[yellow]Attack Types:[/yellow]")
        console.print("  1. http      - HTTP flood (Layer 7)")
        console.print("  2. dns       - DNS amplification")
        console.print("  3. slowloris - Slowloris attack")
        console.print("  4. syn       - SYN flood")
        console.print("  5. udp       - UDP flood")
        attack_type = Prompt.ask("Select attack type", choices=['http', 'dns', 'slowloris', 'syn', 'udp'], default='http')
        params['type'] = attack_type
        
        console.print("\n[yellow]Load Preset:[/yellow]")
        console.print("  1. light   - 10s, 5 threads (safe)")
        console.print("  2. medium  - 30s, 10 threads")
        console.print("  3. heavy   - 60s, 20 threads")
        preset = Prompt.ask("Select preset", choices=['light', 'medium', 'heavy'], default='light')
        params['preset'] = preset
        
        if Confirm.ask("\n⚠️  This is for AUTHORIZED testing only. Do you have written authorization?"):
            params['authorized'] = True
        else:
            console.print("[red]❌ Tool requires authorization. Aborting.[/red]")
            return {}
            
    elif tool_id == 'dorking':
        query = Prompt.ask("Enter search query/keyword")
        params['query'] = query
        
        console.print("\n[yellow]Search Engines:[/yellow]")
        console.print("  1. google   - Google search")
        console.print("  2. bing     - Bing search")
        console.print("  3. duckduck - DuckDuckGo")
        console.print("  4. yahoo    - Yahoo search")
        engine = Prompt.ask("Select search engine", choices=['google', 'bing', 'duckduck', 'yahoo'], default='google')
        params['engine'] = engine
        
    elif tool_id == 'sql-inject':
        url = Prompt.ask("Enter target URL")
        params['url'] = url
        params['test_payloads'] = Confirm.ask("Test with payloads?", default=True)
        
    elif tool_id == 'url-mask':
        real_url = Prompt.ask("Enter real/malicious URL")
        fake_domain = Prompt.ask("Enter fake domain", default="google.com")
        
        console.print("\n[yellow]Masking Methods:[/yellow]")
        console.print("  1. redirect     - Auto-redirect after 1s")
        console.print("  2. iframe       - Embed in iframe")
        console.print("  3. obfuscation  - Base64 + obfuscation")
        console.print("  4. encoding     - Multi-layer encoding")
        method = Prompt.ask("Select method", choices=['redirect', 'iframe', 'obfuscation', 'encoding'], default='redirect')
        
        params['url'] = real_url
        params['fake_domain'] = fake_domain
        params['method'] = method
        params['generate_qr'] = Confirm.ask("Generate QR code?", default=False)
        
    elif tool_id == 'url-shorten':
        url = Prompt.ask("Enter URL to shorten")
        alias = Prompt.ask("Enter custom alias (or leave blank for auto-generated)", default="")
        
        params['url'] = url
        if alias:
            params['alias'] = alias
        params['tracking'] = Confirm.ask("Enable click tracking?", default=True)
    
    else:
        # Generic parameter prompting
        console.print("[yellow]⚠️  Interactive mode not fully configured for this tool[/yellow]")
        console.print("[cyan]Please provide parameters directly:[/cyan]")
        console.print("[cyan]  Example: aleopantest run {tool_id} --param value[/cyan]\n")
        return {}
    
    return params

def show_tool_menu() -> Optional[str]:
    """Show interactive menu to select a tool"""
    from aleopantest.cli import TOOLS_BY_CATEGORY
    
    console.clear()
    console.print("[bold cyan]🛡️  Aleopantest - Interactive Tool Selector[/bold cyan]\n")
    
    all_tools = []
    option_num = 1
    
    for category, tools in TOOLS_BY_CATEGORY.items():
        console.print(f"[bold]{category}:[/bold]")
        for tool_id in tools:
            console.print(f"  [{option_num}] {tool_id}")
            all_tools.append(tool_id)
            option_num += 1
        console.print()
    
    choice = Prompt.ask("Select tool number", default="1")
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(all_tools):
            return all_tools[index]
    except (ValueError, IndexError):
        console.print("[red]Invalid selection[/red]")
        return None
    
    return None

def show_results(result: Dict[str, Any], tool_id: str):
    """Display tool results in a user-friendly format"""
    if not result:
        console.print("[red]❌ No results to display[/red]")
        return
    
    console.print("\n[bold green]✓ Results:[/bold green]")
    
    # Format based on tool type
    if tool_id == 'ip-geo' and 'location_info' in result:
        info = result['location_info']
        table = Table(title=f"IP Geolocation: {result['ip']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in info.items():
            if value and key not in ['ip', 'source']:
                table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(table)
    
    elif isinstance(result, dict):
        import json
        console.print_json(data=result)
    else:
        console.print(result)

