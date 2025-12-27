# Aleopantest V3.0 (Major Patch) - Advanced Penetration Testing Framework
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>

---

## 🧭 Document Navigation List

This section provides a complete navigation map to all documentation files in this repository. You can use these links to quickly jump to specific guides, technical reports, or legal documents.

### 🚀 Getting Started & Core
- [README](README.md) - Main framework documentation
- [00-START-HERE](00-START-HERE.md) - Initial entry point for new users
- [README_START_HERE](README_START_HERE.md) - Alternative quick start guide
- [INDEX](INDEX.md) - Master index of documentation
- [MANIFEST](MANIFEST.md) - Project manifest and file structure

### 📖 User Guides
- [INSTALLATION](INSTALLATION.md) - Detailed installation steps
- [INSTALL_GUIDE](INSTALL_GUIDE.md) - Step-by-step setup walkthrough
- [QUICKSTART](QUICKSTART.md) - Fast-track usage guide
- [QUICKSTART_GUIDE](QUICKSTART_GUIDE.md) - Comprehensive quick start instructions
- [INTERACTIVE_CLI_GUIDE](INTERACTIVE_CLI_GUIDE.md) - Guide for the interactive terminal interface
- [TESTING_GUIDE](TESTING_GUIDE.md) - Instructions for running tests and verification
- [docs/TOOLS](docs/TOOLS.md) - Complete list of 400+ security tools

### 🛠️ Technical & Development
- [ADVANCED_FEATURES](ADVANCED_FEATURES.md) - Deep dive into V3.0 features
- [CHANGELOG](CHANGELOG.md) - Version history and updates
- [CHANGELOG_UI_UPDATE](CHANGELOG_UI_UPDATE.md) - Specific changes for the UI overhaul
- [CHANGES_V33](CHANGES_V33.md) - Recent updates in version 3.3
- [MIGRATION_GUIDE](MIGRATION_GUIDE.md) - Guide for upgrading from previous versions
- [FEATURE_CHECKLIST](FEATURE_CHECKLIST.md) - Status of various framework features
- [docs/FIX_NONE_TYPE_ERROR](docs/FIX_NONE_TYPE_ERROR.md) - Technical report on attribute error fixes
- [PYTHON39_FIX_REPORT](PYTHON39_FIX_REPORT.md) - Compatibility fixes for Python 3.9

### 📊 Reports & Status
- [PROJECT_SUMMARY](PROJECT_SUMMARY.md) - High-level overview of project achievements
- [IMPLEMENTATION_SUMMARY](IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [COMPLETION_REPORT](COMPLETION_REPORT.md) - Final project completion status
- [BUILD_REPORT](BUILD_REPORT.md) - Framework build and compilation details

### ⚖️ Legal & Compliance
- [TERMS_OF_SERVICE](TERMS_OF_SERVICE.md) - Terms of use and legal disclaimers

---

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

## 📖 Project Overview

Aleopantest is a comprehensive solution for security testing that covers various phases of assessment, from information gathering (reconnaissance) to exploitation and reporting. With its plugin-based architecture, users can easily add new tools or integrate existing ones into an automated workflow.

### Key Features:
- **Modular Architecture**: Easy to extend and maintain via a robust plugin system.
- **Interactive CLI & TUI**: User-friendly interface with auto-completion, rich terminal output, and a modern dashboard.
- **Cross-Platform Support**: Seamless operation on Windows, Linux, and macOS.
- **Intelligent Automation**: Context-aware parameter filling and performance optimization.
- **Standardized Reporting**: Consistent JSON and PDF reporting for over 400 specialized tools.

---

## ⚡ Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Pip (Python Package Installer)
- Git (optional, for cloning the repository)

### Standard Installation
```bash
# Clone the repository
git clone https://github.com/ZetaGo-Aurum/aleopantest.git
cd aleopantest

# Install dependencies
pip install -r requirements.txt

# Install as a CLI tool (recommended)
pip install -e .
```

---

## ⚙️ Configuration Details

Aleopantest uses configuration files to manage framework behavior and third-party API integrations.

### 1. Environment Variables (`.env`)
Copy `.env.example` to `.env` and fill in the required API keys:
```env
SHODAN_API_KEY=your_key_here
CENSYS_ID=your_id
CENSYS_SECRET=your_secret
VIRUSTOTAL_API_KEY=your_key
```

### 2. YAML Configuration (`config/default.yml`)
You can customize default settings such as timeouts, user-agents, and output paths:
```yaml
network:
  timeout: 30
  max_retries: 3
  user_agent: "Aleopantest/3.3.5"
output:
  format: json
  directory: ./results
```

---

## 🎮 Usage Guidelines

### Basic CLI Commands
```bash
aleopantest --help          # Display the help menu
aleopantest list-tools      # List all available security tools
aleopantest info            # Show system and framework information
```

### Running Tools via CLI
```bash
# SQL Injection Scanning
aleopantest run sql-inject --url http://example.com

# Web Phishing Detection
aleopantest run web-phishing --url http://suspicious-site.com
```

### Using as a Python Library
Integrate Aleopantest modules directly into your custom Python scripts:

```python
from aleopantest.core.scanner import SecurityScanner

# Initialize the scanner
scanner = SecurityScanner()

# Run a scan on a target with specific modules
results = scanner.scan_target("http://example.com", modules=["sql_inject", "xss"])

# Process and print findings
for issue in results.vulnerabilities:
    print(f"Found: {issue.name} at {issue.location}")
```

---

## ⚖️ Terms of Service (ToS)

The use of **Aleopantest** is governed by the following legal terms. By using this software, you agree to be bound by these conditions.

### 1. Terms of Use
- Aleopantest is developed **exclusively for educational purposes, security research, and ethical hacking**.
- Unauthorized use of this tool on systems or networks without **explicit, written permission** from the system owner is strictly prohibited.
- Users assume full responsibility for all activities performed using this framework.

### 2. Limitation of Liability
- The developers and contributors **ARE NOT LIABLE** for any misuse, illegal activities, or damages caused by this software.
- This software is provided "AS IS" without warranty of any kind, express or implied.
- In no event shall the authors be liable for any claim, damages, or other liability arising from the use of the software.

### 3. Privacy Policy
- Aleopantest **does not collect or transmit personal data** to external servers.
- All scan results and sensitive data collected during testing are stored locally on the user's device.
- Users are responsible for handling collected data in compliance with applicable privacy regulations (e.g., GDPR).

### 4. Copyright Requirements
- Aleopantest is open-source software licensed under the **MIT License**.
- Copyright (c) 2024 Aleocrophic Team.
- You are permitted to copy, modify, and distribute this software as long as the original copyright notice and permission notice are included.

---

## 🤝 Contribution Rules

Contributions are highly welcome! To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add descriptive message'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request for review.

---

## 📄 Licensing Information

This project is licensed under the [MIT License](LICENSE).

---
**Aleopantest V3.0.0**
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>
