<div align="center">

# 🛡️ AleoPantest V4.0.0 PRO (Codename: HYDRA)
*Advanced Penetration Testing & Cybersecurity Framework*

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OS Supported](https://img.shields.io/badge/os-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Kali%20%7C%20Termux-brightgreen?style=for-the-badge&logo=linux&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)]()

**548+ Specialized Tools** • **Cross-Platform** • **Modern CLI, TUI & Web Dashboard**
<br>
<div style="font-size: 80%; color: #666666;">by Aleocrophic Team</div>

</div>

---

## 🧭 Navigation
- [✨ Features](#-features)
- [⚡ Quick Start & Universal Installation](#-quick-start--universal-installation)
- [🧩 Tool Categories (548+ Tools)](#-tool-categories)
- [🖥️ Interfaces (CLI, TUI, Web)](#-interfaces-cli-tui-web)
- [📚 Documentation Directory](#-documentation-directory)
- [⚖️ License & Terms](#%EF%B8%8F-license--terms-of-service)

---

## ✨ Features

**Aleopantest** (by Aleocrophic) is an advanced, modular penetration testing framework designed for security professionals, system administrators, and ethical hackers. Version 4.0.0 (HYDRA) marks a massive overhaul:

- 🚀 **548+ Specialized Tools**: Covering everything from OSINT and Web Exploitation to Cloud Security, Active Directory, and IoT.
- 🌐 **Global Command Alias**: Call the framework from anywhere using `alpnts` or `aleopantest`.
- 🖥️ **Three distinct interfaces**: A rich, robust **CLI**, a modern Text-based User Interface (**TUI**), and a responsive **Web Dashboard**.
- 🤖 **Intelligent Automation**: Context-aware parameter filling, allowing seamless tool chaining without manual input.
- 📊 **Standardized Reporting**: Every tool outputs consistent JSON, TXT, or PDF formats, ready for compliance audits.
- 🌍 **True Cross-Platform**: Optimized specifically for standard OS (Windows, Linux, macOS) AND specialized environments (Kali Linux, Parrot OS, WSL, Termux).

---

## ⚡ Quick Start & Universal Installation

AleoPantest is designed to be universally compatible. Follow these simple steps for your environment.

### 📋 Prerequisites
- **Python 3.9** or higher installed. (Run `python3 --version` or `python --version` to check)
- **Git** (To clone the repository)

### 🚀 Universal Install Guide (Linux, Windows, macOS, Kali, WSL)

Open your terminal or command prompt and run:

```bash
# 1. Clone the repository
git clone https://github.com/ZetaGo-Aurum/AleoPantest.git
cd AleoPantest

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Register the global CLI commands (`aleopantest` and `alpnts`)
pip install -e .

# 4. Verify installation
alpnts --version
```

### 📱 Termux Install Guide (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git clang libxml2 libxslt libffi openssl -y
git clone https://github.com/ZetaGo-Aurum/AleoPantest.git
cd AleoPantest
MATHLIB=m pip install -r requirements.txt
pip install -e .
alpnts --version
```

> **Note:** If you encounter permission issues on Linux/macOS during step 3, try running `pip install --user -e .` instead.

---

## 🧩 Tool Categories

AleoPantest V4.0.0 comes equipped with **548** fully functioning tools spanning **31** distinct categories. Use `alpnts list-tools` to see them all.

| Core Security | Advanced Security | Utilities & Compliance |
|---------------|-------------------|------------------------|
| 🌐 Web Security | ☁️ Cloud Security | 📜 Reporting |
| 📡 Network & WiFi | 🐋 Container Security | ⚖️ Compliance & Audit |
| 🕵️ OSINT | 🏰 Active Directory | ⚙️ Automation |
| 🔐 Password/Auth | 🧬 Binary Analysis | 🛠️ Miscellaneous |
| 🔑 Cryptography | 🧩 API Security | 📱 Mobile Security |
| 🛡️ Exploit/Post-Exploit| 🕵️ Forensics | 🎭 Social Engineering |

*(For a full list of tools, refer to [docs/TOOLS.md](docs/TOOLS.md))*

---

## 🖥️ Interfaces (CLI, TUI, Web)

AleoPantest adapts to your workflow. Use the interface that best suits your current task.

### 1. The Rich CLI
Perfect for quick scans, automation scripts, and CI/CD pipelines.
```bash
alpnts list-tools                   # View the list of all 548 tools
alpnts run dns --domain zeta.com    # Run a specific tool
alpnts run sql-inject -i            # Run a tool in interactive mode
alpnts --license                    # View the license
alpnts info                         # Print framework stats
```

### 2. The Modern TUI (Terminal User Interface)
For a visual, keyboard-driven dashboard directly in your terminal.
```bash
alpnts tui
```

### 3. The Web Dashboard
For a graphical interface with visualization, reporting features, and centralized logs.
```bash
alpnts web --port 8002
```
Access the dashboard via your browser at `http://127.0.0.1:8002`.

---

## 📚 Documentation Directory

Explore the rest of the documentation for advanced setups, technical reports, and historical changes:

- [CHANGELOG_V4](CHANGELOG_V4.md) - **NEW!** See all the massive upgrades in V4.0.0 HYDRA.
- [docs/TOOLS](docs/TOOLS.md) - Complete list of security tools.
- [INDEX](INDEX.md) - Master index of documentation.
- [ADVANCED_FEATURES](ADVANCED_FEATURES.md) - Deep dive into core features.
- [MIGRATION_GUIDE](MIGRATION_GUIDE.md) - Guide for upgrading from previous versions.
- [INTERACTIVE_CLI_GUIDE](INTERACTIVE_CLI_GUIDE.md) - Mastering the CLI and `alpnts`.

---

## ⚖️ License & Terms of Service

AleoPantest is developed strictly for **educational purposes, authorized auditing, and ethical hacking**.

By using this software, you agree to the [Terms of Service](TERMS_OF_SERVICE.md). Any misuse of this tool is strictly prohibited, and the authors hold no liability for damages.

This project is licensed under the **MIT License**. Read the full [LICENSE](LICENSE) file for more information.

<div align="center">
  <br>
  <i>Empowering Security Teams. Elevating Defenses.</i>
</div>
