# CHANGELOG - Aleopantest V4.0.0 (Codename: HYDRA)

**Release Date:** February 2026  
**Author:** Aleocrophic Team

---

## 🚀 Major Changes

### Core Framework
- **Version bump**: V3.0.0 → V4.0.0, codename **HYDRA**
- **Python 3.9+** minimum requirement (supports 3.9–3.13)
- **Dependencies overhaul**: Removed broken/unmaintained packages (`requests-socks`, `scapy-radio`), updated all deps to latest stable versions, organized by category
- **`alpnts` alias**: Global shortcut command registered alongside `aleopantest`
- **Cross-platform support**: Enhanced detection for Windows, Linux, macOS, WSL, Kali, Parrot, Termux
- **Platform-specific optimizations**: Thread count, data directories, external tool detection

### 500+ New Tools (456 new tool files)
- **Active Directory** (30 tools): AD enumeration, Kerberoast, ASREPRoast, BloodHound ingest, GPP decrypt, ACL audit, LDAP search, delegation checks, and more
- **API Security** (35 tools): GraphQL introspection, REST fuzzer, API key leak scanner, JWT attack, OAuth tester, CORS tester, BOLA/IDOR testing, and more
- **Container Security** (25 tools): Docker audit, K8s pod scan, container escape detection, image scanning, Helm audit, RBAC audit, and more
- **Cloud Security** (38 tools): Multi-cloud (AWS/Azure/GCP) auditing, S3 bucket scanning, IAM privilege escalation, Terraform scanning, and more
- **Web Advanced** (40 tools): XXE, SSRF, SSTI, HTTP smuggling, cache poisoning, prototype pollution, DOM XSS, WAF bypass, and more
- **Network Advanced** (25 tools): BGP hijack detection, DNS tunneling, MITM detection, service auditing (Redis, Kafka, RabbitMQ), and more
- **Wireless Advanced** (20 tools): Evil twin detection, KRACK testing, Bluetooth/BLE scanning, Zigbee, SDR, WiFi enterprise audit
- **Binary Analysis** (25 tools): ELF analysis, ROP gadgets, heap analysis, fuzzer generation, shellcode, packer detection, decompiling
- **OSINT Advanced** (35 tools): Telegram/Discord/LinkedIn OSINT, certificate search, Wayback Machine, social media mapping, threat intel
- **Password & Auth** (30 tools): Password spraying, MFA bypass, session hijack detection, brute forcers (HTTP/SSH/FTP/RDP/SMTP/LDAP)
- **Forensics Advanced** (20 tools): Disk/registry/browser forensics, YARA scanning, PCAP analysis, deleted file recovery
- **Compliance & Audit** (25 tools): PCI-DSS, HIPAA, GDPR, ISO 27001, NIST, CIS benchmarks, threat modeling
- **Social Engineering** (15 tools): Phishing templates, vishing/smishing simulation, credential harvesting, deepfake detection
- **Mobile Security** (18 tools): Android/iOS analysis, Frida scripts, certificate pin bypass, mobile API testing
- **Reporting** (13 tools): Executive reports, CSV/XML/SARIF/Markdown export, dashboard generation
- **Automation** (20 tools): Auto-recon pipelines, parallel scanning, CI/CD integration, scan scheduling
- **Cryptography** (18 tools): AES/RSA attacks, padding oracle, TLS downgrade, blockchain analysis
- **Miscellaneous** (25 tools): C2 detection, honeypot detection, reverse shell generator, rootkit detection

### CLI Modernization
- **New ASCII art banner** with tool count and platform info
- **`--license` flag**: Display LICENSE directly from CLI
- **`--tos` flag**: Display Terms of Service from CLI
- **`--version` flag**: Show version, codename, platform, tool count
- **Click group-based commands**: `list-tools`, `info`, `run`, `tui`, `web`
- **Interactive mode** with parameter prompting

### Web Dashboard Fixes
- **Removed duplicate download route** that caused 500 errors
- **Added `/api/license` endpoint** for license display
- **Added `/api/tos` endpoint** for ToS display
- **Updated API title** to V4.0.0
- **Added dual-path endpoints** (e.g., `/api/report` and `/aleopantest/api/report`)

### Cross-Platform Enhancements
- **PlatformDetector**: Now detects Kali, Parrot, WSL2, Termux (improved), with caching
- **External tool checking**: `check_tool_available()` verifies nmap, sqlmap, hydra, etc.
- **Platform-specific data directories**: Proper paths for Windows (`%APPDATA%`), macOS (`~/Library`), Linux (`~/.local/share`)
- **Root/admin detection**: Cross-platform privilege checking

### Base Tool v4 Upgrades
- **12 new ToolCategory enum values**: Active Directory, API Security, Container, Binary, Password & Auth, Compliance, Automation, Reconnaissance, Web Advanced, Network Advanced, Wireless Advanced, Miscellaneous
- **`platform_support` field** in ToolMetadata for per-tool platform compatibility
- **V4 User-Agent header**: `Aleopantest/4.0.0 (Advanced Cybersecurity Framework)`
- **Dual certification**: `v4_certified: True` + backward-compatible `v3_certified: True`

---

## 📊 Statistics

| Metric | V3.0.0 | V4.0.0 |
|--------|--------|--------|
| Total Tools | ~92 | **548+** |
| Categories | 19 | **31** |
| Python Support | 3.8+ | **3.9–3.13** |
| Platforms | 3 | **6** (Win/Linux/macOS/WSL/Kali/Termux) |
| CLI Alias | — | **`alpnts`** |
| License/ToS via CLI | ❌ | ✅ |
| Web API Version | V3 | **V4** |

---

## ⚠️ Breaking Changes
- Minimum Python version raised to **3.9**
- Removed `requests-socks` dependency (use `pysocks` directly)
- CLI now uses `click.group` pattern (subcommands required)
- `TOOLS_REGISTRY` dict significantly expanded

## 📝 Migration Notes
- Run `pip install -r requirements.txt` to install updated dependencies
- Run `pip install -e .` to register the `alpnts` alias
- All V3 tools remain backward-compatible
