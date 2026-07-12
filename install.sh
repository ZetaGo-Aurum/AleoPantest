#!/bin/bash
# Fast Install Script for AleoPantest V4.0.2 (HYDRA)
# Creates an isolated virtual environment so it works on systems with
# PEP 668 "externally-managed-environment" restrictions (Debian/Ubuntu/Termux).
# Optimized for Termux and low-RAM environments.

set -e

echo "[+] Starting AleoPantest Fast Install (venv mode)..."

# Determine python command
if command -v python3 &> /dev/null; then
    PY=python3
elif command -v python &> /dev/null; then
    PY=python
else
    echo "[-] Python 3 is required but was not found. Please install python3 first."
    exit 1
fi

# Create an isolated virtual environment
VENV_DIR="${ALEOPANTEST_HOME:-$HOME/.aleopantest/venv}"
echo "[+] Creating virtual environment at: $VENV_DIR"
mkdir -p "$(dirname "$VENV_DIR")"
if [ ! -d "$VENV_DIR" ]; then
    "$PY" -m venv "$VENV_DIR" || {
        echo "[!] venv module missing, attempting to install python3-venv..."
        sudo apt-get update -qq && sudo apt-get install -y python3-venv python3-full || true
        "$PY" -m venv "$VENV_DIR"
    }
fi

# Activate venv
source "$VENV_DIR/bin/activate"

echo "[+] Upgrading pip (venv)..."
pip install --upgrade pip setuptools wheel --no-cache-dir

echo "[+] Installing AleoPantest into the virtual environment..."
pip install --no-cache-dir -e .

# Create convenience symlinks on PATH if possible
if [ -w "$(dirname "$(command -v alpnts 2>/dev/null || echo /usr/local/bin/alpnts)")" ]; then
    ln -sf "$VENV_DIR/bin/alpnts" /usr/local/bin/alpnts
    ln -sf "$VENV_DIR/bin/aleopantest" /usr/local/bin/aleopantest 2>/dev/null || true
    echo "[+] Symlinked 'alpnts' to /usr/local/bin"
else
    echo "[+] Add venv to PATH: export PATH=\"$VENV_DIR/bin:\$PATH\""
fi

echo "[+] Installation complete!"
echo "[+] Run 'alpnts --version' to test (or: source $VENV_DIR/bin/activate && alpnts --version)"
