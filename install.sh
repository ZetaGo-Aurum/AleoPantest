#!/bin/bash
# Fast Install Script for Aleopantest V4.0.0 (HYDRA)
# Optimized for Termux and low-RAM environments

echo "[+] Starting Aleopantest Fast Install..."
echo "[+] Using --no-cache-dir to conserve RAM"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "[-] pip is not installed. Please install Python and pip first."
    exit 1
fi

# Install only the core dependencies first to prevent hanging
pip install setuptools wheel --no-cache-dir
pip install -r requirements.txt --no-cache-dir

# Install the package itself
pip install -e . --no-cache-dir

echo "[+] Installation complete!"
echo "[+] Run 'alpnts --version' to test."
