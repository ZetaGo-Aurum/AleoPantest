# AloPantest v2.0 - Comprehensive Penetration Testing Framework

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  AloPantest v2.0 - Penetration Testing  🛡️        ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║       400+ Tools • Multi-Platform • Rich CLI • Full Docs      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 📋 Navigation

- [Installation Guide](INSTALL_GUIDE.md)
- [Quick Start Guide](QUICKSTART.md)
- [Tools Documentation](docs/TOOLS.md)
- [Changelog](CHANGELOG.md)
- [Feature Checklist](FEATURE_CHECKLIST.md)
- [Installation Instructions](#installation)
- [Usage Examples](#usage-examples)

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- pip package manager

### Standard Installation

```bash
# Clone or download AloPantest
cd AloPantest

# Install dependencies
pip install -r requirements.txt

# Install as command-line tool
pip install -e .
```

### Verification
```bash
# Test installation
aleopantest --help
aleopantest info
aleopantest list-tools
```

## ⚡ Quick Start

### Show Help
```bash
aleopantest --help
aleopantest list-tools
aleopantest info
```

### Run a Tool
```bash
# DNS Lookup
aleopantest run dns --domain target.com

# SQL Injection Detection
aleopantest run sql-inject --url http://target.com

# Phishing Detection
aleopantest run web-phishing --url http://phishing-site.com

# Clickjacking Check
aleopantest run clickjacking-check --url http://target.com

# DDoS Simulation
aleopantest run ddos-sim --target target.com --type http --duration 30
```

### Get Tool Help
```bash
aleopantest help-tool dns
aleopantest help-tool web-phishing
aleopantest help-tool clickjacking-check
```

## 🎉 New Features in v2.0

### 🎣 Phishing Tools (4 New Tools)
- **Web Phishing Detector** - Detects phishing websites and suspicious URLs
- **Email Phishing Detector** - Analyzes emails for phishing indicators
- **Phishing Locator** - Finds phishing domains mimicking your target
- **Phishing Impersonation Generator** - Creates educational phishing templates

#### Examples:
```bash
# Detect phishing website
aleopantest run web-phishing --url http://suspicious-site.com

# Analyze email for phishing
aleopantest run email-phishing --email attacker@fake-bank.com --subject "Verify Account"

# Find phishing domains
aleopantest run phishing-locator --domain example.com

# Generate phishing template (educational)
aleopantest run phishing-impersonation --type email --target bank
```

### 🖱️ Clickjacking Tools (3 New Tools)
- **Clickjacking Checker** - Detects clickjacking vulnerabilities
- **Clickjacking PoC Maker** - Creates clickjacking proof of concept
- **Anti-Clickjacking Generator** - Generates protection code/headers

#### Examples:
```bash
# Check for clickjacking vulnerability
aleopantest run clickjacking-check --url http://target.com

# Create clickjacking PoC
aleopantest run clickjacking-make --url http://target.com

# Generate protection headers
aleopantest run anti-clickjacking --framework nginx --output config.conf
```

### 🛡️ Security Tools (2 New Tools)
- **Anti-DDoS Detector** - Detects DDoS protection mechanisms (Cloudflare, Akamai, etc)
- **WAF Detector** - Identifies Web Application Firewalls

#### Examples:
```bash
# Detect DDoS protection
aleopantest run anti-ddos --url http://target.com

# Detect WAF
aleopantest run waf-detect --url http://target.com
```

### 🔗 Network Tools - DDoS Simulator
- **DDoS Simulator** - Educational DDoS attack simulator (HTTP, DNS, Slowloris)

#### Examples:
```bash
# Simulate HTTP flood
aleopantest run ddos-sim --target target.com --type http --duration 30 --threads 10

# Simulate DNS flood
aleopantest run ddos-sim --target target.com --type dns --duration 30

# Simulate Slowloris
aleopantest run ddos-sim --target target.com --type slowloris --duration 30
```

## 📚 Available Tools

### Network Tools (9)
- port-scan, ping, dns, traceroute, whois, ssl-check, ip-scan, sniffer, **ddos-sim**

### Web Tools (6)
- sql-inject, xss-detect, csrf-detect, crawler, vuln-scan, subdomain

### Phishing Tools (4) - NEW
- **web-phishing**, **email-phishing**, **phishing-locator**, **phishing-impersonation**

### Clickjacking Tools (3) - NEW
- **clickjacking-check**, **clickjacking-make**, **anti-clickjacking**

### Security Tools (2) - NEW
- **anti-ddos**, **waf-detect**

### OSINT Tools (5)
- email-find, domain-info, ip-geo, metadata, dorking

### Utilities (5)
- passgen, hash, proxy, encode, revshell

**Total: 400+ integrated tools and functions**

## 💻 Usage Examples

### Example 1: Complete Website Security Assessment

```bash
# Step 1: Check for clickjacking vulnerability
aleopantest run clickjacking-check --url http://target.com

# Step 2: Detect WAF
aleopantest run waf-detect --url http://target.com

# Step 3: Check for DDoS protection
aleopantest run anti-ddos --url http://target.com

# Step 4: Check for phishing characteristics
aleopantest run web-phishing --url http://target.com
```

### Example 2: Phishing Campaign Analysis

```bash
# Analyze suspected phishing email
aleopantest run email-phishing --email "noreply@bankofworld.com" --subject "Verify Your Account Now"

# Check for phishing domain variants
aleopantest run phishing-locator --domain bank.com

# Generate phishing awareness template (for training)
aleopantest run phishing-impersonation --type email --target bank
```

### Example 3: DDoS Impact Assessment (Authorized Testing Only)

```bash
# Simulate attack and assess defenses
aleopantest run ddos-sim --target target.com --type http --duration 60 --threads 20
```

## 🛠️ Command Reference

### Main Commands

```bash
aleopantest --help              # Show all commands
aleopantest info                # Show tool statistics
aleopantest list-tools          # List all tools
aleopantest list-by-category [category]  # List tools by category
```

### Run Tool

```bash
aleopantest run <tool-id> [options]

Common Options:
  --url <URL>          Target URL (web tools)
  --domain <DOMAIN>    Target domain
  --host <HOST>        Target host/IP
  --port <PORT>        Port number
  --email <EMAIL>      Email address
  --subject <SUBJECT>  Email subject
  --target <TARGET>    Attack target
  --type <TYPE>        Tool type
  --duration <SEC>     Duration in seconds
  --threads <NUM>      Number of threads
  --framework <FW>     Framework (nginx, apache, nodejs, python)
  --output <FILE>      Output file path
  --test-payloads      Test with attack payloads
```

### Get Help

```bash
aleopantest help-tool <tool-id>  # Detailed help for specific tool
```

## 🔒 Security & Ethics

### Important Notes
- ⚠️ **Authorization Required**: Only use on systems you own or have explicit written permission
- 🎓 **Educational Purpose**: Learn cybersecurity through authorized testing
- ⚖️ **Legal Compliance**: Follow laws and regulations in your jurisdiction
- 📋 **Documentation**: Always document authorization and testing procedures

### Responsible Use
- Get written authorization before testing
- Only test on designated test environments
- Report findings through proper channels
- Never use for malicious purposes
- Follow bug bounty program rules if applicable

## 📊 Output & Results

Results are displayed in rich formatted output and can be exported:

```bash
# Export results to JSON
aleopantest run dns --domain target.com --output results.json

# Results saved to: output/results.json
```

## 🐛 Troubleshooting

### Command Not Found
```bash
# Ensure package is installed
pip install -e .

# Verify installation
aleopantest --version
```

### Dependencies Missing
```bash
# Reinstall requirements
pip install -r requirements.txt

# Update pip
pip install --upgrade pip
```

### Permission Issues
- Run as administrator if needed
- Ensure output directory is writable
- Check file permissions in ./output directory

## 📖 Documentation

- `QUICKSTART.md` - Quick start guide
- `INSTALLATION.md` - Detailed installation
- `docs/TOOLS.md` - Complete tool documentation

## 🔄 Version History

### v2.0 (Current)
- ✨ Added Phishing Detection Tools (4)
- ✨ Added Clickjacking Tools (3)
- ✨ Added Security Tools (2)
- ✨ Added DDoS Simulator
- 🎯 Updated CLI with better help and examples
- 📦 Improved package management
- 📚 Enhanced documentation

### v1.0
- Initial release with 350+ tools
- Network, Web, OSINT, Utilities

## 🤝 Contributing

Contributions are welcome! Please:
1. Follow ethical hacking principles
2. Add tests for new tools
3. Update documentation
4. Submit pull requests

## 📜 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This framework is provided for **educational and authorized security testing purposes only**. Users are responsible for ensuring their use complies with all applicable laws and regulations. Unauthorized access to computer systems is illegal.

---

**Stay ethical. Stay legal. Learn security responsibly.**

🛡️ AloPantest Team
