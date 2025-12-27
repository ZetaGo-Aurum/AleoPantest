#!/usr/bin/env python3
"""
Aleopantest - Comprehensive Penetration Testing Framework
by Aleocrophic
Entry point untuk aplikasi CLI
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from aleopantest.cli import cli, print_banner

if __name__ == '__main__':
    print_banner()
    cli()
