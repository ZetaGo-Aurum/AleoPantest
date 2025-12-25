"""Main CLI Application untuk AloPantest V2"""
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
    TraceRoute, WhoisLookup, SSLChecker, IPScanner, DDoSSimulator
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
    URLEncoder, ReverseShellGenerator, URLMasking, URLShortener
)
from alo_pantest.modules.phishing import (
    WebPhishing, EmailPhishing, PhishingLocator, PhishingImpersonation, NgrokPhishing
)
from alo_pantest.modules.clickjacking import (
    ClickjackingChecker, ClickjackingMaker, AntiClickjackingGenerator
)
from alo_pantest.modules.security import (
    AntiDDoS, WAFDetector
)
from alo_pantest.modules.web import AdvancedDorking

console = Console()

# Tool registry organized by category
TOOLS_REGISTRY = {
    # Network Tools
    'port-scan': PortScanner,
    'ping': PingTool,
    'dns': DNSLookup,
    'traceroute': TraceRoute,
    'whois': WhoisLookup,
    'ssl-check': SSLChecker,
    'ip-scan': IPScanner,
    'sniffer': PacketSniffer,
    'ddos-sim': DDoSSimulator,
    
    # Web Tools
    'sql-inject': SQLInjector,
    'xss-detect': XSSDetector,
    'csrf-detect': CSRFDetector,
    'crawler': WebCrawler,
    'vuln-scan': VulnerabilityScanner,
    'subdomain': SubdomainFinder,
    'advanced-dorking': AdvancedDorking,
    
    # Phishing Tools
    'web-phishing': WebPhishing,
    'email-phishing': EmailPhishing,
    'phishing-locator': PhishingLocator,
    'phishing-impersonation': PhishingImpersonation,
    'ngrok-phishing': NgrokPhishing,
    
    # Clickjacking Tools
    'clickjacking-check': ClickjackingChecker,
    'clickjacking-make': ClickjackingMaker,
    'anti-clickjacking': AntiClickjackingGenerator,
    
    # Security Tools
    'anti-ddos': AntiDDoS,
    'waf-detect': WAFDetector,
    
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
    'url-mask': URLMasking,
    'url-shorten': URLShortener,
}

# Organize tools by category
TOOLS_BY_CATEGORY = {
    'Network': ['port-scan', 'ping', 'dns', 'traceroute', 'whois', 'ssl-check', 'ip-scan', 'sniffer', 'ddos-sim'],
    'Web': ['sql-inject', 'xss-detect', 'csrf-detect', 'crawler', 'vuln-scan', 'subdomain', 'advanced-dorking'],
    'Phishing': ['web-phishing', 'email-phishing', 'phishing-locator', 'phishing-impersonation', 'ngrok-phishing'],
    'Clickjacking': ['clickjacking-check', 'clickjacking-make', 'anti-clickjacking'],
    'Security': ['anti-ddos', 'waf-detect'],
    'OSINT': ['email-find', 'domain-info', 'ip-geo', 'metadata', 'dorking'],
    'Utilities': ['passgen', 'hash', 'proxy', 'encode', 'revshell', 'url-mask', 'url-shorten'],
}


def print_banner():
    """Print AloPantest banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  AloPantest v2.0 - Penetration Testing  🛡️        ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║       400+ Tools • Multi-Platform • Rich CLI • Full Docs      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    rprint(banner)


def print_tools_table():
    """Print tools table organized by category"""
    table = Table(title="Available Tools by Category", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan", width=15)
    table.add_column("Tool ID", style="green")
    table.add_column("Description")
    
    for category, tools in TOOLS_BY_CATEGORY.items():
        for idx, tool_id in enumerate(tools):
            if tool_id in TOOLS_REGISTRY:
                instance = TOOLS_REGISTRY[tool_id]()
                desc = instance.metadata.description[:40] + "..."
                
                if idx == 0:
                    table.add_row(category, tool_id, desc)
                else:
                    table.add_row("", tool_id, desc)
    
    console.print(table)


@click.group()
def cli():
    """AloPantest v2.0 - Comprehensive Penetration Testing Framework
    
Usage Examples:
  aleopantest --help              Show all commands
  aleopantest list-tools          List all available tools
  aleopantest run dns --domain example.com              Run DNS lookup
  aleopantest run sql-inject --url http://example.com  Run SQL injection detection
  aleopantest run phishing-locator --domain example.com  Locate phishing variants
"""
    pass


@cli.command()
def info():
    """Show tool information and statistics"""
    print_banner()
    console.print("\n[bold cyan]📊 AloPantest v2.0 Statistics[/bold cyan]\n")
    
    categories = {}
    for tool_id, tool_class in TOOLS_REGISTRY.items():
        instance = tool_class()
        cat = instance.metadata.category.value
        categories[cat] = categories.get(cat, 0) + 1
    
    table = Table(title="Tools by Category", show_header=True, header_style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="green", justify="right")
    
    for cat in sorted(categories.keys()):
        table.add_row(cat, str(categories[cat]))
    
    console.print(table)
    rprint(f"\n[bold]Total Tools Available:[/bold] {len(TOOLS_REGISTRY)}")


@cli.command()
def list_tools():
    """List all available tools"""
    print_banner()
    print_tools_table()
    
    console.print("\n[bold cyan]💡 Usage Examples:[/bold cyan]")
    examples = [
        ("DNS Lookup", "aleopantest run dns --domain target.com"),
        ("SQL Injection Test", "aleopantest run sql-inject --url http://target.com"),
        ("Phishing Detection", "aleopantest run web-phishing --url http://phishing-site.com"),
        ("Clickjacking Check", "aleopantest run clickjacking-check --url http://target.com"),
        ("WAF Detection", "aleopantest run waf-detect --url http://target.com"),
        ("DDoS Simulation", "aleopantest run ddos-sim --target target.com --type http --duration 30"),
    ]
    
    for tool_name, example in examples:
        console.print(f"  {tool_name}: [yellow]{example}[/yellow]")


@cli.command()
@click.argument('tool_id')
@click.option('--host', help='Target host/IP')
@click.option('--url', help='Target URL')
@click.option('--domain', help='Target domain')
@click.option('--port', type=int, help='Port number')
@click.option('--email', help='Email address')
@click.option('--subject', help='Email subject')
@click.option('--target', help='Target for attack')
@click.option('--type', help='Tool type/attack type')
@click.option('--duration', type=int, help='Duration in seconds')
@click.option('--threads', type=int, default=5, help='Number of threads')
@click.option('--output', help='Output file path')
@click.option('--framework', help='Framework (for code generation)')
@click.option('--alias', help='Alias (for URL tools)')
@click.option('--fake-domain', help='Fake domain (for URL masking)')
@click.option('--method', help='Method type')
@click.option('--base-url', help='Base URL (for URL shortener)')
@click.option('--generate-qr', is_flag=True, help='Generate QR code')
@click.option('--tracking', help='Enable tracking')
@click.option('--test-payloads', is_flag=True, help='Test with payloads')
def run(tool_id, host, url, domain, port, email, subject, target, type, duration, threads, output, framework, alias, fake_domain, method, base_url, generate_qr, tracking, test_payloads):
    """Run a specific tool
    
Examples:
  aleopantest run dns --domain target.com
  aleopantest run web-phishing --url http://example.com
  aleopantest run url-mask --url https://attacker.com --fake-domain google.com --method redirect
  aleopantest run url-shorten --url https://example.com --alias mylink
  aleopantest run ddos-sim --target target.com --type http --duration 30
  aleopantest run anti-clickjacking --framework nginx --output config.conf
"""
    
    print_banner()
    
    if tool_id not in TOOLS_REGISTRY:
        console.print(f"[red]❌ Tool '{tool_id}' not found[/red]")
        console.print(f"\n[yellow]Available tools:[/yellow]")
        for category, tools in TOOLS_BY_CATEGORY.items():
            console.print(f"  [cyan]{category}:[/cyan] {', '.join(tools)}")
        return
    
    # Display tool metadata/help first
    tool_class = TOOLS_REGISTRY[tool_id]
    tool = tool_class()
    metadata = tool.metadata
    
    console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
    console.print(f"[bold cyan]🛠️  {metadata.name} (v{metadata.version})[/bold cyan]")
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
    
    console.print(f"[yellow]📝 Description:[/yellow] {metadata.description}\n")
    
    console.print(f"[yellow]📚 Usage:[/yellow]")
    console.print(metadata.usage)
    
    if metadata.risk_level and metadata.risk_level != "LOW":
        console.print(f"\n[bold red]⚠️  Risk Level: {metadata.risk_level}[/bold red]")
    
    if metadata.legal_disclaimer:
        console.print(f"[bold red]⚖️  Legal: {metadata.legal_disclaimer}[/bold red]")
    
    console.print(f"\n[yellow]🏷️  Tags:[/yellow] {', '.join(metadata.tags)}")
    console.print(f"[yellow]📦 Requirements:[/yellow] {', '.join(metadata.requirements)}\n")
    
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
    
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
    if email:
        kwargs['email'] = email
    if subject:
        kwargs['subject'] = subject
    if target:
        kwargs['target'] = target
    if type:
        kwargs['type'] = type
    if duration:
        kwargs['duration'] = duration
    if threads:
        kwargs['threads'] = threads
    if framework:
        kwargs['framework'] = framework
    if alias:
        kwargs['alias'] = alias
    if fake_domain:
        kwargs['fake_domain'] = fake_domain
    if method:
        kwargs['method'] = method
    if base_url:
        kwargs['base_url'] = base_url
    if generate_qr:
        kwargs['generate_qr'] = generate_qr
    if tracking:
        kwargs['tracking'] = tracking.lower() == 'true'
    if test_payloads:
        kwargs['test_payloads'] = test_payloads
    
    # If no arguments provided, just show help
    if not any([host, url, domain, port, email, subject, target, type, duration, framework, alias, fake_domain, method, base_url, generate_qr, tracking, test_payloads]):
        console.print(f"[cyan]💡 Tip: Provide parameters to run this tool, or check help above[/cyan]\n")
        return
    
    console.print(f"[bold cyan]🚀 Running: {tool_id}[/bold cyan]\n")
    
    try:
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
    """Get detailed help for a specific tool
    
Example: aleopantest help-tool dns
"""
    
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
@click.argument('category', default='all')
def list_by_category(category):
    """List tools by category"""
    print_banner()
    
    if category.lower() == 'all':
        print_tools_table()
    elif category.title() in TOOLS_BY_CATEGORY:
        table = Table(title=f"{category.title()} Tools", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Description")
        
        for tool_id in TOOLS_BY_CATEGORY[category.title()]:
            instance = TOOLS_REGISTRY[tool_id]()
            table.add_row(tool_id, instance.metadata.description[:50] + "...")
        
        console.print(table)
    else:
        console.print(f"[red]Category '{category}' not found[/red]")
        console.print(f"\n[yellow]Available categories:[/yellow]")
        for cat in sorted(TOOLS_BY_CATEGORY.keys()):
            console.print(f"  • {cat}")


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
    if len(sys.argv) == 1:
        print_banner()
        console.print("\n[bold cyan]Quick Start:[/bold cyan]")
        console.print("  aleopantest list-tools       List all tools")
        console.print("  aleopantest info              Show statistics")
        console.print("  aleopantest run dns --domain example.com")
        console.print("  aleopantest --help            Show all commands\n")
    
    try:
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        Path('output').mkdir(exist_ok=True)
        
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Operation interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")
        logger.exception("Fatal error in CLI")
        sys.exit(1)


if __name__ == '__main__':
    main()
