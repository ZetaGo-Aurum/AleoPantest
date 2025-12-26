"""Web module initialization"""
from .sql_injector import SQLInjector
from .xss_detector import XSSDetector
from .csrf_detector import CSRFDetector
from .web_crawler import WebCrawler
from .vulnerability_scanner import VulnerabilityScanner
from .subdomain_finder import SubdomainFinder
from .advanced_dorking import AdvancedDorking
from .tech_stack import TechStack
from .dir_brute import DirBrute
from .link_extract import LinkExtractor
from .admin_finder import AdminFinder
from .headers_analyzer import HeadersAnalyzer
from .proxy_finder import ProxyFinder
from .api_analyzer import APIAnalyzer

__all__ = [
    'SQLInjector',
    'XSSDetector',
    'CSRFDetector',
    'WebCrawler',
    'VulnerabilityScanner',
    'SubdomainFinder',
    'AdvancedDorking',
    'TechStack',
    'DirBrute',
    'LinkExtractor',
    'AdminFinder',
    'HeadersAnalyzer',
    'ProxyFinder',
    'APIAnalyzer'
]
