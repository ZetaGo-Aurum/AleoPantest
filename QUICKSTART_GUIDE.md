# Aleocrophic Quick Start Guide

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# View main help
Aleocrophic --help

# View all tools
Aleocrophic list-tools

# Get statistics
Aleocrophic info
```

## Common Commands

### OSINT Tools

#### IP Geolocation
```bash
# Get IP location (geolocation & ISP info)
Aleocrophic run ip-geo --ip 8.8.8.8
Aleocrophic run ip-geo --host 1.1.1.1
```

#### Domain Information
```bash
# Get domain information
Aleocrophic run domain-info --domain google.com
```

#### Email Finder
```bash
# Find email addresses from domain
Aleocrophic run email-find --domain example.com
```

### Network Tools

#### DNS Lookup
```bash
# Perform DNS lookup
Aleocrophic run dns --domain target.com
```

#### Port Scanning
```bash
# Scan for open ports
Aleocrophic run port-scan --host 192.168.1.1
Aleocrophic run port-scan --host target.com
```

#### SSL Certificate Check
```bash
# Check SSL certificate
Aleocrophic run ssl-check --domain https://example.com
```

#### Ping
```bash
# Ping a host
Aleocrophic run ping --host 8.8.8.8
```

#### Traceroute
```bash
# Trace route to host
Aleocrophic run traceroute --host 8.8.8.8
```

#### WHOIS Lookup
```bash
# Get WHOIS information
Aleocrophic run whois --domain example.com
```

### Web Vulnerability Tools

#### SQL Injection Detection
```bash
# Test for SQL injection vulnerabilities
Aleocrophic run sql-inject --url http://example.com
```

#### XSS Detection
```bash
# Test for cross-site scripting
Aleocrophic run xss-detect --url http://example.com
```

#### CSRF Detection
```bash
# Test for CSRF vulnerabilities
Aleocrophic run csrf-detect --url http://example.com
```

#### Web Crawler
```bash
# Crawl website structure
Aleocrophic run crawler --url http://example.com
```

#### Vulnerability Scanner
```bash
# Scan for vulnerabilities
Aleocrophic run vuln-scan --url http://example.com
```

#### Subdomain Finder
```bash
# Find subdomains
Aleocrophic run subdomain --domain example.com
```

### Security Tools

#### WAF Detection
```bash
# Detect Web Application Firewall
Aleocrophic run waf-detect --url http://example.com
```

#### Anti-DDoS Check
```bash
# Check anti-DDoS protection
Aleocrophic run anti-ddos --url http://example.com
```

#### Clickjacking Check
```bash
# Test for clickjacking vulnerability
Aleocrophic run clickjacking-check --url http://example.com
```

### Phishing Tools

#### Web Phishing Detection
```bash
# Detect phishing websites
Aleocrophic run web-phishing --url http://suspicious-site.com
```

#### Email Phishing
```bash
# Simulate email phishing (authorized only)
Aleocrophic run email-phishing --email target@example.com --subject "Important Update"
```

#### Phishing Locator
```bash
# Find phishing variants of domain
Aleocrophic run phishing-locator --domain example.com
```

### Clickjacking Tools

#### Generate Anti-Clickjacking Config
```bash
# Generate anti-clickjacking headers (nginx)
Aleocrophic run anti-clickjacking --framework nginx --output config.conf

# Generate anti-clickjacking headers (apache)
Aleocrophic run anti-clickjacking --framework apache --output config.conf
```

#### Clickjacking Maker
```bash
# Create clickjacking test page
Aleocrophic run clickjacking-make --url http://example.com
```

### Utility Tools

#### Password Generator
```bash
# Generate random password
Aleocrophic run passgen
```

#### Hash Tools
```bash
# Hash generation and cracking
Aleocrophic run hash --type md5 --input "password"
```

#### URL Encoder
```bash
# Encode URLs
Aleocrophic run encode --url "http://example.com?param=value"
```

#### URL Masking
```bash
# Mask URL appearance
Aleocrophic run url-mask --url https://attacker.com --fake-domain google.com --method redirect
```

#### URL Shortener
```bash
# Create short URL
Aleocrophic run url-shorten --url https://very-long-url.example.com --alias mylink
```

#### Reverse Shell Generator
```bash
# Generate reverse shell code
Aleocrophic run revshell --type bash
```

### Advanced Tools

#### DDoS Simulator (AUTHORIZED TESTING ONLY)
```bash
# Light DDoS simulation (10s, 5 threads)
Aleocrophic run ddos-sim --target example.com --type http --preset light --authorized

# Medium DDoS simulation (30s, 10 threads)
Aleocrophic run ddos-sim --target example.com --type http --preset medium --authorized

# Heavy DDoS simulation (60s, 20 threads)
Aleocrophic run ddos-sim --target example.com --type http --preset heavy --authorized

# Custom duration and threads
Aleocrophic run ddos-sim --target example.com --type dns --duration 45 --threads 15 --authorized

# Different attack types
Aleocrophic run ddos-sim --target example.com --type slowloris --preset light --authorized
Aleocrophic run ddos-sim --target example.com --type syn --preset medium --authorized
```

#### Metadata Extractor
```bash
# Extract metadata from files
Aleocrophic run metadata --file document.pdf
```

#### Search Engine Dorking
```bash
# Perform Google dorking
Aleocrophic run dorking --domain example.com
```

## Output Options

### Save Results to JSON
```bash
# Export results to JSON file
Aleocrophic run dns --domain example.com --output results.json
Aleocrophic run ip-geo --ip 8.8.8.8 --output location.json
```

### Generate Reports
```bash
# Tools support exporting to various formats
Aleocrophic run port-scan --host target.com --output scan_results.json
Aleocrophic run vuln-scan --url http://example.com --output vulnerabilities.json
```

## Help & Documentation

```bash
# Get general help
Aleocrophic --help

# Get command-specific help
Aleocrophic run --help

# Get tool-specific help
Aleocrophic help-tool dns
Aleocrophic help-tool ip-geo
Aleocrophic help-tool ddos-sim

# List tools by category
Aleocrophic list-by-category network
Aleocrophic list-by-category osint
Aleocrophic list-by-category web
Aleocrophic list-by-category phishing

# View current configuration
Aleocrophic config-show
```

## Advanced Usage

### Interactive Mode
```bash
# Launch interactive parameter entry (future feature)
Aleocrophic run dns --interactive
Aleocrophic run ip-geo --interactive
```

### Batch Operations
```bash
# Test multiple domains
Aleocrophic run dns --domain example.com --output example.json
Aleocrophic run dns --domain google.com --output google.json
```

### Chaining Tools
```bash
# Find subdomains then scan them
Aleocrophic run subdomain --domain example.com --output subdomains.json
# Then use those subdomains in other tools
Aleocrophic run port-scan --host sub1.example.com
Aleocrophic run port-scan --host sub2.example.com
```

## Parameter Aliases

### IP/Host Parameters
```bash
# All these are equivalent:
Aleocrophic run ip-geo --ip 8.8.8.8
Aleocrophic run ip-geo --host 8.8.8.8
Aleocrophic run ip-geo --address 8.8.8.8
```

### URL Parameters
```bash
# All these may work for web tools:
--url http://example.com
--website http://example.com
--target-url http://example.com
```

## Important Notes

### Authorization Required
Some tools require explicit authorization:
```bash
# DDoS Simulator MUST include --authorized flag
Aleocrophic run ddos-sim --target example.com --type http --preset light --authorized
```

### Legal Disclaimer
- Only test systems you own or have explicit written permission to test
- Unauthorized attacks are illegal in most jurisdictions
- Document all testing and authorization
- Contact your ISP before large-scale testing

### Safety Limits
- DDoS Simulator: Max 2 minutes, 50 threads
- All parameters validated before execution
- Clear error messages guide correct usage

## Troubleshooting

### "Tool not found"
```bash
# Check available tools
Aleocrophic list-tools

# Or check by category
Aleocrophic list-by-category network
```

### "Missing required parameter"
```bash
# Check what parameters are needed
Aleocrophic help-tool <tool-id>
```

### "Invalid parameter format"
```bash
# Example: For IP geolocation
# ❌ Aleocrophic run ip-geo --ip invalid
# ✅ Aleocrophic run ip-geo --ip 8.8.8.8

# Example: For URLs
# ❌ Aleocrophic run web-phishing --url example.com
# ✅ Aleocrophic run web-phishing --url http://example.com
```

## Tips & Tricks

1. **Use JSON export** for automated processing
   ```bash
   Aleocrophic run dns --domain example.com --output results.json
   ```

2. **Combine with external tools**
   ```bash
   # Export to JSON and process with jq
   Aleocrophic run port-scan --host target.com --output scan.json | jq '.open_ports'
   ```

3. **Check tool version**
   ```bash
   Aleocrophic run dns  # Shows version in help output
   ```

4. **View latest results**
   ```bash
   # Check output directory
   ls output/
   ```

## Resources

- **Full Documentation**: See `INTERACTIVE_CLI_GUIDE.md`
- **Tool Documentation**: `docs/TOOLS.md`
- **Project Summary**: `PROJECT_SUMMARY.md`
- **Installation Guide**: `INSTALL_GUIDE.md`

## Getting Help

1. Check tool help:
   ```bash
   Aleocrophic help-tool <tool-id>
   ```

2. View tool list:
   ```bash
   Aleocrophic list-tools
   ```

3. Check specific command:
   ```bash
   Aleocrophic run --help
   ```

4. View project documentation:
   - Check `README.md`
   - Check `docs/TOOLS.md`
   - Check `INTERACTIVE_CLI_GUIDE.md`

## Version Information

- **Aleocrophic**: v2.0+
- **Python**: 3.7+
- **Key Dependencies**: click, requests, rich

---

**Last Updated**: December 2025
**Framework**: Aleocrophic Penetration Testing Suite
