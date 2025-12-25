# AloPantest Quick Start Guide

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# View main help
aleopantest --help

# View all tools
aleopantest list-tools

# Get statistics
aleopantest info
```

## Common Commands

### OSINT Tools

#### IP Geolocation
```bash
# Get IP location (geolocation & ISP info)
aleopantest run ip-geo --ip 8.8.8.8
aleopantest run ip-geo --host 1.1.1.1
```

#### Domain Information
```bash
# Get domain information
aleopantest run domain-info --domain google.com
```

#### Email Finder
```bash
# Find email addresses from domain
aleopantest run email-find --domain example.com
```

### Network Tools

#### DNS Lookup
```bash
# Perform DNS lookup
aleopantest run dns --domain target.com
```

#### Port Scanning
```bash
# Scan for open ports
aleopantest run port-scan --host 192.168.1.1
aleopantest run port-scan --host target.com
```

#### SSL Certificate Check
```bash
# Check SSL certificate
aleopantest run ssl-check --domain https://example.com
```

#### Ping
```bash
# Ping a host
aleopantest run ping --host 8.8.8.8
```

#### Traceroute
```bash
# Trace route to host
aleopantest run traceroute --host 8.8.8.8
```

#### WHOIS Lookup
```bash
# Get WHOIS information
aleopantest run whois --domain example.com
```

### Web Vulnerability Tools

#### SQL Injection Detection
```bash
# Test for SQL injection vulnerabilities
aleopantest run sql-inject --url http://example.com
```

#### XSS Detection
```bash
# Test for cross-site scripting
aleopantest run xss-detect --url http://example.com
```

#### CSRF Detection
```bash
# Test for CSRF vulnerabilities
aleopantest run csrf-detect --url http://example.com
```

#### Web Crawler
```bash
# Crawl website structure
aleopantest run crawler --url http://example.com
```

#### Vulnerability Scanner
```bash
# Scan for vulnerabilities
aleopantest run vuln-scan --url http://example.com
```

#### Subdomain Finder
```bash
# Find subdomains
aleopantest run subdomain --domain example.com
```

### Security Tools

#### WAF Detection
```bash
# Detect Web Application Firewall
aleopantest run waf-detect --url http://example.com
```

#### Anti-DDoS Check
```bash
# Check anti-DDoS protection
aleopantest run anti-ddos --url http://example.com
```

#### Clickjacking Check
```bash
# Test for clickjacking vulnerability
aleopantest run clickjacking-check --url http://example.com
```

### Phishing Tools

#### Web Phishing Detection
```bash
# Detect phishing websites
aleopantest run web-phishing --url http://suspicious-site.com
```

#### Email Phishing
```bash
# Simulate email phishing (authorized only)
aleopantest run email-phishing --email target@example.com --subject "Important Update"
```

#### Phishing Locator
```bash
# Find phishing variants of domain
aleopantest run phishing-locator --domain example.com
```

### Clickjacking Tools

#### Generate Anti-Clickjacking Config
```bash
# Generate anti-clickjacking headers (nginx)
aleopantest run anti-clickjacking --framework nginx --output config.conf

# Generate anti-clickjacking headers (apache)
aleopantest run anti-clickjacking --framework apache --output config.conf
```

#### Clickjacking Maker
```bash
# Create clickjacking test page
aleopantest run clickjacking-make --url http://example.com
```

### Utility Tools

#### Password Generator
```bash
# Generate random password
aleopantest run passgen
```

#### Hash Tools
```bash
# Hash generation and cracking
aleopantest run hash --type md5 --input "password"
```

#### URL Encoder
```bash
# Encode URLs
aleopantest run encode --url "http://example.com?param=value"
```

#### URL Masking
```bash
# Mask URL appearance
aleopantest run url-mask --url https://attacker.com --fake-domain google.com --method redirect
```

#### URL Shortener
```bash
# Create short URL
aleopantest run url-shorten --url https://very-long-url.example.com --alias mylink
```

#### Reverse Shell Generator
```bash
# Generate reverse shell code
aleopantest run revshell --type bash
```

### Advanced Tools

#### DDoS Simulator (AUTHORIZED TESTING ONLY)
```bash
# Light DDoS simulation (10s, 5 threads)
aleopantest run ddos-sim --target example.com --type http --preset light --authorized

# Medium DDoS simulation (30s, 10 threads)
aleopantest run ddos-sim --target example.com --type http --preset medium --authorized

# Heavy DDoS simulation (60s, 20 threads)
aleopantest run ddos-sim --target example.com --type http --preset heavy --authorized

# Custom duration and threads
aleopantest run ddos-sim --target example.com --type dns --duration 45 --threads 15 --authorized

# Different attack types
aleopantest run ddos-sim --target example.com --type slowloris --preset light --authorized
aleopantest run ddos-sim --target example.com --type syn --preset medium --authorized
```

#### Metadata Extractor
```bash
# Extract metadata from files
aleopantest run metadata --file document.pdf
```

#### Search Engine Dorking
```bash
# Perform Google dorking
aleopantest run dorking --domain example.com
```

## Output Options

### Save Results to JSON
```bash
# Export results to JSON file
aleopantest run dns --domain example.com --output results.json
aleopantest run ip-geo --ip 8.8.8.8 --output location.json
```

### Generate Reports
```bash
# Tools support exporting to various formats
aleopantest run port-scan --host target.com --output scan_results.json
aleopantest run vuln-scan --url http://example.com --output vulnerabilities.json
```

## Help & Documentation

```bash
# Get general help
aleopantest --help

# Get command-specific help
aleopantest run --help

# Get tool-specific help
aleopantest help-tool dns
aleopantest help-tool ip-geo
aleopantest help-tool ddos-sim

# List tools by category
aleopantest list-by-category network
aleopantest list-by-category osint
aleopantest list-by-category web
aleopantest list-by-category phishing

# View current configuration
aleopantest config-show
```

## Advanced Usage

### Interactive Mode
```bash
# Launch interactive parameter entry (future feature)
aleopantest run dns --interactive
aleopantest run ip-geo --interactive
```

### Batch Operations
```bash
# Test multiple domains
aleopantest run dns --domain example.com --output example.json
aleopantest run dns --domain google.com --output google.json
```

### Chaining Tools
```bash
# Find subdomains then scan them
aleopantest run subdomain --domain example.com --output subdomains.json
# Then use those subdomains in other tools
aleopantest run port-scan --host sub1.example.com
aleopantest run port-scan --host sub2.example.com
```

## Parameter Aliases

### IP/Host Parameters
```bash
# All these are equivalent:
aleopantest run ip-geo --ip 8.8.8.8
aleopantest run ip-geo --host 8.8.8.8
aleopantest run ip-geo --address 8.8.8.8
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
aleopantest run ddos-sim --target example.com --type http --preset light --authorized
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
aleopantest list-tools

# Or check by category
aleopantest list-by-category network
```

### "Missing required parameter"
```bash
# Check what parameters are needed
aleopantest help-tool <tool-id>
```

### "Invalid parameter format"
```bash
# Example: For IP geolocation
# ❌ aleopantest run ip-geo --ip invalid
# ✅ aleopantest run ip-geo --ip 8.8.8.8

# Example: For URLs
# ❌ aleopantest run web-phishing --url example.com
# ✅ aleopantest run web-phishing --url http://example.com
```

## Tips & Tricks

1. **Use JSON export** for automated processing
   ```bash
   aleopantest run dns --domain example.com --output results.json
   ```

2. **Combine with external tools**
   ```bash
   # Export to JSON and process with jq
   aleopantest run port-scan --host target.com --output scan.json | jq '.open_ports'
   ```

3. **Check tool version**
   ```bash
   aleopantest run dns  # Shows version in help output
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
   aleopantest help-tool <tool-id>
   ```

2. View tool list:
   ```bash
   aleopantest list-tools
   ```

3. Check specific command:
   ```bash
   aleopantest run --help
   ```

4. View project documentation:
   - Check `README.md`
   - Check `docs/TOOLS.md`
   - Check `INTERACTIVE_CLI_GUIDE.md`

## Version Information

- **AloPantest**: v2.0+
- **Python**: 3.7+
- **Key Dependencies**: click, requests, rich

---

**Last Updated**: December 2025
**Framework**: AloPantest Penetration Testing Suite
