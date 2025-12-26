# INSTALLATION GUIDE - Aleocrophic

Panduan lengkap instalasi Aleocrophic di berbagai platform.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Windows Installation](#windows-installation)
- [Linux/Ubuntu/Debian Installation](#linuxubuntudebian-installation)
- [macOS Installation](#macos-installation)
- [Termux Installation (Android)](#termux-installation-android)
- [WSL (Windows Subsystem for Linux)](#wsl-windows-subsystem-for-linux)
- [Docker Installation](#docker-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Windows, Linux, macOS, atau Android (Termux)
- **Python**: 3.8 atau lebih tinggi
- **RAM**: Minimum 512MB (2GB recommended)
- **Disk Space**: 100MB untuk instalasi
- **Internet**: Koneksi internet (untuk beberapa tools)

### Check Python Version
```bash
python --version
# atau
python3 --version
```

Jika Python belum terinstall, download dari [python.org](https://www.python.org/downloads/)

---

## Windows Installation

### Method 1: Native Installation (Recommended for Windows)

#### Step 1: Download dan Install Python
1. Kunjungi [python.org](https://www.python.org/downloads/)
2. Download Python 3.10+ untuk Windows
3. Run installer
4. **PENTING**: Centang "Add Python to PATH"
5. Click "Install Now"

#### Step 2: Download Aleocrophic
```powershell
# Option A: Using Git
git clone https://github.com/ZetaGo-Aurum/Aleocrophic.git
cd Aleocrophic

# Option B: Manual Download
# Download dari GitHub dan extract ke folder
cd C:\Users\YourUsername\Aleocrophic
```

#### Step 3: Install Dependencies
```powershell
# Buka PowerShell atau Command Prompt
cd C:\Users\YourUsername\Aleocrophic

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Verify Installation
```powershell
python aleo_pantest_cli.py info
```

#### Step 5: Run Tools
```powershell
# List all tools
python aleo_pantest_cli.py list-tools

# Run port scanner
python aleo_pantest_cli.py run port-scan --host 192.168.1.1
```

### Method 2: WSL Installation (Recommended for Advanced Users)

**WSL (Windows Subsystem for Linux)** memberikan Linux environment di Windows dengan better compatibility.

#### Step 1: Enable WSL
```powershell
# Run PowerShell as Administrator
wsl --install

# Restart komputer jika diperlukan
```

#### Step 2: Install Ubuntu dalam WSL
```powershell
wsl --install -d Ubuntu

# Set default user dan password
```

#### Step 3: Follow Linux Installation
Setelah WSL terinstall, ikuti "Linux/Ubuntu/Debian Installation" di bawah.

---

## Linux/Ubuntu/Debian Installation

### Step 1: Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 2: Install Python dan Dependencies
```bash
# Install Python3 dan pip
sudo apt-get install python3 python3-pip python3-dev -y

# Install additional dependencies
sudo apt-get install git build-essential libssl-dev -y
```

### Step 3: Download Aleocrophic
```bash
# Clone repository
git clone https://github.com/ZetaGo-Aurum/Aleocrophic.git
cd Aleocrophic

# Atau manual download dan extract
# cd ~/Aleocrophic
```

### Step 4: Install Python Requirements
```bash
pip3 install -r requirements.txt

# Atau dengan sudo (jika diperlukan)
sudo pip3 install -r requirements.txt
```

### Step 5: Make CLI Executable
```bash
chmod +x aleo_pantest_cli.py
```

### Step 6: Verify Installation
```bash
./aleo_pantest_cli.py info
# atau
python3 aleo_pantest_cli.py info
```

### Step 7: Optional - System-wide Installation
```bash
# Install as system command
sudo pip3 install -e .

# Then run dari anywhere
Aleocrophic info
```

---

## macOS Installation

### Step 1: Install Homebrew (jika belum)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python
```bash
brew install python@3.11

# Verify
python3 --version
```

### Step 3: Download Aleocrophic
```bash
# Clone atau download
git clone https://github.com/ZetaGo-Aurum/Aleocrophic.git
cd Aleocrophic
```

### Step 4: Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 5: Make Executable
```bash
chmod +x aleo_pantest_cli.py
```

### Step 6: Verify dan Run
```bash
python3 aleo_pantest_cli.py info
./aleo_pantest_cli.py list-tools
```

### Step 7: Optional - Create Alias
```bash
# Edit ~/.zshrc atau ~/.bash_profile
echo "alias Aleocrophic='python3 ~/Aleocrophic/aleo_pantest_cli.py'" >> ~/.zshrc

# Apply
source ~/.zshrc

# Usage
Aleocrophic info
```

---

## Termux Installation (Android)

Termux memungkinkan Anda menjalankan Aleocrophic di Android phone/tablet.

### Step 1: Install Termux
1. Download Termux dari [F-Droid](https://f-droid.org/packages/com.termux/)
   - **PENTING**: Jangan dari Google Play Store (outdated)
2. Install dan open Termux app

### Step 2: Update Termux Packages
```bash
pkg update
pkg upgrade
```

### Step 3: Install Python
```bash
pkg install python3 python3-pip git

# Verify
python3 --version
```

### Step 4: Download Aleocrophic
```bash
# Clone atau download
git clone https://github.com/ZetaGo-Aurum/Aleocrophic.git
cd Aleocrophic

# Atau manual
# Download dan extract ke ~/Aleocrophic
```

### Step 5: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 6: Run Aleocrophic
```bash
python3 aleo_pantest_cli.py info

# List tools
python3 aleo_pantest_cli.py list-tools

# Run tool
python3 aleo_pantest_cli.py run ping --host 8.8.8.8
```

### Step 7: Optional - Storage Access
```bash
# Request storage permission
termux-setup-storage

# Access files
cd ~/storage/downloads
```

---

## WSL (Windows Subsystem for Linux)

WSL memberikan Linux environment penuh di Windows. Recommended untuk power users.

### Step 1: Enable WSL (Windows 10/11)
```powershell
# Run PowerShell as Administrator
wsl --install

# Or install specific distribution
wsl --install -d Ubuntu-22.04
```

### Step 2: Setup WSL User
```bash
# First time WSL runs, setup user and password
# (Akan otomatis saat pertama kali open Ubuntu)
```

### Step 3: Update WSL System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 4: Install Python (dalam WSL)
```bash
sudo apt-get install python3 python3-pip git -y
```

### Step 5: Install Aleocrophic
```bash
git clone https://github.com/ZetaGo-Aurum/Aleocrophic.git
cd Aleocrophic
pip3 install -r requirements.txt
```

### Step 6: Run dari Windows PowerShell
```powershell
# Run WSL tool dari Windows
wsl python3 ~/Aleocrophic/aleo_pantest_cli.py info
```

---

## Docker Installation

### Step 1: Install Docker
- **Windows**: Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- **Linux**: `sudo apt-get install docker.io`
- **macOS**: Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

### Step 2: Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "aleo_pantest_cli.py"]
```

### Step 3: Build Docker Image
```bash
docker build -t Aleocrophic:latest .
```

### Step 4: Run Container
```bash
# Interactive mode
docker run -it Aleocrophic:latest info

# Run specific tool
docker run -it Aleocrophic:latest run port-scan --host 192.168.1.1

# With volume mount
docker run -it -v /home/user/output:/app/output Aleocrophic:latest run port-scan --host 192.168.1.1 --output /app/output/results.json
```

---

## Verification

### Verify Installation
```bash
# Check Python
python3 --version

# Check pip packages
pip3 list | grep -E 'click|rich|requests'

# Check Aleocrophic
python3 aleo_pantest_cli.py info
```

### Test Tools
```bash
# Test basic tools
python3 aleo_pantest_cli.py run passgen
python3 aleo_pantest_cli.py run hash --text "test" --algorithm sha256
python3 aleo_pantest_cli.py run encode --text "hello" --operation encode
```

---

## Troubleshooting

### Error: "python: command not found"
**Solution**: Install Python dari [python.org](https://python.org)
```bash
# Linux
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# Windows
# Download dari python.org dan install
```

### Error: "No module named 'click'"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Error: "Permission denied" (Linux/macOS)
**Solution**: Make script executable
```bash
chmod +x aleo_pantest_cli.py
./aleo_pantest_cli.py info
```

### Error: "ModuleNotFoundError: No module named 'aleo_pantest'"
**Solution**: Run dari directory Aleocrophic
```bash
cd Aleocrophic
python3 aleo_pantest_cli.py info
```

### Error: "SSL: CERTIFICATE_VERIFY_FAILED"
**Solution 1**: Update certificates
```bash
pip install --upgrade certifi
```

**Solution 2**: Workaround (tidak recommended)
```bash
pip install certifi
python3 -m pip install --upgrade pip
```

### Error: "Port already in use" (Server)
**Solution**: Use different port
```bash
python3 aleo_pantest_cli.py server --port 8000
```

### Network Issues Behind Proxy
**Solution**: Configure pip untuk proxy
```bash
pip install -r requirements.txt -i https://pypi.org/simple/ --proxy [user:passwd@]proxy.server:port
```

### Performance Issues
**Solution**: Check system resources
```bash
# Linux
free -h  # Memory
df -h    # Disk

# macOS
vm_stat

# Windows
systeminfo
```

### Import Errors untuk Network Tools
```bash
# Some network tools require system packages
# Linux
sudo apt-get install net-tools nmap

# macOS
brew install nmap

# Windows
# Download dari nmap.org
```

---

## Post-Installation

### Setup Configuration
```bash
# Create custom config
mkdir -p config
cp config/default.yml config/settings.yml

# Edit config
nano config/settings.yml
```

### Create Output Directory
```bash
mkdir -p output logs
chmod 755 output logs
```

### Test Specific Tool
```bash
# Network tools
python3 aleo_pantest_cli.py run ping --host 8.8.8.8

# Web tools
python3 aleo_pantest_cli.py run dns --domain google.com

# Utilities
python3 aleo_pantest_cli.py run hash --text "password" --algorithm sha256
```

---

## Next Steps

1. **Read Documentation**: Lihat [README.md](README.md)
2. **List Tools**: `python3 aleo_pantest_cli.py list-tools`
3. **Get Tool Help**: `python3 aleo_pantest_cli.py help-tool <tool-id>`
4. **Start Testing**: Run tools sesuai kebutuhan

---

## Support

- **Issues**: Open GitHub issue
- **Questions**: Email support@Aleocrophic.com
- **Community**: Join Discord server
- **Docs**: [Aleocrophic Documentation](https://docs.Aleocrophic.com)

---

**Happy Installation! 🚀**

Last Updated: Desember 2024
