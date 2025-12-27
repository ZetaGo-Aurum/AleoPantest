# Aleopantest V3.0.0 Quick Start Guide
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>

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

### 1. Help & Information
-   **Show global help**: `aleopantest --help`
-   **Show tool stats**: `aleopantest info`
-   **List all tools**: `aleopantest list-tools`
-   **List category**: `aleopantest list-by-category network`
-   **Interactive Dashboard**: `aleopantest tui`

### 2. Tool Documentation
-   **Show tool help**: `aleopantest help-tool <tool-id>`
-   **Example**: `aleopantest help-tool port-scan`

### 3. Execution Patterns
-   **Run with target**: `aleopantest run <tool-id> --target <target>`
-   **Run with params**: `aleopantest run <tool-id> --param1 val1 --param2 val2`
-   **Run interactive**: `aleopantest run <tool-id>` (prompts for missing params)

---

## 💡 Pro Tips

1.  **Use Tab Completion**: If installed globally, `aleopantest` supports tab completion.
2.  **Check Tool Help**: Always run `aleopantest help-tool <tool-id>` before using a new tool.
3.  **TUI Experience**: Try `aleopantest tui` for a professional, visual dashboard experience.
4.  **Quick List**: Use `aleopantest list-tools` to see all 39+ available security tools.

---

## 📞 Support & Feedback

-   **Version**: V3.0.0
-   **Framework**: Aleopantest Penetration Testing Suite
-   **By**: Aleocrophic
-   **License**: Educational/Authorized Use Only
