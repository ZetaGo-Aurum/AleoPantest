# AloPantest v2.0 - Quick Start Guide

## 🚀 Instalasi Cepat

### 1. Install Package
```bash
cd AloPantest
pip install -e .
pip install -r requirements.txt
```

### 2. Verifikasi Instalasi
```bash
aleopantest --help
aleopantest info
```

## 💡 Contoh Penggunaan

### Phishing Detection
```bash
# Deteksi website phishing
aleopantest run web-phishing --url http://suspicious-site.com

# Analisis email phishing
aleopantest run email-phishing --email "hacker@fake.com" --subject "Verify Now"

# Cari domain phishing dari target
aleopantest run phishing-locator --domain example.com

# Buat template phishing untuk awareness training
aleopantest run phishing-impersonation --type email --target bank
```

### Clickjacking Detection
```bash
# Check vulnerability clickjacking
aleopantest run clickjacking-check --url http://target.com

# Buat PoC (Proof of Concept)
aleopantest run clickjacking-make --url http://target.com --type basic

# Generate header proteksi
aleopantest run anti-clickjacking --framework nginx --output nginx.conf
```

### Security Analysis
```bash
# Deteksi DDoS protection (Cloudflare, Akamai, dll)
aleopantest run anti-ddos --url http://target.com

# Deteksi WAF (Web Application Firewall)
aleopantest run waf-detect --url http://target.com
```

### Network Tools
```bash
# DNS Lookup
aleopantest run dns --domain google.com

# Port Scanning
aleopantest run port-scan --host 192.168.1.1

# SSL Certificate Check
aleopantest run ssl-check --domain google.com

# DDoS Simulation (authorized testing only)
aleopantest run ddos-sim --target target.com --type http --duration 30
```

## 📊 Daftar Tools by Category

### Phishing (4 tools)
- `web-phishing` - Phishing website detection
- `email-phishing` - Email phishing analysis
- `phishing-locator` - Find phishing domains
- `phishing-impersonation` - Create phishing templates

### Clickjacking (3 tools)
- `clickjacking-check` - Check vulnerability
- `clickjacking-make` - Create PoC
- `anti-clickjacking` - Generate protection code

### Security (2 tools)
- `anti-ddos` - Detect DDoS protection
- `waf-detect` - Detect Web Application Firewall

### Network (9 tools)
- `dns` - DNS Lookup
- `ping` - Ping host
- `port-scan` - Port scanning
- `ssl-check` - SSL certificate check
- `traceroute` - Trace network path
- `whois` - WHOIS lookup
- `ip-scan` - IP scanning
- `sniffer` - Packet sniffing
- `ddos-sim` - DDoS simulation

### Web (6 tools)
- `sql-inject` - SQL injection testing
- `xss-detect` - XSS detection
- `csrf-detect` - CSRF detection
- `crawler` - Web crawling
- `vuln-scan` - Vulnerability scanning
- `subdomain` - Subdomain finding

### OSINT (5 tools)
- `email-find` - Email finding
- `domain-info` - Domain information
- `ip-geo` - IP geolocation
- `metadata` - Metadata extraction
- `dorking` - Search engine dorking

### Utilities (5 tools)
- `passgen` - Password generator
- `hash` - Hash tools
- `proxy` - Proxy manager
- `encode` - URL encoder
- `revshell` - Reverse shell generator

## 🎯 Common Workflows

### Workflow 1: Website Security Audit
```bash
# 1. Check for phishing characteristics
aleopantest run web-phishing --url http://target.com

# 2. Check clickjacking protection
aleopantest run clickjacking-check --url http://target.com

# 3. Detect WAF
aleopantest run waf-detect --url http://target.com

# 4. Detect DDoS protection
aleopantest run anti-ddos --url http://target.com

# 5. Check SSL
aleopantest run ssl-check --domain target.com

# 6. Find subdomains
aleopantest run subdomain --url http://target.com
```

### Workflow 2: Phishing Campaign Investigation
```bash
# 1. Analyze email sender
aleopantest run email-phishing --email "suspicious@fake-domain.com" --subject "Urgent Action Required"

# 2. Check website characteristics
aleopantest run web-phishing --url http://suspicious-site.com

# 3. Find phishing domain variants
aleopantest run phishing-locator --domain legitimate-site.com

# 4. Generate awareness template
aleopantest run phishing-impersonation --type email --target company-name
```

### Workflow 3: Security Hardening
```bash
# 1. Check current protections
aleopantest run anti-ddos --url http://target.com
aleopantest run waf-detect --url http://target.com

# 2. Check clickjacking
aleopantest run clickjacking-check --url http://target.com

# 3. Generate protection headers
aleopantest run anti-clickjacking --framework nginx

# 4. View and implement recommendations
aleopantest help-tool anti-clickjacking
```

## 🔧 Help & Documentation

```bash
# Show all commands
aleopantest --help

# List all tools
aleopantest list-tools

# Show statistics
aleopantest info

# Get help for specific tool
aleopantest help-tool dns
aleopantest help-tool web-phishing
aleopantest help-tool clickjacking-check

# List tools by category
aleopantest list-by-category Phishing
aleopantest list-by-category Security
aleopantest list-by-category Network
```

## ⚙️ Advanced Options

### Export Results
```bash
aleopantest run dns --domain target.com --output results.json
```

### Run with Multiple Options
```bash
aleopantest run web-phishing --url http://target.com --output phishing_report.json
```

### Adjust Thread Count (for network tools)
```bash
aleopantest run port-scan --host 192.168.1.1 --threads 50
```

### DDoS Testing Parameters
```bash
# Quick test (10 seconds)
aleopantest run ddos-sim --target target.com --type http --duration 10

# Extended test (5 minutes with 20 threads)
aleopantest run ddos-sim --target target.com --type http --duration 300 --threads 20
```

## 📝 Output

Results are shown in terminal and optionally saved to JSON:
```bash
# Results displayed in rich format with colors and tables
# Saved to: output/results.json (if --output specified)
```

## ⚠️ Legal & Ethical

- ✅ Use only on authorized systems
- ✅ Get written permission before testing
- ✅ Document all testing activities
- ✅ Follow local laws and regulations
- ❌ Never use for unauthorized access
- ❌ Never use for malicious purposes

## 🆘 Troubleshooting

### Command not found
```bash
# Reinstall package
pip install -e .
```

### Module not found
```bash
# Install requirements again
pip install -r requirements.txt
```

### Permission errors
- Run as administrator (if needed)
- Check output directory permissions
- Ensure write access to logs/ and output/ directories

## 🔗 More Information

- Full README: `README_v2.md`
- Installation Guide: `INSTALLATION.md`
- Tool Documentation: `docs/TOOLS.md`
- Project Summary: `PROJECT_SUMMARY.md`

---

Happy testing! Stay ethical and responsible. 🛡️
