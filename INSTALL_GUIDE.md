# AloPantest v2.0 Installation Guide

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning repository)
- 500MB free disk space
- Internet connection for dependencies

## 🚀 Quick Installation

### Option 1: From Source (Development)

```bash
# Clone repository
git clone https://github.com/ZetaGo-Aurum/AleoPantest.git
cd AloPantest

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install in development mode
pip install -e .

# Verify installation
aleopantest --help
```

### Option 2: From PyPI (When Available)

```bash
# Install from PyPI
pip install alopantest

# Verify installation
aleopantest --help
```

## 🔧 Setup Instructions

### 1. Prerequisites Check

Verify Python installation:
```bash
python --version
# Should show: Python 3.8 or higher
```

### 2. Virtual Environment Setup (Recommended)

Create isolated environment:
```bash
# Create virtual environment
python -m venv alopantest_env

# Activate it
# Windows:
alopantest_env\Scripts\activate
# Linux/Mac:
source alopantest_env/bin/activate
```

### 3. Install Dependencies

```bash
# Update pip
pip install --upgrade pip

# Install AloPantest
pip install -e .
# Or with all optional dependencies:
pip install -e ".[full]"
```

### 4. Verify Installation

```bash
# Check CLI accessibility
aleopantest --version

# List all tools
aleopantest list-tools

# Show help
aleopantest --help
```

## 📦 Dependency Installation

### Core Dependencies (Installed Automatically)
```
click>=8.1.7          # CLI framework
rich>=13.7.0          # Terminal formatting
pydantic>=2.5.0       # Data validation
python-dotenv>=1.0.0  # Environment variables
pyyaml>=6.0.1         # Configuration
requests>=2.31.0      # HTTP client
beautifulsoup4>=4.12.2 # HTML parsing
```

### Optional Dependencies

For specific tools:
```bash
# Web tools
pip install selenium>=4.0.0

# Database tools
pip install sqlalchemy>=2.0.0

# Crypto tools
pip install cryptography>=41.0.0

# OSINT tools
pip install shodan>=1.28.0
```

## 🛠️ Configuration

### 1. Create Config Directory

```bash
# Linux/Mac
mkdir -p ~/.alopantest
cp config/default.yml ~/.alopantest/

# Windows
mkdir %USERPROFILE%\.alopantest
copy config\default.yml %USERPROFILE%\.alopantest\
```

### 2. Set Environment Variables

Create `.env` file:
```bash
# API Keys (optional)
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key

# Configuration
LOG_LEVEL=INFO
OUTPUT_DIR=./output
```

### 3. Update Configuration

Edit `config/default.yml`:
```yaml
alopantest:
  version: 2.0.0
  log_level: INFO
  output_directory: ./output
  
tools:
  network:
    timeout: 30
  web:
    max_connections: 10
```

## 🔍 Troubleshooting

### Issue: "aleopantest: command not found"

**Solution:**
```bash
# Check virtual environment is activated
which python  # Should show path with venv

# Reinstall
pip install -e .

# Try running directly
python -m alo_pantest.cli --help
```

### Issue: Permission Denied

**Solution (Linux/Mac):**
```bash
# Make script executable
chmod +x ~/.venv/bin/aleopantest

# Or run with python
python -m alo_pantest.cli
```

### Issue: Module Not Found

**Solution:**
```bash
# Reinstall with dependencies
pip install -e . --force-reinstall

# Check installation
python -c "import alo_pantest; print(alo_pantest.__version__)"
```

### Issue: Network Tools Not Working

**Solution:**
```bash
# Install network tools dependencies
pip install scapy>=2.5.0
pip install nmap

# Verify network access
aleopantest run ping-tool --host 8.8.8.8
```

### Issue: Web Tools Not Scraping

**Solution:**
```bash
# Install web scraping dependencies
pip install selenium>=4.0.0
pip install playwright>=1.40.0

# Download browser drivers
playwright install
```

## 🌍 Installing from Different Locations

### From GitHub

```bash
# Latest development version
pip install git+https://github.com/ZetaGo-Aurum/AleoPantest.git

# Specific branch
pip install git+https://github.com/ZetaGo-Aurum/AleoPantest.git@develop

# Specific tag/release
pip install git+https://github.com/ZetaGo-Aurum/AleoPantest.git@v2.0.0
```

### From Offline Installation

```bash
# Download all dependencies
pip download -d ./wheels alopantest

# Install from wheels
pip install --no-index --find-links ./wheels alopantest
```

## 🐳 Docker Installation

### Build Docker Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

ENTRYPOINT ["aleopantest"]
```

### Build and Run

```bash
# Build image
docker build -t alopantest:2.0.0 .

# Run container
docker run -it --rm alopantest:2.0.0 --help

# Run with volume mount
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  alopantest:2.0.0 list-tools
```

## 🔄 Updating AloPantest

### Update from Source

```bash
# Pull latest changes
git pull origin main

# Reinstall
pip install -e . --upgrade

# Verify update
aleopantest --version
```

### Update via pip

```bash
# Update to latest
pip install alopantest --upgrade

# Update to specific version
pip install alopantest==2.0.0
```

## 🧪 Post-Installation Testing

### 1. Basic Functionality Test

```bash
# Show banner and help
aleopantest --help

# List available tools
aleopantest list-tools

# Get info about tools
aleopantest info
```

### 2. Test Specific Categories

```bash
# Test phishing tools
aleopantest list-by-category phishing

# Test clickjacking tools
aleopantest list-by-category clickjacking

# Test security tools
aleopantest list-by-category security
```

### 3. Run Sample Tool

```bash
# Test info command
aleopantest info

# Test a simple tool (email phishing)
aleopantest run email-phishing \
  --email test@example.com \
  --subject "Verify Account"

# Test network tool
aleopantest run ping-tool --host 8.8.8.8
```

## 🔐 Security Notes

### Best Practices

1. **Use Virtual Environment**
   ```bash
   python -m venv alopantest_env
   source alopantest_env/bin/activate  # Linux/Mac
   ```

2. **Keep Secure Config**
   ```bash
   # Don't commit .env with API keys
   echo ".env" >> .gitignore
   ```

3. **Restrict File Permissions**
   ```bash
   chmod 700 ~/.alopantest
   chmod 600 ~/.alopantest/config.yml
   ```

4. **Use Read-Only Installation**
   ```bash
   pip install --user alopantest  # Install for current user only
   ```

## 📞 Getting Help

### Documentation

- Main docs: [README.md](README.md)
- Quick start: [QUICKSTART_v2.md](QUICKSTART_v2.md)
- Release notes: [RELEASE_NOTES_v2.md](RELEASE_NOTES_v2.md)

### Commands

```bash
# General help
aleopantest --help

# Tool-specific help
aleopantest help-tool <tool-id>

# Category help
aleopantest list-by-category <category>
```

### Reporting Issues

1. Check documentation first
2. Search existing GitHub issues
3. Create detailed bug report including:
   - OS and Python version
   - Installation method
   - Exact command that failed
   - Error message (full traceback)
   - Steps to reproduce

## ✅ Installation Checklist

Before using AloPantest, verify:

- [ ] Python 3.8+ installed
- [ ] pip is up to date
- [ ] Virtual environment created (optional but recommended)
- [ ] AloPantest installed successfully
- [ ] `aleopantest --help` works
- [ ] `aleopantest list-tools` shows tools
- [ ] `aleopantest info` returns tool count
- [ ] Sample tool execution successful
- [ ] Configuration files in place
- [ ] Output directory created

## 🎉 Ready to Use!

Your AloPantest v2.0 installation is complete!

```bash
# Quick test
aleopantest --help

# Start exploring
aleopantest list-tools

# Try a tool
aleopantest run email-phishing --email test@example.com --subject "Test"
```

## 📚 Next Steps

1. Read [QUICKSTART_v2.md](QUICKSTART_v2.md) for usage examples
2. Explore tools with `aleopantest help-tool <tool-id>`
3. Check [RELEASE_NOTES_v2.md](RELEASE_NOTES_v2.md) for new features
4. Review security guidelines in [README.md](README.md)

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: team@alopantest.com
- **Wiki**: Check project wiki

---

**Last Updated:** December 25, 2025  
**Version:** 2.0.0  
**License:** MIT
