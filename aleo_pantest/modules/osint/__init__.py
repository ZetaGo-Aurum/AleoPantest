"""OSINT module initialization with robust error handling"""
from aleo_pantest.core.tool_helper import robust_import

EmailFinder = robust_import("aleo_pantest.modules.osint.email_finder", "EmailFinder")
DomainInfo = robust_import("aleo_pantest.modules.osint.domain_info", "DomainInfo")
IPGeolocation = robust_import("aleo_pantest.modules.osint.ip_geolocation", "IPGeolocation")
MetadataExtractor = robust_import("aleo_pantest.modules.osint.metadata_extractor", "MetadataExtractor")
SearchEngineDorking = robust_import("aleo_pantest.modules.osint.search_engine_dorking", "SearchEngineDorking")
UserSearch = robust_import("aleo_pantest.modules.osint.user_search", "UserSearch")
GitRecon = robust_import("aleo_pantest.modules.osint.git_recon", "GitRecon")
WhoisHistory = robust_import("aleo_pantest.modules.osint.whois_history", "WhoisHistory")
ShodanSearch = robust_import("aleo_pantest.modules.osint.shodan_search", "ShodanSearch")
PhoneLookup = robust_import("aleo_pantest.modules.osint.phone_lookup", "PhoneLookup")
MetadataExif = robust_import("aleo_pantest.modules.osint.metadata_exif", "MetadataExif")
SocialAnalyzer = robust_import("aleo_pantest.modules.osint.social_analyzer", "SocialAnalyzer")
BreachChecker = robust_import("aleo_pantest.modules.osint.breach_check", "BreachChecker")

__all__ = [
    'EmailFinder',
    'DomainInfo',
    'IPGeolocation',
    'MetadataExtractor',
    'SearchEngineDorking',
    'UserSearch',
    'GitRecon',
    'WhoisHistory',
    'ShodanSearch',
    'PhoneLookup',
    'MetadataExif',
    'SocialAnalyzer',
    'BreachChecker'
]
