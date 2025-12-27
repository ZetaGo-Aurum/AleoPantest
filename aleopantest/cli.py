"""Main CLI Application untuk Aleopantest V3.0.0 - by Aleocrophic"""
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

from aleopantest.core.logger import logger
from aleopantest.core.config import config
from aleopantest.core.interactive_handler import ParameterMapper
from aleopantest.core.session import SessionManager, SecurityGuard
from aleopantest.core.platform_detector import PlatformDetector

# Import all tools
from aleopantest.modules.network import (
    PortScanner, PacketSniffer, PingTool, DNSLookup,
    TraceRoute, WhoisLookup, SSLChecker, IPScanner, DDoSSimulator,
    MACLookup, NetSpeed, SubnetCalc, ArpScanner, VLANScanner
)
from aleopantest.modules.web import (
    SQLInjector, XSSDetector, CSRFDetector, WebCrawler,
    VulnerabilityScanner, SubdomainFinder, TechStack,
    DirBrute, LinkExtractor, AdminFinder, HeadersAnalyzer, ProxyFinder,
    APIAnalyzer
)
from aleopantest.modules.osint import (
    EmailFinder, DomainInfo, IPGeolocation,
    MetadataExtractor, SearchEngineDorking, UserSearch,
    GitRecon, WhoisHistory, ShodanSearch, PhoneLookup,
    MetadataExif, SocialAnalyzer, BreachChecker
)
from aleopantest.modules.utilities import (
    PasswordGenerator, HashTools, ProxyManager,
    URLEncoder, ReverseShellGenerator, URLMasking, URLShortener,
    Base64Tool, JSONFormatter, JWTDecoder, IPInfo, CronGen
)
from aleopantest.modules.utilities.test_complex_params import ComplexParamTester
from aleopantest.modules.phishing import (
    WebPhishing, EmailPhishing, PhishingLocator, PhishingImpersonation, NgrokPhishing
)
from aleopantest.modules.clickjacking import (
    ClickjackingChecker, ClickjackingMaker, AntiClickjackingGenerator
)
from aleopantest.modules.security import (
    AntiDDoS, WAFDetector, VulnDB, FirewallBypass, IDSEvasionHelper
)
from aleopantest.modules.crypto import (
    HashCracker, SteganoTool, RSAGen, VigenereCipher, HashGenerator, XORCipher
)
from aleopantest.modules.wireless import (
    BeaconFlood, DeauthTool, WifiScanner
)
from aleopantest.modules.database import (
    SQLBruteForcer, MongoDBAuditor
)
from aleopantest.modules.web import AdvancedDorking

import json
import requests
from datetime import datetime

console = Console()

def send_to_web_dashboard(tool_id, result):
    """Send tool execution results to the web dashboard if available"""
    try:
        # Default web server port is 8002
        url = "http://127.0.0.1:8002/aleopantest/api/report"
        data = {
            "tool_id": tool_id,
            "results": result,
            "source": "CLI",
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(url, json=data, timeout=2)
        if response.status_code == 200:
            return True
    except:
        # Silently fail if web server is not running
        pass
    return False

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
    'mac-lookup': MACLookup,
    'net-speed': NetSpeed,
    'subnet-calc': SubnetCalc,
    'arp-scan': ArpScanner,
    'vlan-scan': VLANScanner,
    
    # Web Tools
    'sql-inject': SQLInjector,
    'xss-detect': XSSDetector,
    'csrf-detect': CSRFDetector,
    'crawler': WebCrawler,
    'vuln-scan': VulnerabilityScanner,
    'subdomain': SubdomainFinder,
    'advanced-dorking': AdvancedDorking,
    'tech-stack': TechStack,
    'dir-brute': DirBrute,
    'link-extract': LinkExtractor,
    'admin-finder': AdminFinder,
    'headers-analyzer': HeadersAnalyzer,
    'proxy-finder': ProxyFinder,
    'api-analyzer': APIAnalyzer,
    
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
    'vuln-db': VulnDB,
    'firewall-bypass': FirewallBypass,
    'ids-evasion': IDSEvasionHelper,
    
    # OSINT Tools
    'email-find': EmailFinder,
    'domain-info': DomainInfo,
    'ip-geo': IPGeolocation,
    'metadata': MetadataExtractor,
    'dorking': SearchEngineDorking,
    'user-search': UserSearch,
    'git-recon': GitRecon,
    'whois-history': WhoisHistory,
    'shodan-search': ShodanSearch,
    'phone-lookup': PhoneLookup,
    'metadata-exif': MetadataExif,
    'social-analyzer': SocialAnalyzer,
    'breach-check': BreachChecker,
    
    # Utilities
    'passgen': PasswordGenerator,
    'hash': HashTools,
    'proxy': ProxyManager,
    'encode': URLEncoder,
    'revshell': ReverseShellGenerator,
    'url-mask': URLMasking,
    'url-shorten': URLShortener,
    'base64': Base64Tool,
    'json-format': JSONFormatter,
    'jwt-decoder': JWTDecoder,
    'ip-info': IPInfo,
    'cron-gen': CronGen,
    'complex-tester': ComplexParamTester,

    # Crypto Tools
    'hash-cracker': HashCracker,
    'stegano': SteganoTool,
    'rsa-gen': RSAGen,
    'vigenere': VigenereCipher,
    'hash-gen': HashGenerator,
    'xor-cipher': XORCipher,

    # Wireless Tools
    'beacon-flood': BeaconFlood,
    'deauth': DeauthTool,
    'wifi-scan': WifiScanner,

    # Database Tools
    'sql-brute': SQLBruteForcer,
    'mongodb-audit': MongoDBAuditor,
}

# Organize tools by category
TOOLS_BY_CATEGORY = {
    'Network': ['port-scan', 'ping', 'dns', 'traceroute', 'whois', 'ssl-check', 'ip-scan', 'sniffer', 'ddos-sim', 'mac-lookup', 'net-speed', 'subnet-calc', 'arp-scan', 'vlan-scan'],
    'Web': ['sql-inject', 'xss-detect', 'csrf-detect', 'crawler', 'vuln-scan', 'subdomain', 'advanced-dorking', 'tech-stack', 'dir-brute', 'link-extract', 'admin-finder', 'headers-analyzer', 'proxy-finder', 'api-analyzer'],
    'Phishing': ['web-phishing', 'email-phishing', 'phishing-locator', 'phishing-impersonation', 'ngrok-phishing'],
    'Clickjacking': ['clickjacking-check', 'clickjacking-make', 'anti-clickjacking'],
    'Security': ['anti-ddos', 'waf-detect', 'vuln-db', 'firewall-bypass', 'ids-evasion'],
    'OSINT': ['email-find', 'domain-info', 'ip-geo', 'metadata', 'dorking', 'user-search', 'git-recon', 'whois-history', 'shodan-search', 'phone-lookup', 'metadata-exif', 'social-analyzer', 'breach-check'],
    'Utilities': ['passgen', 'hash', 'proxy', 'encode', 'revshell', 'url-mask', 'url-shorten', 'base64', 'json-format', 'jwt-decoder', 'ip-info', 'cron-gen'],
    'Crypto': ['hash-cracker', 'stegano', 'rsa-gen', 'vigenere', 'hash-gen', 'xor-cipher'],
    'Wireless': ['beacon-flood', 'deauth', 'wifi-scan'],
    'Database': ['sql-brute', 'mongodb-audit'],
}


def print_banner():
    """Print Aleopantest banner"""
    platform_name = PlatformDetector.get_platform_name()
    banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🛡️  Aleopantest v{config.VERSION}  🛡️               ║
║                    by Aleocrophic                             ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║       400+ Tools • Multi-Platform • Modern TUI • V3.3.5 PRO   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    Platform: {platform_name}
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
    """Aleopantest v3.3.5 - by Aleocrophic - Comprehensive Penetration Testing Framework
    
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
    console.print(f"\n[bold cyan]📊 Aleopantest v{config.VERSION} Statistics[/bold cyan]\n")
    
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
def tui():
    """Launch the modern TUI dashboard"""
    from .tui import AleopantestTUI
    app = AleopantestTUI()
    app.run()


@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the web server')
@click.option('--port', default=8002, help='Port to bind the web server')
def web(host, port):
    """Launch the modern Web Dashboard"""
    try:
        from .core.web_server import start_web_server
        start_web_server(host=host, port=port)
    except (ImportError, ModuleNotFoundError) as e:
        console.print(f"[red]❌ Fatal Error: Missing dependency for Web Dashboard: {str(e)}[/red]")
        console.print("[yellow]💡 Tip: Run 'pip install -r requirements.txt' or 'pip install fastapi uvicorn' to fix this.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Fatal Error while starting Web Server: {str(e)}[/red]")
        logger.error(f"Fatal error in web command: {str(e)}", exc_info=True)


@cli.command()
@click.argument('tool_id')
@click.option('--host', help='Target host/IP (alias: --ip)')
@click.option('--ip', help='Target IP address (alias: --host)')
@click.option('--url', help='Target URL')
@click.option('--domain', help='Target domain')
@click.option('--port', type=int, help='Port number')
@click.option('--email', help='Email address')
@click.option('--subject', help='Email subject')
@click.option('--target', help='Target for attack')
@click.option('--type', help='Tool type/attack type')
@click.option('--duration', type=int, help='Duration in seconds')
@click.option('--threads', type=int, default=None, help='Number of threads')
@click.option('--preset', help='Preset configuration (for DDoS: light, medium, heavy)')
@click.option('--output', help='Output file path')
@click.option('--framework', help='Framework (for code generation)')
@click.option('--alias', help='Alias (for URL tools)')
@click.option('--fake-domain', help='Fake domain (for URL masking)')
@click.option('--method', help='Method type')
@click.option('--base-url', help='Base URL (for URL shortener)')
@click.option('--generate-qr', is_flag=True, help='Generate QR code')
@click.option('--tracking', help='Enable tracking')
@click.option('--test-payloads', is_flag=True, help='Test with payloads')
@click.option('--authorized', is_flag=True, help='Confirm authorization for sensitive operations (required for DDoS, etc.)')
@click.option('--query', help='Search query (for dorking tools)')
@click.option('--engine', help='Search engine (for dorking tools: google, duckduckgo, github, shodan)')
@click.option('--template', help='Dorking template (exposed_configs, admin_panels, backup_files, source_code, user_data)')
@click.option('--text', help='Text to hash or process (alias: --input)')
@click.option('--file-path', help='File path to hash or process')
@click.option('--algorithm', help='Hash algorithm (md5, sha1, sha256, sha512)')
@click.option('--interactive', is_flag=True, help='Use interactive mode to enter parameters')
@click.option('--serve', is_flag=True, help='Start a local server to handle redirects')
def run(tool_id, host, ip, url, domain, port, email, subject, target, type, duration, threads, preset, 
        output, framework, alias, fake_domain, method, base_url, generate_qr, tracking, test_payloads, authorized, query, engine, template, text, file_path, algorithm, interactive, serve):
    """Run a specific tool with optional interactive mode
    
EXAMPLES:
  Basic usage:
    aleopantest run dns --domain target.com
    aleopantest run ip-geo --ip 8.8.8.8
    aleopantest run ip-geo --host 1.1.1.1
    
  Interactive mode (prompts for parameters):
    aleopantest run ip-geo --interactive
    aleopantest run dns --interactive
    
  Advanced usage:
    aleopantest run url-mask --url https://attacker.com --fake-domain google.com --method redirect
    aleopantest run ddos-sim --target target.com --type http --duration 30 --authorized
    aleopantest run anti-clickjacking --framework nginx --output config.conf
    
PARAMETER ALIASES:
  --host and --ip are interchangeable (both set the target IP)
  
SAFETY FEATURES:
  - DDoS simulator requires --authorized flag for legal compliance
  - Parameters are automatically normalized and validated
  - Comprehensive error messages guide correct usage
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
    
    if tool_class is None:
        console.print(f"[red]❌ Tool '{tool_id}' exists but failed to load due to an internal error.[/red]")
        console.print(f"[yellow]💡 Tip: Check for syntax errors or missing dependencies in the tool module.[/yellow]")
        return

    try:
        tool = tool_class()
        if not tool:
            console.print(f"[red]❌ Error: Failed to instantiate tool '{tool_id}'.[/red]")
            return
            
        metadata = tool.metadata
        if not metadata:
            console.print(f"[red]❌ Error: Tool '{tool_id}' is missing metadata.[/red]")
            return
            
        console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
        console.print(f"[bold cyan]🛠️  {metadata.name} (v{metadata.version})[/bold cyan]")
        console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
        
        console.print(f"[yellow]📝 Description:[/yellow]\n{metadata.description}\n")
        
        console.print(f"[yellow]📚 Usage:[/yellow]\n{metadata.usage}\n")
        
        if metadata.risk_level and metadata.risk_level != "LOW":
            console.print(f"[bold red]⚠️  Risk Level: {metadata.risk_level}[/bold red]\n")
        
        if metadata.legal_disclaimer:
            console.print(f"[bold red]⚖️  Legal Disclaimer:[/bold red]\n{metadata.legal_disclaimer}\n")
        
        console.print(f"[yellow]🏷️  Tags:[/yellow] {', '.join(metadata.tags)}")
        console.print(f"[yellow]📦 Requirements:[/yellow] {', '.join(metadata.requirements)}\n")
        
        console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
        
    except Exception as e:
        console.print(f"[red]❌ Error loading metadata for tool '{tool_id}': {e}[/red]")
        return
    
    # Prepare arguments with parameter mapping
    kwargs = {}
    
    # Use parameter mapping to normalize inputs
    if host:
        kwargs['host'] = host
    if ip:
        kwargs['ip'] = ip
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
    if threads is not None:
        kwargs['threads'] = threads
    if preset:
        kwargs['preset'] = preset
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
    if authorized:
        kwargs['authorized'] = authorized
    if query:
        kwargs['query'] = query
    if engine:
        kwargs['engine'] = engine
    if template:
        kwargs['template'] = template
    if text:
        kwargs['text'] = text
    if file_path:
        kwargs['file_path'] = file_path
    if algorithm:
        kwargs['algorithm'] = algorithm
    if serve:
        kwargs['serve'] = serve
    
    # Normalize parameters using parameter mapper
    normalized_kwargs = ParameterMapper.normalize_params(kwargs)
    
    # If no arguments provided and not interactive, show hint
    if not any([host, ip, url, domain, port, email, subject, target, type, duration, threads, framework, alias, fake_domain, method, base_url, generate_qr, tracking, test_payloads, query, engine, template, text, file_path, algorithm, serve]):
        if interactive:
            console.print(f"[cyan]💡 Interactive mode enabled - please provide parameters below[/cyan]\n")
        else:
            console.print(f"[cyan]💡 Tip: Provide parameters to run this tool, or use --interactive mode[/cyan]\n")
            return
    
    console.print(f"[bold cyan]🚀 Running: {tool_id}[/bold cyan]\n")
    
    # Initialize session
    session = SessionManager()
    if not session.check_quota():
        console.print("[red]❌ Session quota reached (10 minutes max). Please restart.[/red]")
        return

    try:
        # Apply safety limits
        normalized_kwargs = SecurityGuard.enforce_limits(tool_id, normalized_kwargs)
        
        # Run tool with normalized parameters
        result = tool.run(**normalized_kwargs)
        
        if result:
            console.print(f"\n[bold green]✓ Execution completed successfully[/bold green]")
            console.print(f"\n[bold cyan]📊 Results:[/bold cyan]")
            
            # Pretty print results
            console.print_json(data=result)
            
            # Send to web dashboard if available
            if send_to_web_dashboard(tool_id, result):
                console.print(f"\n[dim green]ℹ Results also delivered to web dashboard[/dim green]")
            
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
            if tool.warnings:
                console.print(f"\n[bold yellow]Warnings:[/bold yellow]")
                for warning in tool.warnings:
                    console.print(f"  • {warning}")
    
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        logger.exception("Tool execution error")


@cli.command()
@click.option('--port', type=int, default=5000, help='Server port')
def server(port):
    """Start HTTP API server (requires FastAPI)"""
    try:
        from aleopantest.api.server import create_app
        app = create_app()
        
        console.print(f"\n[bold green]✓ Starting Aleopantest API Server[/bold green]")
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
