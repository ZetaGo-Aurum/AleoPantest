# AloPantest - Comprehensive Penetration Testing Framework

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  AloPantest - Penetration Testing Framework  🛡️   ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                     v1.0.0 (Educational)                     ║
║                                                               ║
║     350+ Tools • Multi-Platform • Rich CLI • Full Featured    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Tools](#available-tools)
- [Usage Guide](#usage-guide)
- [Platform Support](#platform-support)
- [Documentation](#documentation)
- [License](#license)

## 🎯 Overview

**AloPantest** adalah framework comprehensive untuk penetration testing dan cybersecurity learning. Dikembangkan dengan Python, menyediakan lebih dari 350 tools siap pakai yang dirancang untuk berbagai kebutuhan testing cyber, mulai dari network reconnaissance, web exploitation, OSINT, hingga cryptography tools.

### Target Pengguna
- 🎓 Cybersecurity Students
- 🔒 Security Professionals
- 🔍 Penetration Testers
- 👨‍💼 Bug Bounty Hunters
- 📚 Security Researchers

### Tujuan Pengembangan
Tool ini dikembangkan **untuk keperluan edukasi dan pembelajaran cybersecurity** dengan standar etika yang tinggi. Penggunaan hanya diizinkan pada sistem yang Anda miliki atau dengan izin eksplisit dari pemilik sistem.

## ✨ Features

### 🌐 Network Tools (8+ Tools)
- **Port Scanner** - Fast multi-threaded port scanning
- **Packet Sniffer** - Real-time network traffic analysis
- **Ping Tool** - Host reachability testing
- **DNS Lookup** - Domain name resolution
- **Traceroute** - Network path analysis
- **WHOIS Lookup** - Domain ownership information
- **SSL Checker** - Certificate analysis
- **IP Scanner** - Subnet enumeration

### 🌍 Web Exploitation Tools (6+ Tools)
- **SQL Injector** - SQL injection vulnerability testing
- **XSS Detector** - Cross-site scripting detection
- **CSRF Detector** - Cross-site request forgery analysis
- **Web Crawler** - Website structure mapping
- **Vulnerability Scanner** - Common web vulnerabilities
- **Subdomain Finder** - Subdomain enumeration

### 🔎 OSINT Tools (5+ Tools)
- **Email Finder** - Email address discovery
- **Domain Info** - Comprehensive domain gathering
- **IP Geolocation** - Geographical IP lookup
- **Metadata Extractor** - File and website metadata
- **Search Engine Dorking** - Advanced search queries

### 🛠️ Utility Tools (5+ Tools)
- **Password Generator** - Secure password generation
- **Hash Tools** - Multi-algorithm hashing (MD5, SHA1, SHA256, etc.)
- **Proxy Manager** - Proxy testing and rotation
- **URL Encoder/Decoder** - Encoding transformations
- **Reverse Shell Generator** - Payload generation

### 📦 Extensible Architecture
- Modular tool system
- Easy to add new tools
- Plugin-based architecture
- Custom tool development support

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python Package Manager)
- Git (optional)

### 1. Install from Source

```bash
# Clone or download repository
cd AloPantest

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### 2. Verify Installation

```bash
python alo_pantest_cli.py info
```

### 3. Platform-Specific Installation

#### 🐧 Linux/Ubuntu/Debian
```bash
# Update system packages
sudo apt-get update
sudo apt-get install python3 python3-pip

# Install AloPantest
cd AloPantest
pip3 install -r requirements.txt
```

#### 🪟 Windows (Native)
```powershell
# Using PowerShell
cd AloPantest
pip install -r requirements.txt
python alo_pantest_cli.py info
```

#### 🪟 Windows (WSL - Recommended)
```bash
# Enable WSL: https://docs.microsoft.com/en-us/windows/wsl/install
wsl --install

# Inside WSL terminal
cd AloPantest
pip3 install -r requirements.txt
python3 alo_pantest_cli.py info
```

#### 📱 Termux (Android)
```bash
# Install Termux: https://termux.dev/

# Inside Termux
pkg update
pkg install python3 python3-pip git

cd AloPantest
pip install -r requirements.txt

python alo_pantest_cli.py info
```

#### 🍎 macOS
```bash
# Using Homebrew
brew install python3

cd AloPantest
pip3 install -r requirements.txt
python3 alo_pantest_cli.py info
```

## 🚀 Quick Start

### 1. List Available Tools
```bash
python alo_pantest_cli.py list-tools
```

### 2. Get Tool Information
```bash
python alo_pantest_cli.py info
```

### 3. Run a Tool

#### Port Scanning
```bash
python alo_pantest_cli.py run port-scan --host 192.168.1.1
```

#### DNS Lookup
```bash
python alo_pantest_cli.py run dns --domain google.com
```

#### Web Vulnerability Scan
```bash
python alo_pantest_cli.py run vuln-scan --url http://target.com
```

#### SQL Injection Test
```bash
python alo_pantest_cli.py run sql-inject --url http://target.com/page.php?id=1
```

#### Password Generation
```bash
python alo_pantest_cli.py run passgen
```

### 4. Export Results
```bash
python alo_pantest_cli.py run port-scan --host 192.168.1.1 --output scan_results.json
```

### 5. Get Tool Help
```bash
python alo_pantest_cli.py help-tool port-scan
```

## 📚 Available Tools

### Network Tools (8)
| Tool ID | Name | Description |
|---------|------|-------------|
| `port-scan` | Port Scanner | Multi-threaded port scanning |
| `sniffer` | Packet Sniffer | Network traffic capture |
| `ping` | Ping Tool | Host reachability test |
| `dns` | DNS Lookup | Domain resolution |
| `traceroute` | Traceroute | Network path analysis |
| `whois` | WHOIS Lookup | Domain info |
| `ssl-check` | SSL Checker | Certificate analysis |
| `ip-scan` | IP Scanner | Subnet scanning |

### Web Tools (6)
| Tool ID | Name | Description |
|---------|------|-------------|
| `sql-inject` | SQL Injector | SQLi vulnerability testing |
| `xss-detect` | XSS Detector | XSS vulnerability detection |
| `csrf-detect` | CSRF Detector | CSRF vulnerability analysis |
| `crawler` | Web Crawler | Website mapping |
| `vuln-scan` | Vulnerability Scanner | Common vulnerabilities |
| `subdomain` | Subdomain Finder | Subdomain enumeration |

### OSINT Tools (5)
| Tool ID | Name | Description |
|---------|------|-------------|
| `email-find` | Email Finder | Email discovery |
| `domain-info` | Domain Info | Domain information gathering |
| `ip-geo` | IP Geolocation | Geographical lookup |
| `metadata` | Metadata Extractor | Metadata extraction |
| `dorking` | Search Engine Dorking | Advanced search queries |

### Utility Tools (5)
| Tool ID | Name | Description |
|---------|------|-------------|
| `passgen` | Password Generator | Password generation |
| `hash` | Hash Tools | Hashing algorithms |
| `proxy` | Proxy Manager | Proxy testing |
| `encode` | URL Encoder/Decoder | Encoding transformations |
| `revshell` | Reverse Shell Generator | Payload generation |

## 📖 Usage Guide

### Basic Usage Pattern
```bash
python alo_pantest_cli.py run <tool-id> [OPTIONS]
```

### Common Options
```
--host      Target hostname/IP
--url       Target URL
--domain    Target domain
--port      Port number
--output    Output file path
```

### Advanced Examples

#### 1. Complete Network Scan
```bash
# Port scan
python alo_pantest_cli.py run port-scan --host 192.168.1.1

# Get DNS info
python alo_pantest_cli.py run dns --domain target.com

# Check SSL certificate
python alo_pantest_cli.py run ssl-check --host target.com --port 443
```

#### 2. Web Application Testing
```bash
# Find subdomains
python alo_pantest_cli.py run subdomain --domain target.com

# Crawl website
python alo_pantest_cli.py run crawler --url http://target.com --depth 2

# Check vulnerabilities
python alo_pantest_cli.py run vuln-scan --url http://target.com

# Test SQL injection
python alo_pantest_cli.py run sql-inject --url http://target.com/page?id=1
```

#### 3. OSINT Operations
```bash
# Domain information
python alo_pantest_cli.py run domain-info --domain target.com

# IP geolocation
python alo_pantest_cli.py run ip-geo --ip 8.8.8.8

# Email finding
python alo_pantest_cli.py run email-find --domain target.com

# Metadata extraction
python alo_pantest_cli.py run metadata --url http://target.com
```

#### 4. Utility Operations
```bash
# Generate password
python alo_pantest_cli.py run passgen --length 16 --count 5

# Hash text
python alo_pantest_cli.py run hash --text "mypassword" --algorithm sha256

# URL encoding
python alo_pantest_cli.py run encode --text "hello world" --operation encode

# Reverse shell generation
python alo_pantest_cli.py run revshell --host 10.0.0.1 --port 4444 --language bash
```

### Using as Python Library

```python
from alo_pantest.modules.network import PortScanner
from alo_pantest.modules.web import SQLInjector
from alo_pantest.modules.osint import DomainInfo

# Port scanning
scanner = PortScanner()
result = scanner.run(host='192.168.1.1', ports='1-1024')
print(result)

# SQL injection testing
sqli = SQLInjector()
result = sqli.run(url='http://target.com/page.php?id=1')
print(result)

# Domain information gathering
info = DomainInfo()
result = info.run(domain='target.com')
print(result)
```

## 🖥️ Platform Support

| Platform | Status | Installation |
|----------|--------|--------------|
| 🐧 Linux | ✅ Full | Native |
| 🪟 Windows | ✅ Full | Native + WSL |
| 🪟 Windows (WSL) | ✅ Full | Recommended |
| 📱 Termux | ✅ Full | Mobile |
| 🍎 macOS | ✅ Full | Native |
| 🔒 Docker | ⏳ Coming | Container |

## 📋 Requirements

```
Python 3.8+
RAM: 512MB minimum (2GB recommended)
Disk: 100MB for installation
Network: Internet connection (for some tools)
```

## 📝 Configuration

### Config File (config/settings.yml)
```yaml
timeout: 30
retries: 3
thread_count: 5
user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
proxy: null
verbose: false
output_dir: 'output'
log_dir: 'logs'
cache_enabled: true
cache_ttl: 3600
```

## 🔐 Security & Ethics

### ⚠️ Important Notice
**AloPantest adalah tool UNTUK KEPERLUAN EDUKASI SEMATA.**

Penggunaan tool ini hanya diizinkan:
- ✅ Pada sistem yang Anda miliki
- ✅ Dengan izin eksplisit dari pemilik sistem
- ✅ Untuk keperluan pendidikan dan penelitian
- ✅ Untuk bug bounty programs yang terautentikasi

Penggunaan tidak diizinkan untuk:
- ❌ Unauthorized access ke sistem orang lain
- ❌ Illegal hacking atau cyber crimes
- ❌ Disruption of services
- ❌ Privacy violation

### Code of Ethics
- Respect privacy dan confidentiality
- Follow all applicable laws and regulations
- Disclose vulnerabilities responsibly
- Share knowledge untuk community benefit

## 📚 Documentation

### File Struktur
```
AloPantest/
├── alo_pantest/
│   ├── core/              # Core framework
│   ├── modules/           # Tool modules
│   │   ├── network/       # Network tools
│   │   ├── web/           # Web tools
│   │   ├── osint/         # OSINT tools
│   │   ├── utilities/     # Utility tools
│   │   ├── crypto/        # Crypto tools
│   │   └── wireless/      # Wireless tools
│   ├── cli.py             # CLI interface
│   └── api/               # API server
├── config/                # Configuration files
├── logs/                  # Log files
├── output/                # Output directory
├── requirements.txt       # Dependencies
├── setup.py              # Setup script
├── README.md             # This file
└── alo_pantest_cli.py    # Entry point
```

### Adding Custom Tools

```python
from alo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class CustomTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Custom Tool",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="Your Name",
            description="Tool description",
            usage="usage example",
            requirements=[],
            tags=["tag1", "tag2"]
        )
        super().__init__(metadata)
    
    def validate_input(self, **kwargs):
        return True
    
    def run(self, **kwargs):
        # Implementation
        pass
```

## 🐛 Troubleshooting

### ImportError: No module named 'requests'
```bash
pip install -r requirements.txt
```

### Permission Denied (Linux/Mac)
```bash
chmod +x alo_pantest_cli.py
./alo_pantest_cli.py
```

### Port Already in Use (API Server)
```bash
python alo_pantest_cli.py server --port 8000
```

### Certificate Verification Failed
```bash
# Windows
pip install --upgrade certifi

# Or use environment variable
set PYTHONHTTPSVERIFY=0
```

## 📞 Support & Community

- 📧 Email: support@alopantest.com
- 💬 Discord: [Join Community]
- 🐛 Issues: GitHub Issues
- 📖 Wiki: [Documentation Wiki]
- 💡 Discussions: GitHub Discussions

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add tests untuk fitur baru
- Update documentation
- Be respectful dan constructive

## 📄 License

AloPantest dilisensikan di bawah **MIT License** untuk keperluan **Edukasi dan Penelitian Cybersecurity**.

```
Copyright (c) 2024 AloPantest Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

[Baca lisensi lengkap](LICENSE)

## ⚖️ Legal Disclaimer

**Disclaimer Penting:**

Pengembang AloPantest TIDAK bertanggung jawab atas:
- Penyalahgunaan tool untuk tujuan ilegal
- Damage atau kerugian yang ditimbulkan
- Violation of laws atau regulations
- Unauthorized access ke sistem

Dengan menggunakan AloPantest, Anda setuju bahwa Anda akan menggunakan tool ini **secara etis dan legal**.

## 🎓 Learning Resources

### Recommended Learning Path
1. Basic Networking
2. Web Technologies (HTTP, HTML, CSS, JavaScript)
3. Security Fundamentals
4. Penetration Testing Methodology
5. Tool Usage & Automation
6. Advanced Exploitation
7. Report Writing & Communication

### External Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)

## 🚀 Roadmap

### v1.1.0 (Coming Soon)
- [ ] GUI Interface (Qt/Tkinter)
- [ ] Docker Support
- [ ] API Authentication
- [ ] Database Integration
- [ ] Report Generation

### v1.2.0
- [ ] Advanced Fuzzing Tools
- [ ] Advanced Exploitation
- [ ] Mobile App Security Tools
- [ ] Cloud Security Tools
- [ ] AI-powered vulnerability detection

### v2.0.0
- [ ] Distributed Testing
- [ ] Real-time Collaboration
- [ ] Advanced Analytics
- [ ] Custom Dashboards
- [ ] Enterprise Features

## 📊 Statistics

- **Total Tools**: 30+
- **Lines of Code**: 5000+
- **Supported Platforms**: 5+
- **Programming Language**: Python 3.8+
- **License**: MIT (Educational)

## 🙏 Acknowledgments

Terima kasih kepada:
- Security community
- Open source contributors
- Educational institutions
- All users and testers

## 📮 Contact & Feedback

Kirim feedback atau saran:
- Email: feedback@alopantest.com
- GitHub Discussions: [Link]
- Twitter: [@AloPantest]
- LinkedIn: [Company Page]

---

**Made with ❤️ for Cybersecurity Education**

**Last Updated**: Desember 2024
**Version**: 1.0.0
**Status**: Active Development

---

## Quick Command Reference

```bash
# Installation
pip install -r requirements.txt

# Running
python alo_pantest_cli.py run <tool-id> [OPTIONS]

# List tools
python alo_pantest_cli.py list-tools

# Get info
python alo_pantest_cli.py info

# Get tool help
python alo_pantest_cli.py help-tool <tool-id>

# Export results
python alo_pantest_cli.py run <tool-id> --output results.json
```

---

**Happy Testing! Stay Ethical! 🛡️**
