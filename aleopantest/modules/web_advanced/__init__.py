"""Web Advanced module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

XXEDetect = robust_import("aleopantest.modules.web_advanced.xxe_detect", "XXEDetect")
SSRFDetect = robust_import("aleopantest.modules.web_advanced.ssrf_detect", "SSRFDetect")
SSTIDetect = robust_import("aleopantest.modules.web_advanced.ssti_detect", "SSTIDetect")
PrototypePollute = robust_import("aleopantest.modules.web_advanced.prototype_pollute", "PrototypePollute")
DeserializeCheck = robust_import("aleopantest.modules.web_advanced.deserialize_check", "DeserializeCheck")
HTTPSmuggle = robust_import("aleopantest.modules.web_advanced.http_smuggle", "HTTPSmuggle")
CachePoison = robust_import("aleopantest.modules.web_advanced.cache_poison", "CachePoison")
CORSMiscfg = robust_import("aleopantest.modules.web_advanced.cors_miscfg", "CORSMiscfg")
OpenRedirect = robust_import("aleopantest.modules.web_advanced.open_redirect", "OpenRedirect")
HostHeaderInject = robust_import("aleopantest.modules.web_advanced.host_header_inject", "HostHeaderInject")
CRLFInject = robust_import("aleopantest.modules.web_advanced.crlf_inject", "CRLFInject")
LFIDetect = robust_import("aleopantest.modules.web_advanced.lfi_detect", "LFIDetect")
RFIDetect = robust_import("aleopantest.modules.web_advanced.rfi_detect", "RFIDetect")
CommandInject = robust_import("aleopantest.modules.web_advanced.command_inject", "CommandInject")
IDORDetect = robust_import("aleopantest.modules.web_advanced.idor_detect", "IDORDetect")
PathTraversal = robust_import("aleopantest.modules.web_advanced.path_traversal", "PathTraversal")
UploadVuln = robust_import("aleopantest.modules.web_advanced.upload_vuln", "UploadVuln")
SessionFixation = robust_import("aleopantest.modules.web_advanced.session_fixation", "SessionFixation")
BusinessLogic = robust_import("aleopantest.modules.web_advanced.business_logic", "BusinessLogic")
RaceCondition = robust_import("aleopantest.modules.web_advanced.race_condition", "RaceCondition")
SubdomainTakeover = robust_import("aleopantest.modules.web_advanced.subdomain_takeover", "SubdomainTakeover")
WebSocketTest = robust_import("aleopantest.modules.web_advanced.websocket_test", "WebSocketTest")
CSRFAdvanced = robust_import("aleopantest.modules.web_advanced.csrf_advanced", "CSRFAdvanced")
ContentSecurity = robust_import("aleopantest.modules.web_advanced.content_security", "ContentSecurity")
CookieSecurity = robust_import("aleopantest.modules.web_advanced.cookie_security", "CookieSecurity")
JSAnalyzer = robust_import("aleopantest.modules.web_advanced.js_analyzer", "JSAnalyzer")
WAFBypass = robust_import("aleopantest.modules.web_advanced.waf_bypass", "WAFBypass")
WebFingerprint = robust_import("aleopantest.modules.web_advanced.web_fingerprint", "WebFingerprint")
BrokenAccess = robust_import("aleopantest.modules.web_advanced.broken_access", "BrokenAccess")
SecurityHeaders = robust_import("aleopantest.modules.web_advanced.security_headers", "SecurityHeaders")
HTMLInject = robust_import("aleopantest.modules.web_advanced.html_inject", "HTMLInject")
WebParamMine = robust_import("aleopantest.modules.web_advanced.web_param_mine", "WebParamMine")
HTTP2Test = robust_import("aleopantest.modules.web_advanced.http2_test", "HTTP2Test")
GraphQLVuln = robust_import("aleopantest.modules.web_advanced.graphql_vuln", "GraphQLVuln")
WebSocketHijack = robust_import("aleopantest.modules.web_advanced.web_socket_hijack", "WebSocketHijack")
DOMXSS = robust_import("aleopantest.modules.web_advanced.dom_xss", "DOMXSS")
WebCacheDeception = robust_import("aleopantest.modules.web_advanced.web_cache_deception", "WebCacheDeception")
ClickHijack = robust_import("aleopantest.modules.web_advanced.click_hijack", "ClickHijack")
JWTVuln = robust_import("aleopantest.modules.web_advanced.jwt_vuln", "JWTVuln")

__all__ = [
    'XXEDetect',
    'SSRFDetect',
    'SSTIDetect',
    'PrototypePollute',
    'DeserializeCheck',
    'HTTPSmuggle',
    'CachePoison',
    'CORSMiscfg',
    'OpenRedirect',
    'HostHeaderInject',
    'CRLFInject',
    'LFIDetect',
    'RFIDetect',
    'CommandInject',
    'IDORDetect',
    'PathTraversal',
    'UploadVuln',
    'SessionFixation',
    'BusinessLogic',
    'RaceCondition',
    'SubdomainTakeover',
    'WebSocketTest',
    'CSRFAdvanced',
    'ContentSecurity',
    'CookieSecurity',
    'JSAnalyzer',
    'WAFBypass',
    'WebFingerprint',
    'BrokenAccess',
    'SecurityHeaders',
    'HTMLInject',
    'WebParamMine',
    'HTTP2Test',
    'GraphQLVuln',
    'WebSocketHijack',
    'DOMXSS',
    'WebCacheDeception',
    'ClickHijack',
    'JWTVuln',
]
