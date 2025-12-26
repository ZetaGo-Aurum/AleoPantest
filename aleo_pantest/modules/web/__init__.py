"""Web module initialization with robust error handling"""
from aleo_pantest.core.tool_helper import robust_import

SQLInjector = robust_import("aleo_pantest.modules.web.sql_injector", "SQLInjector")
XSSDetector = robust_import("aleo_pantest.modules.web.xss_detector", "XSSDetector")
CSRFDetector = robust_import("aleo_pantest.modules.web.csrf_detector", "CSRFDetector")
WebCrawler = robust_import("aleo_pantest.modules.web.web_crawler", "WebCrawler")
VulnerabilityScanner = robust_import("aleo_pantest.modules.web.vulnerability_scanner", "VulnerabilityScanner")
SubdomainFinder = robust_import("aleo_pantest.modules.web.subdomain_finder", "SubdomainFinder")
AdvancedDorking = robust_import("aleo_pantest.modules.web.advanced_dorking", "AdvancedDorking")
TechStack = robust_import("aleo_pantest.modules.web.tech_stack", "TechStack")
DirBrute = robust_import("aleo_pantest.modules.web.dir_brute", "DirBrute")
LinkExtractor = robust_import("aleo_pantest.modules.web.link_extract", "LinkExtractor")
AdminFinder = robust_import("aleo_pantest.modules.web.admin_finder", "AdminFinder")
HeadersAnalyzer = robust_import("aleo_pantest.modules.web.headers_analyzer", "HeadersAnalyzer")
ProxyFinder = robust_import("aleo_pantest.modules.web.proxy_finder", "ProxyFinder")
APIAnalyzer = robust_import("aleo_pantest.modules.web.api_analyzer", "APIAnalyzer")

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
