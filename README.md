# Aleopantest v3.3.5 - Advanced Penetration Testing Framework
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  Aleopantest v3.3.5 - by Aleocrophic  🛡️          ║
║                                                               ║
║              Advanced Cybersecurity Tool Suite                ║
║                                                               ║
║      400+ Tools • Multi-Platform • Modern TUI • V3.3.5 PRO    ║
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
*   **v3.3.3 API Standardization**: Fixed string-integer comparison errors and standardized JSON output format for all modules.
*   **v3.3.2 Admin Update**: Enhanced admin detection and environment adapter for multi-stage deployment.
*   **v3.3.1 Stability Update**: Robustness fixes for undefined/null errors across API, Web, TUI, and CLI.

---

## ⚡ Quick Installation

```bash
# Clone the repository
git clone https://github.com/ZetaGo-Aurum/aleopantest.git
cd aleopantest

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

## 🛠️ Standardization & Safety (v3.3+)

Starting from v3.3, Aleopantest implements strict parameter validation and standardized output across all modules.

### Parameter Validation
All high-risk tools now perform automatic type conversion and safety checks for duration parameters.
- **Duration**: Must be a positive integer (string inputs like `"60"` are automatically converted).
- **Safety Limit**: Intensive tasks are limited to a maximum of 3600 seconds (1 hour).

### Standardized JSON Output
Every module now returns a consistent JSON structure, making it easier for automation and web integration:

```json
{
  "status": "completed",
  "tool_metadata": {
    "name": "Beacon Flood",
    "risk_level": "HIGH",
    "version": "3.3.5"
  },
  "results": [...],
  "error_message": null,
  "execution_details": {
    "duration_seconds": 12.34,
    "results_count": 5,
    "errors_count": 0,
    "warnings_count": 0,
    "timestamp": "2025-12-27T00:33:54",
    "admin_info": {
      "username": "admin",
      "hostname": "localhost",
      "env": "local"
    }
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please check the [Project Summary](PROJECT_SUMMARY.md) for roadmap and [Testing Guide](TESTING_GUIDE.md) for standards.

## 📄 License

This project is licensed under the [LICENSE](LICENSE) file.

---
**Aleopantest v3.3.5**
<div style="font-size: 80%; color: #666666;">by Aleocrophic</div>
