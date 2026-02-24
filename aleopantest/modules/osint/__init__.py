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
DarkWebSearch = robust_import("aleopantest.modules.osint.dark_web_search", "DarkWebSearch")

TelegramOSINT = robust_import("aleopantest.modules.osint.telegram_osint", "TelegramOSINT")
DiscordRecon = robust_import("aleopantest.modules.osint.discord_recon", "DiscordRecon")
LinkedInEnum = robust_import("aleopantest.modules.osint.linkedin_enum", "LinkedInEnum")
PastebinMonitor = robust_import("aleopantest.modules.osint.pastebin_monitor", "PastebinMonitor")
WaybackRecon = robust_import("aleopantest.modules.osint.wayback_recon", "WaybackRecon")
CertSearch = robust_import("aleopantest.modules.osint.cert_search", "CertSearch")
DNSHistory = robust_import("aleopantest.modules.osint.dns_history", "DNSHistory")
FaviconHash = robust_import("aleopantest.modules.osint.favicon_hash", "FaviconHash")
S3Finder = robust_import("aleopantest.modules.osint.s3_finder", "S3Finder")
GoogleDorkingAdv = robust_import("aleopantest.modules.osint.google_dorking_adv", "GoogleDorkingAdv")
GitHubRecon = robust_import("aleopantest.modules.osint.github_recon", "GitHubRecon")
TwitterOSINT = robust_import("aleopantest.modules.osint.twitter_osint", "TwitterOSINT")
InstagramOSINT = robust_import("aleopantest.modules.osint.instagram_osint", "InstagramOSINT")
FaceSearch = robust_import("aleopantest.modules.osint.face_search", "FaceSearch")
EmailOSINT = robust_import("aleopantest.modules.osint.email_osint", "EmailOSINT")
CompanyRecon = robust_import("aleopantest.modules.osint.company_recon", "CompanyRecon")
GeoOSINT = robust_import("aleopantest.modules.osint.geo_osint", "GeoOSINT")
VehicleOSINT = robust_import("aleopantest.modules.osint.vehicle_osint", "VehicleOSINT")
CryptoTrace = robust_import("aleopantest.modules.osint.crypto_trace", "CryptoTrace")
DomainMonitor = robust_import("aleopantest.modules.osint.domain_monitor", "DomainMonitor")
LeakSearch = robust_import("aleopantest.modules.osint.leak_search", "LeakSearch")
WebArchive = robust_import("aleopantest.modules.osint.web_archive", "WebArchive")
ImageForensics = robust_import("aleopantest.modules.osint.image_forensics", "ImageForensics")
SocialMediaMap = robust_import("aleopantest.modules.osint.social_media_map", "SocialMediaMap")
WebsiteMonitor = robust_import("aleopantest.modules.osint.website_monitor", "WebsiteMonitor")
TechProfiler = robust_import("aleopantest.modules.osint.tech_profiler", "TechProfiler")
NetworkOSINT = robust_import("aleopantest.modules.osint.network_osint", "NetworkOSINT")
DocumentOSINT = robust_import("aleopantest.modules.osint.document_osint", "DocumentOSINT")
PhoneOSINT = robust_import("aleopantest.modules.osint.phone_osint", "PhoneOSINT")
UsernameSearch = robust_import("aleopantest.modules.osint.username_search", "UsernameSearch")
IPReputation = robust_import("aleopantest.modules.osint.ip_reputation", "IPReputation")
ThreatIntel = robust_import("aleopantest.modules.osint.threat_intel", "ThreatIntel")
MalwareHash = robust_import("aleopantest.modules.osint.malware_hash", "MalwareHash")
SubdomainEnum = robust_import("aleopantest.modules.osint.subdomain_enum", "SubdomainEnum")
ASNLookup = robust_import("aleopantest.modules.osint.asn_lookup", "ASNLookup")

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
    'BreachChecker',
    'DarkWebSearch'

    'TelegramOSINT',
    'DiscordRecon',
    'LinkedInEnum',
    'PastebinMonitor',
    'WaybackRecon',
    'CertSearch',
    'DNSHistory',
    'FaviconHash',
    'S3Finder',
    'GoogleDorkingAdv',
    'GitHubRecon',
    'TwitterOSINT',
    'InstagramOSINT',
    'FaceSearch',
    'EmailOSINT',
    'CompanyRecon',
    'GeoOSINT',
    'VehicleOSINT',
    'CryptoTrace',
    'DomainMonitor',
    'LeakSearch',
    'WebArchive',
    'ImageForensics',
    'SocialMediaMap',
    'WebsiteMonitor',
    'TechProfiler',
    'NetworkOSINT',
    'DocumentOSINT',
    'PhoneOSINT',
    'UsernameSearch',
    'IPReputation',
    'ThreatIntel',
    'MalwareHash',
    'SubdomainEnum',
    'ASNLookup',
]
