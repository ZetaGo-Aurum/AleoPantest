"""
AleoPantest - Comprehensive Penetration Testing Framework
Version: 1.0.0
Author: Cybersecurity Team
Description: Advanced penetration testing tool suite with 360+ tools
License: MIT (For Educational Purposes Only)
"""

__version__ = "1.0.0"
__author__ = "AleoPantest Team"
__license__ = "MIT - Educational Use Only"

from .core.logger import setup_logger

logger = setup_logger(__name__)
