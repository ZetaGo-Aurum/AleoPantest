"""
Aleopantest - Advanced Penetration Testing Framework
by Aleocrophic
Version: 4.0.0
Author: Aleocrophic Team
Description: Comprehensive penetration testing tool suite with 900+ tools
License: MIT (For Educational Purposes Only)
"""

__version__ = "4.0.1"
__author__ = "Aleocrophic Team"
__license__ = "MIT - Educational Use Only"
__codename__ = "HYDRA"

from .core.logger import setup_logger

logger = setup_logger(__name__)
