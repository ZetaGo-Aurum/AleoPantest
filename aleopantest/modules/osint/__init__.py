"""OSINT module initialization with robust error handling"""
from aleopantest.core.tool_helper import robust_import

EmailFinder = robust_import("aleopantest.modules.osint.email_finder", "EmailFinder")
DomainInfo = robust_import("aleopantest.modules.osint.domain_info", "DomainInfo")
IPGeolocation = robust_import("aleopantest.modules.osint.ip_geolocation", "IPGeolocation")
MetadataExtractor = robust_import("aleopantest.modules.osint.metadata_extractor", "MetadataExtractor")
SearchEngineDorking = robust_import("aleopantest.modules.osint.search_engine_dorking", "SearchEngineDorking")
UserSearch = robust_import("aleopantest.modules.osint.user_search", "UserSearch")
GitRecon = robust_import("aleopantest.modules.osint.git_recon", "GitRecon")
WhoisHistory = robust_import("aleopantest.modules.osint.whois_history", "WhoisHistory")
ShodanSearch = robust_import("aleopantest.modules.osint.shodan_search", "ShodanSearch")
PhoneLookup = robust_import("aleopantest.modules.osint.phone_lookup", "PhoneLookup")
MetadataExif = robust_import("aleopantest.modules.osint.metadata_exif", "MetadataExif")
SocialAnalyzer = robust_import("aleopantest.modules.osint.social_analyzer", "SocialAnalyzer")
BreachChecker = robust_import("aleopantest.modules.osint.breach_check", "BreachChecker")

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
