# QUICK START GUIDE

Panduan cepat untuk mulai menggunakan AloPantest.

## 5 Menit Setup

### 1. Install
```bash
cd AloPantest
pip install -r requirements.txt
```

### 2. Verify
```bash
python alo_pantest_cli.py info
```

### 3. List Tools
```bash
python alo_pantest_cli.py list-tools
```

### 4. Run Your First Tool
```bash
# DNS Lookup (safe & educational)
python alo_pantest_cli.py run dns --domain google.com
```

## Common Usage

### Network Tools
```bash
# Port Scanning
python alo_pantest_cli.py run port-scan --host 192.168.1.1

# Ping
python alo_pantest_cli.py run ping --host 8.8.8.8

# SSL Check
python alo_pantest_cli.py run ssl-check --host google.com
```

### Web Tools
```bash
# Web Vulnerability Scan
python alo_pantest_cli.py run vuln-scan --url http://target.com

# Subdomain Finder
python alo_pantest_cli.py run subdomain --domain target.com

# Web Crawler
python alo_pantest_cli.py run crawler --url http://target.com
```

### OSINT Tools
```bash
# Domain Info
python alo_pantest_cli.py run domain-info --domain target.com

# IP Geolocation
python alo_pantest_cli.py run ip-geo --ip 8.8.8.8

# Email Finder
python alo_pantest_cli.py run email-find --domain target.com
```

### Utilities
```bash
# Generate Password
python alo_pantest_cli.py run passgen --length 16 --count 5

# Hash Text
python alo_pantest_cli.py run hash --text "password" --algorithm sha256

# Encode URL
python alo_pantest_cli.py run encode --text "hello world"

# Generate Reverse Shell
python alo_pantest_cli.py run revshell --host 10.0.0.1 --port 4444
```

## Getting Help

```bash
# Tool information
python alo_pantest_cli.py info

# List all tools
python alo_pantest_cli.py list-tools

# Help for specific tool
python alo_pantest_cli.py help-tool port-scan
```

## Export Results

```bash
# Save results to JSON
python alo_pantest_cli.py run port-scan --host 192.168.1.1 --output results.json
```

## Important Notes

⚠️ **ALWAYS TEST ON SYSTEMS YOU OWN OR HAVE PERMISSION TO TEST**

- Never unauthorized scanning
- Always get written permission
- Use ethically and legally
- Report vulnerabilities responsibly
- Respect privacy and data

---

Ready? Start with:
```bash
python alo_pantest_cli.py info
```

Happy Testing! 🛡️
