# AleoPantest v3.0 - Advanced Penetration Testing Framework

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  AleoPantest v3.0 - Penetration Testing  🛡️        ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║       400+ Tools • Multi-Platform • Modern TUI • V3.0 PRO     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**AleoPantest** is an advanced, modular penetration testing framework designed for security professionals and ethical hackers. Version 3.0 introduces a modern TUI dashboard, intelligent automation, and enhanced cross-platform support.

---

## 📚 Documentation Hub

Explore the full documentation to get the most out of AleoPantest.

### 🚀 Getting Started
*   [**Start Here**](00-START-HERE.md) - Overview of v2.0 release and new features.
*   [**Installation Guide**](INSTALL_GUIDE.md) - Detailed installation instructions for all platforms.
*   [**Quick Start Guide**](QUICKSTART_GUIDE.md) - Get up and running in minutes.
*   [**Installation (ID)**](INSTALLATION.md) - Panduan instalasi dalam Bahasa Indonesia.

### 📖 User Guides
*   [**Interactive CLI Guide**](INTERACTIVE_CLI_GUIDE.md) - Master the new interactive command-line interface.
*   [**Advanced Features**](ADVANCED_FEATURES.md) - Deep dive into advanced capabilities.
*   [**Testing Guide**](TESTING_GUIDE.md) - How to run tests and verify the system.
*   [**Tools Reference**](docs/TOOLS.md) - Complete reference for all 400+ tools.

### � Project Reports & Status
*   [**Project Summary**](PROJECT_SUMMARY.md) - High-level project overview.
*   [**Implementation Summary**](IMPLEMENTATION_SUMMARY.md) - Technical details of implementation.
*   [**Feature Checklist**](FEATURE_CHECKLIST.md) - Status of all planned features.
*   [**Changelog**](CHANGELOG.md) - History of changes and updates.
*   [**Build Report**](BUILD_REPORT.md) - Build status and verification.
*   [**Python 3.9+ Fix Report**](PYTHON39_FIX_REPORT.md) - Details on compatibility fixes.
*   **v3.3.2 Admin Update**: Enhanced admin detection and environment adapter for multi-stage deployment.
*   **v3.3.1 Stability Update**: Robustness fixes for undefined/null errors across API, Web, TUI, and CLI.

---

## ⚡ Quick Installation

```bash
# Clone the repository
git clone https://github.com/ZetaGo-Aurum/AleoPantest.git
cd AleoPantest

# Install dependencies
pip install -r requirements.txt

# Install as CLI tool
pip install -e .
```

For detailed instructions, see [INSTALL_GUIDE.md](INSTALL_GUIDE.md).

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

More examples in [QUICKSTART_GUIDE.md](QUICKSTART_GUIDE.md).

## 🌟 Key Features

*   **Modular Architecture**: Easy to extend and maintain.
*   **Interactive CLI**: User-friendly interface with auto-completion and rich output.
*   **Cross-Platform**: Works on Windows, Linux, and macOS.
*   **Comprehensive Toolset**: Covering Network, Web, OSINT, Phishing, and more.

## 🤝 Contributing

Contributions are welcome! Please check the [Project Summary](PROJECT_SUMMARY.md) for roadmap and [Testing Guide](TESTING_GUIDE.md) for standards.

## 📄 License

This project is licensed under the [LICENSE](LICENSE) file.
