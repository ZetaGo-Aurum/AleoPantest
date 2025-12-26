# Aleocrophic v2.0 - Advanced Features Documentation

## 🎯 New Features Overview

This document outlines the advanced features added in the latest update to Aleocrophic v2.0.

---

## 🎣 Ngrok Phishing Tools

### Purpose
Educational tool for demonstrating sophisticated phishing attacks with real internet exposure via ngrok tunneling.

### Features
- **Login Page Phishing**: Create convincing login pages to capture credentials
- **Camera Permission Phishing**: Trick users into granting camera access
- **Location Permission Phishing**: Extract user location data
- **Custom HTML**: Deploy custom phishing templates

### Usage Example
```bash
# Get ngrok token from https://dashboard.ngrok.com
Aleocrophic run ngrok-phishing \
  --ngrok-token YOUR_NGROK_TOKEN \
  --phishing-type login \
  --target facebook
```

### Safety & Legal Notes
⚠️ **CRITICAL**: This tool is **ILLEGAL** without explicit written authorization. 
- Federal penalties apply
- Only use for authorized penetration testing
- Must have documented client approval
- Educational purposes only in controlled environments

---

## 🔍 Advanced Search Engine Dorking

### Purpose
Multi-engine search dorking with pre-built templates for discovering exposed information.

### Supported Search Engines
- **Google**: Full operator support (site:, inurl:, intitle:, filetype:, etc.)
- **DuckDuckGo**: Privacy-focused alternative
- **GitHub**: Source code and repository discovery
- **Shodan**: IoT device and server discovery (requires API key)
- **Bing**: Alternative search engine

### Built-in Templates
```
• exposed_configs   - Find .conf, .yaml, .env files
• admin_panels      - Discover /admin, /control panel
• backup_files      - Locate .sql, .bak, .backup files
• source_code       - Find exposed .php, .py, .java files
• user_data         - Find user exports and CSVs
• ssl_certs         - Locate .crt, .pem, .key files
• logs              - Find log files and debug info
```

### Usage Examples
```bash
# Using built-in template
Aleocrophic run advanced-dorking \
  --engine google \
  --domain target.com \
  --template exposed_configs

# Custom query
Aleocrophic run advanced-dorking \
  --engine duckduckgo \
  --query "site:github.com password config"

# GitHub source code search
Aleocrophic run advanced-dorking \
  --engine github \
  --query "api_key secret database"

# Shodan IoT discovery (requires API key)
Aleocrophic run advanced-dorking \
  --engine shodan \
  --shodan-api-key YOUR_API_KEY \
  --query "port:3389 os:windows"
```

---

## ⚔️ Real DDoS Attack Mode

### Purpose
Authorized penetration testing tool for real DDoS attacks with built-in safety limits.

### Safety Limits (Cannot be bypassed)
```
Maximum duration:     120 seconds
Maximum threads:      50 concurrent connections
Maximum requests:     10,000 total requests
Rate limit trigger:   Pauses if > 1,000 req/sec
```

### Attack Types Supported
- **HTTP Flood**: HTTP request flooding
- **SYN Flood**: TCP SYN packet flooding
- **UDP Flood**: UDP packet flooding
- **DNS Flood**: DNS query flooding
- **Slowloris**: Slow HTTP connection attack

### Authorization Requirement
⚠️ **MANDATORY**: Requires explicit `--authorized` flag

### Usage Example
```bash
# HTTP flood attack (requires authorization)
Aleocrophic run ddos-sim \
  --target example.com \
  --type http \
  --duration 30 \
  --threads 20 \
  --authorized
```

### Legal Compliance
- **ILLEGAL** without written authorization
- Only use against systems you own or have permission to test
- Federal Computer Fraud and Abuse Act (CFAA) violations carry criminal penalties
- Maintain detailed audit logs of all testing

---

## 📦 Complete Library Dependencies

### New Dependencies Added
```
# Network Analysis
whois==0.9.1
python-whois==0.7.3

# Ngrok Tunneling
ngrok==6.1.1
pyngrok==7.0.1

# Search Engines & OSINT
duckduckgo-search==3.9.5
bing-image-downloader==1.3.3

# Geolocation
geoip2==4.7.0
maxminddb==2.2.0
```

### Installation
```bash
# All dependencies
pip install -r requirements.txt

# Or update existing installation
pip install --upgrade -r requirements.txt
```

---

## 📋 Commands Reference

### List All Tools
```bash
Aleocrophic list-tools
```

### Get Help for Specific Tool
```bash
Aleocrophic help-tool ngrok-phishing
Aleocrophic help-tool advanced-dorking
Aleocrophic help-tool ddos-sim
```

### Run with Output
```bash
Aleocrophic run advanced-dorking \
  --engine google \
  --domain target.com \
  --template exposed_configs \
  --output results.json
```

---

## ⚖️ Legal Disclaimer

**Aleocrophic is provided for educational and authorized security testing purposes only.**

### Important Notes
1. **Authorization Required**: Always obtain written permission before testing
2. **Legal Liability**: You are responsible for any unauthorized access or damage
3. **Ethical Use**: Follow responsible disclosure practices
4. **Compliance**: Adhere to all applicable laws and regulations
5. **Documentation**: Keep detailed logs of all security testing activities

### Potential Violations
Unauthorized use may violate:
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- EU Network and Information Security Directive
- Similar laws in other jurisdictions

---

## 🔒 Best Practices

### Before Using These Tools
1. ✅ Obtain written authorization from system owner
2. ✅ Define scope and rules of engagement (ROE)
3. ✅ Document all testing activities
4. ✅ Use isolated test environment when possible
5. ✅ Have incident response plan ready
6. ✅ Coordinate with IT team if applicable

### During Testing
1. ✅ Monitor system performance and impact
2. ✅ Start with low-intensity attacks
3. ✅ Stop immediately if issues detected
4. ✅ Log all commands and results
5. ✅ Respect safety limits and timeouts

### After Testing
1. ✅ Generate detailed report
2. ✅ Include recommendations for remediation
3. ✅ Maintain confidentiality of findings
4. ✅ Follow responsible disclosure timeline
5. ✅ Provide executive summary to stakeholders

---

## 🚀 Advanced Configuration

### Custom Dorking Templates
Extend `DORK_TEMPLATES` in `advanced_dorking.py`:
```python
DORK_TEMPLATES = {
    'custom_template': [
        'site:{domain} custom_query_1',
        'site:{domain} custom_query_2',
    ]
}
```

### Ngrok Configuration
Set ngrok token via environment variable:
```bash
export NGROK_AUTHTOKEN=your_token_here
Aleocrophic run ngrok-phishing --phishing-type login
```

### DDoS Custom Attack
Modify rate limiting in `ddos_simulator.py`:
```python
SAFETY_LIMITS = {
    'max_duration': 120,      # Modify as needed
    'max_threads': 50,        # Increase for test
    'max_rate': 10000,        # Adjust rate
    'rate_limit_threshold': 1000
}
```

---

## 📞 Support & Issues

- **GitHub Issues**: https://github.com/ZetaGo-Aurum/Aleocrophic/issues
- **Documentation**: See other .md files in root directory
- **Quick Start**: Start with `QUICKSTART.md`

---

**Version**: 2.0.0  
**Last Updated**: December 25, 2025  
**Maintained By**: Aleocrophic Team

---

⚠️ **REMINDER**: Use these tools responsibly and legally. Unauthorized access is a crime.
