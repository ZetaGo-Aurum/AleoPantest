# Aleocrophic v2.0 - Quick Start Guide

## 🚀 Instalasi Cepat

### 1. Install Package
```bash
cd Aleocrophic
pip install -e .
pip install -r requirements.txt
```

### 2. Verifikasi Instalasi
```bash
Aleocrophic --help
Aleocrophic info
```

## 💡 Contoh Penggunaan

### Phishing Detection
```bash
# Deteksi website phishing
Aleocrophic run web-phishing --url http://suspicious-site.com

# Analisis email phishing
Aleocrophic run email-phishing --email "hacker@fake.com" --subject "Verify Now"

# Cari domain phishing dari target
Aleocrophic run phishing-locator --domain example.com

# Buat template phishing untuk awareness training
Aleocrophic run phishing-impersonation --type email --target bank
```

### Clickjacking Detection
```bash
# Check vulnerability clickjacking
Aleocrophic run clickjacking-check --url http://target.com

# Buat PoC (Proof of Concept)
Aleocrophic run clickjacking-make --url http://target.com --type basic

# Generate header proteksi
Aleocrophic run anti-clickjacking --framework nginx --output nginx.conf
```

### Security Analysis
```bash
# Deteksi DDoS protection (Cloudflare, Akamai, dll)
Aleocrophic run anti-ddos --url http://target.com

# Deteksi WAF (Web Application Firewall)
Aleocrophic run waf-detect --url http://target.com
```

### Network Tools
```bash
# DNS Lookup
Aleocrophic run dns --domain google.com

# Port Scanning
Aleocrophic run port-scan --host 192.168.1.1

# SSL Certificate Check
Aleocrophic run ssl-check --domain google.com

# DDoS Simulation (authorized testing only)
Aleocrophic run ddos-sim --target target.com --type http --duration 30
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
Aleocrophic run web-phishing --url http://target.com

# 2. Check clickjacking protection
Aleocrophic run clickjacking-check --url http://target.com

# 3. Detect WAF
Aleocrophic run waf-detect --url http://target.com

# 4. Detect DDoS protection
Aleocrophic run anti-ddos --url http://target.com

# 5. Check SSL
Aleocrophic run ssl-check --domain target.com

# 6. Find subdomains
Aleocrophic run subdomain --url http://target.com
```

### Workflow 2: Phishing Campaign Investigation
```bash
# 1. Analyze email sender
Aleocrophic run email-phishing --email "suspicious@fake-domain.com" --subject "Urgent Action Required"

# 2. Check website characteristics
Aleocrophic run web-phishing --url http://suspicious-site.com

# 3. Find phishing domain variants
Aleocrophic run phishing-locator --domain legitimate-site.com

# 4. Generate awareness template
Aleocrophic run phishing-impersonation --type email --target company-name
```

### Workflow 3: Security Hardening
```bash
# 1. Check current protections
Aleocrophic run anti-ddos --url http://target.com
Aleocrophic run waf-detect --url http://target.com

# 2. Check clickjacking
Aleocrophic run clickjacking-check --url http://target.com

# 3. Generate protection headers
Aleocrophic run anti-clickjacking --framework nginx

# 4. View and implement recommendations
Aleocrophic help-tool anti-clickjacking
```

## 🔧 Help & Documentation

```bash
# Show all commands
Aleocrophic --help

# List all tools
Aleocrophic list-tools

# Show statistics
Aleocrophic info

# Get help for specific tool
Aleocrophic help-tool dns
Aleocrophic help-tool web-phishing
Aleocrophic help-tool clickjacking-check

# List tools by category
Aleocrophic list-by-category Phishing
Aleocrophic list-by-category Security
Aleocrophic list-by-category Network
```

## ⚙️ Advanced Options

### Export Results
```bash
Aleocrophic run dns --domain target.com --output results.json
```

### Run with Multiple Options
```bash
Aleocrophic run web-phishing --url http://target.com --output phishing_report.json
```

### Adjust Thread Count (for network tools)
```bash
Aleocrophic run port-scan --host 192.168.1.1 --threads 50
```

### DDoS Testing Parameters
```bash
# Quick test (10 seconds)
Aleocrophic run ddos-sim --target target.com --type http --duration 10

# Extended test (5 minutes with 20 threads)
Aleocrophic run ddos-sim --target target.com --type http --duration 300 --threads 20
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
