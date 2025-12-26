"""
Aleocrophic - Comprehensive Penetration Testing Framework
Version: 3.2.0
Author: Aleocrophic Team
Description: Advanced penetration testing tool suite with 400+ tools
License: MIT (For Educational Purposes Only)
"""

__version__ = "3.2.0"
__author__ = "Aleocrophic Team"
__license__ = "MIT - Educational Use Only"

from .core.logger import setup_logger

logger = setup_logger(__name__)
