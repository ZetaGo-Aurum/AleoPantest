"""Web module initialization"""
from .sql_injector import SQLInjector
from .xss_detector import XSSDetector
from .csrf_detector import CSRFDetector
from .web_crawler import WebCrawler
from .vulnerability_scanner import VulnerabilityScanner
from .subdomain_finder import SubdomainFinder
from .advanced_dorking import AdvancedDorking

__all__ = [
    'SQLInjector',
    'XSSDetector',
    'CSRFDetector',
    'WebCrawler',
    'VulnerabilityScanner',
    'SubdomainFinder',
    'AdvancedDorking',
]
