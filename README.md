# Aleopantest V3.0 (Major Patch) - Advanced Penetration Testing Framework
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  Aleopantest V3.0.0 - by Aleocrophic  🛡️          ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║      400+ Tools • Multi-Platform • Modern TUI • V3.0.0 PRO    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Aleopantest** (by Aleocrophic) is an advanced, modular penetration testing framework designed for security professionals and ethical hackers. Version 3.3.5 introduces a modern TUI dashboard, intelligent automation, and enhanced cross-platform support.

---

## 📚 Documentation Hub

Explore the full documentation to get the most out of **Aleopantest**.

### 🚀 Getting Started
*   [**Start Here**](00-START-HERE.md) - Overview of v2.0 release and new features.
*   [**Installation Guide**](INSTALL_GUIDE.md) - Detailed installation instructions for all platforms.
*   [**Quick Start Guide**](QUICKSTART_GUIDE.md) - Get up and running in minutes.

### 📖 User Guides
*   [**Interactive CLI Guide**](INTERACTIVE_CLI_GUIDE.md) - Master the new interactive command-line interface.
*   [**Advanced Features**](ADVANCED_FEATURES.md) - Deep dive into advanced capabilities.
*   [**Testing Guide**](TESTING_GUIDE.md) - How to run tests and verify the system.
*   [**Tools Reference**](docs/TOOLS.md) - Complete reference for all 400+ tools.

### 📊 Project Reports & Status
*   [**Project Summary**](PROJECT_SUMMARY.md) - High-level project overview.
*   [**Implementation Summary**](IMPLEMENTATION_SUMMARY.md) - Technical details of implementation.
*   [**Feature Checklist**](FEATURE_CHECKLIST.md) - Status of all planned features.
*   [**Changelog**](CHANGELOG.md) - History of changes and updates.
*   [**Build Report**](BUILD_REPORT.md) - Build status and verification.
*   [**Python 3.9+ Fix Report**](PYTHON39_FIX_REPORT.md) - Details on compatibility fixes.

---

## ⚡ Installation

### Prerequisites
- Python 3.8 or higher
- Pip (Python Package Installer)
- Git (optional, for cloning)

### Standard Installation
```bash
# Clone the repository
git clone https://github.com/ZetaGo-Aurum/aleopantest.git
cd aleopantest

# Install dependencies
pip install -r requirements.txt

# Install as CLI tool (recommended)
pip install -e .
```

### Dependency Overview
Aleopantest relies on several core libraries:
- **CLI/TUI**: `click`, `rich`, `textual`, `typer`
- **Networking**: `scapy`, `requests`, `nmap`, `paramiko`
- **Web**: `beautifulsoup4`, `selenium`, `httpx`
- **OSINT**: `shodan`, `geoip2`, `googlesearch-python`
- **Security**: `cryptography`, `passlib`, `bcrypt`

For a full list, see [requirements.txt](requirements.txt).

---

## 🎮 Usage Examples

### Basic Commands
```bash
aleopantest --help          # Show help menu
aleopantest list-tools      # List all available tools
aleopantest info            # Show system info
```

### Running Tools
```bash
# SQL Injection Scan
aleopantest run sql-inject --url http://example.com

# Phishing Detection
aleopantest run web-phishing --url http://suspicious-site.com

# DNS Lookup
aleopantest run dns --domain target.com
```

---

## 🛠️ Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Ensure you've run `pip install -e .` to register the package.
2. **Permission Denied**: Some network tools (like packet sniffing or port scanning) may require administrator/root privileges. Run with `sudo` (Linux/macOS) or as Administrator (Windows).
3. **Dependency Conflicts**: It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```

---

## ⚖️ Terms of Service & Legal

The use of **Aleopantest** is governed by strict legal terms to ensure ethical and responsible usage.

Aleopantest is developed exclusively for **educational purposes, security research, and ethical hacking**. Users are strictly prohibited from using this tool on systems or networks without explicit written permission from the system owner. Any unauthorized use may be considered a serious legal violation.

The developers and contributors are **not responsible** for any misuse, illegal activities, or damages caused by this software. Users bear full responsibility for compliance with local and international laws, including but not limited to:
- **UU ITE** (Indonesia)
- **CFAA** (United States)
- **GDPR** (European Union)

For complete information regarding liability limitations, jurisdictional clauses, and user obligations, please read the full **[Terms of Service](TERMS_OF_SERVICE.md)** document.

---

## 🌟 Key Features

*   **Modular Architecture**: Easy to extend and maintain.
*   **Interactive CLI**: User-friendly interface with auto-completion and rich output.
*   **Cross-Platform**: Works on Windows, Linux, and macOS.
*   **Intelligent Automation**: Context-aware parameter filling and optimization.
*   **Standardized Output**: Consistent JSON reporting for all 400+ tools.

---

## 🤝 Contributing

Contributions are welcome! Please check the [Project Summary](PROJECT_SUMMARY.md) for roadmap and [Testing Guide](TESTING_GUIDE.md) for standards.

## 📄 License

This project is licensed under the [LICENSE](LICENSE) file.

---
**Aleopantest V3.0.0**
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>
