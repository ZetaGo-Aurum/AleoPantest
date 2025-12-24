"""Main CLI Application untuk AloPantest"""
import sys
import os
from pathlib import Path

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
except ImportError:
    print("Required packages not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

from alo_pantest.core.logger import logger
from alo_pantest.core.config import config

# Import all tools
from alo_pantest.modules.network import (
    PortScanner, PacketSniffer, PingTool, DNSLookup,
    TraceRoute, WhoisLookup, SSLChecker, IPScanner
)
from alo_pantest.modules.web import (
    SQLInjector, XSSDetector, CSRFDetector, WebCrawler,
    VulnerabilityScanner, SubdomainFinder
)
from alo_pantest.modules.osint import (
    EmailFinder, DomainInfo, IPGeolocation,
    MetadataExtractor, SearchEngineDorking
)
from alo_pantest.modules.utilities import (
    PasswordGenerator, HashTools, ProxyManager,
    URLEncoder, ReverseShellGenerator
)

console = Console()

# Tool registry
TOOLS_REGISTRY = {
    # Network Tools
    'port-scan': PortScanner,
    'sniffer': PacketSniffer,
    'ping': PingTool,
    'dns': DNSLookup,
    'traceroute': TraceRoute,
    'whois': WhoisLookup,
    'ssl-check': SSLChecker,
    'ip-scan': IPScanner,
    
    # Web Tools
    'sql-inject': SQLInjector,
    'xss-detect': XSSDetector,
    'csrf-detect': CSRFDetector,
    'crawler': WebCrawler,
    'vuln-scan': VulnerabilityScanner,
    'subdomain': SubdomainFinder,
    
    # OSINT Tools
    'email-find': EmailFinder,
    'domain-info': DomainInfo,
    'ip-geo': IPGeolocation,
    'metadata': MetadataExtractor,
    'dorking': SearchEngineDorking,
    
    # Utilities
    'passgen': PasswordGenerator,
    'hash': HashTools,
    'proxy': ProxyManager,
    'encode': URLEncoder,
    'revshell': ReverseShellGenerator,
}


def print_banner():
    """Print AloPantest banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  AloPantest - Penetration Testing Framework  🛡️   ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                     v1.0.0 (Educational)                     ║
║                                                               ║
║     350+ Tools • Multi-Platform • Rich CLI • Full Featured    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    rprint(banner)


def print_tools_table():
    """Print tools table"""
    table = Table(title="Available Tools", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Tool Name", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Description")
    
    for idx, (tool_id, tool_class) in enumerate(TOOLS_REGISTRY.items(), 1):
        instance = tool_class()
        table.add_row(
            str(idx),
            tool_id,
            instance.metadata.category.value,
            instance.metadata.description[:50] + "..."
        )
    
    console.print(table)


@click.group()
def cli():
    """AloPantest - Comprehensive Penetration Testing Framework"""
    pass


@cli.command()
def info():
    """Show tool information"""
    print_banner()
    console.print("\n[bold cyan]📊 Available Tools Statistics[/bold cyan]\n")
    
    categories = {}
    for tool_id, tool_class in TOOLS_REGISTRY.items():
        instance = tool_class()
        cat = instance.metadata.category.value
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        rprint(f"[green]✓[/green] {cat}: [bold]{count}[/bold] tools")
    
    rprint(f"\n[bold]Total Tools:[/bold] {len(TOOLS_REGISTRY)}")


@cli.command()
def list_tools():
    """List all available tools"""
    print_banner()
    print_tools_table()


@cli.command()
@click.argument('tool_id')
@click.option('--host', help='Target host/IP')
@click.option('--url', help='Target URL')
@click.option('--domain', help='Target domain')
@click.option('--port', type=int, help='Port number')
@click.option('--output', help='Output file path')
def run(tool_id, host, url, domain, port, output):
    """Run a specific tool"""
    
    print_banner()
    
    if tool_id not in TOOLS_REGISTRY:
        console.print(f"[red]❌ Tool '{tool_id}' not found[/red]")
        console.print(f"[yellow]Available tools: {', '.join(TOOLS_REGISTRY.keys())}[/yellow]")
        return
    
    console.print(f"[bold cyan]🚀 Running: {tool_id}[/bold cyan]\n")
    
    try:
        tool_class = TOOLS_REGISTRY[tool_id]
        tool = tool_class()
        
        # Prepare arguments
        kwargs = {}
        if host:
            kwargs['host'] = host
        if url:
            kwargs['url'] = url
        if domain:
            kwargs['domain'] = domain
        if port:
            kwargs['port'] = port
        
        # Run tool
        result = tool.run(**kwargs)
        
        if result:
            console.print(f"\n[bold green]✓ Execution completed successfully[/bold green]")
            console.print(f"\n[bold cyan]📊 Results:[/bold cyan]")
            
            # Pretty print results
            import json
            console.print_json(data=result)
            
            # Export if output specified
            if output:
                tool.export_json(output)
                console.print(f"\n[green]✓[/green] Results exported to [bold]{output}[/bold]")
        else:
            console.print(f"\n[red]❌ Tool execution failed[/red]")
            if tool.errors:
                console.print(f"\n[bold red]Errors:[/bold red]")
                for error in tool.errors:
                    console.print(f"  • {error}")
    
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        logger.exception("Tool execution error")


@cli.command()
@click.option('--port', type=int, default=5000, help='Server port')
def server(port):
    """Start HTTP API server (requires FastAPI)"""
    try:
        from alo_pantest.api.server import create_app
        app = create_app()
        
        console.print(f"\n[bold green]✓ Starting AloPantest API Server[/bold green]")
        console.print(f"[cyan]http://localhost:{port}[/cyan]\n")
        
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError:
        console.print("[red]FastAPI and Uvicorn required. Install with:[/red]")
        console.print("[yellow]pip install fastapi uvicorn[/yellow]")


@cli.command()
@click.argument('tool_id')
def help_tool(tool_id):
    """Get help for a specific tool"""
    
    if tool_id not in TOOLS_REGISTRY:
        console.print(f"[red]Tool '{tool_id}' not found[/red]")
        return
    
    tool_class = TOOLS_REGISTRY[tool_id]
    tool = tool_class()
    metadata = tool.metadata
    
    console.print(Panel(
        f"[bold]{metadata.name}[/bold]\nv{metadata.version} by {metadata.author}",
        title="Tool Information"
    ))
    
    console.print(f"\n[bold cyan]Description:[/bold cyan]\n{metadata.description}\n")
    console.print(f"[bold cyan]Usage:[/bold cyan]\n{metadata.usage}\n")
    console.print(f"[bold cyan]Category:[/bold cyan] {metadata.category.value}\n")
    console.print(f"[bold cyan]Tags:[/bold cyan] {', '.join(metadata.tags)}\n")
    console.print(f"[bold cyan]Requirements:[/bold cyan] {', '.join(metadata.requirements)}")


@cli.command()
def config_show():
    """Show current configuration"""
    console.print(Panel("Current Configuration", style="bold magenta"))
    
    from rich.syntax import Syntax
    import json
    
    config_json = json.dumps(config.to_dict(), indent=2)
    syntax = Syntax(config_json, "json", theme="monokai", line_numbers=True)
    console.print(syntax)


def main():
    """Main entry point"""
    if __name__ == '__main__':
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        Path('output').mkdir(exist_ok=True)
        
        cli()


if __name__ == '__main__':
    main()
