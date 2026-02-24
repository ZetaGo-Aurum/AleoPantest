"""Password module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

SprayAttack = robust_import("aleopantest.modules.password_auth.spray_attack", "SprayAttack")
CredentialTest = robust_import("aleopantest.modules.password_auth.credential_test", "CredentialTest")
PassPolicyAudit = robust_import("aleopantest.modules.password_auth.pass_policy_audit", "PassPolicyAudit")
MFABypassCheck = robust_import("aleopantest.modules.password_auth.mfa_bypass_check", "MFABypassCheck")
SessionHijackDetect = robust_import("aleopantest.modules.password_auth.session_hijack_detect", "SessionHijackDetect")
CookieAnalyzer = robust_import("aleopantest.modules.password_auth.cookie_analyzer", "CookieAnalyzer")
OAuthAbuse = robust_import("aleopantest.modules.password_auth.oauth_abuse", "OAuthAbuse")
SAMLAttack = robust_import("aleopantest.modules.password_auth.saml_attack", "SAMLAttack")
TicketForge = robust_import("aleopantest.modules.password_auth.ticket_forge", "TicketForge")
RainbowGen = robust_import("aleopantest.modules.password_auth.rainbow_gen", "RainbowGen")
WordlistGen = robust_import("aleopantest.modules.password_auth.wordlist_gen", "WordlistGen")
HashIdentify = robust_import("aleopantest.modules.password_auth.hash_identify", "HashIdentify")
PassStrength = robust_import("aleopantest.modules.password_auth.pass_strength", "PassStrength")
BruteHTTP = robust_import("aleopantest.modules.password_auth.brute_http", "BruteHTTP")
BruteSSH = robust_import("aleopantest.modules.password_auth.brute_ssh", "BruteSSH")
BruteFTP = robust_import("aleopantest.modules.password_auth.brute_ftp", "BruteFTP")
BruteRDP = robust_import("aleopantest.modules.password_auth.brute_rdp", "BruteRDP")
BruteMySQL = robust_import("aleopantest.modules.password_auth.brute_mysql", "BruteMySQL")
BruteSMTP = robust_import("aleopantest.modules.password_auth.brute_smtp", "BruteSMTP")
BruteLDAP = robust_import("aleopantest.modules.password_auth.brute_ldap", "BruteLDAP")
BruteCustom = robust_import("aleopantest.modules.password_auth.brute_custom", "BruteCustom")
DefaultCreds = robust_import("aleopantest.modules.password_auth.default_creds", "DefaultCreds")
PassReuse = robust_import("aleopantest.modules.password_auth.pass_reuse", "PassReuse")
AuthTokenTest = robust_import("aleopantest.modules.password_auth.auth_token_test", "AuthTokenTest")
SSOAudit = robust_import("aleopantest.modules.password_auth.sso_audit", "SSOAudit")
TOTPTest = robust_import("aleopantest.modules.password_auth.totp_test", "TOTPTest")
APIKeyTest = robust_import("aleopantest.modules.password_auth.api_key_test", "APIKeyTest")
CertAuthTest = robust_import("aleopantest.modules.password_auth.cert_auth_test", "CertAuthTest")
BiometricBypass = robust_import("aleopantest.modules.password_auth.biometric_bypass", "BiometricBypass")
CaptchaTest = robust_import("aleopantest.modules.password_auth.captcha_test", "CaptchaTest")

__all__ = [
    'SprayAttack',
    'CredentialTest',
    'PassPolicyAudit',
    'MFABypassCheck',
    'SessionHijackDetect',
    'CookieAnalyzer',
    'OAuthAbuse',
    'SAMLAttack',
    'TicketForge',
    'RainbowGen',
    'WordlistGen',
    'HashIdentify',
    'PassStrength',
    'BruteHTTP',
    'BruteSSH',
    'BruteFTP',
    'BruteRDP',
    'BruteMySQL',
    'BruteSMTP',
    'BruteLDAP',
    'BruteCustom',
    'DefaultCreds',
    'PassReuse',
    'AuthTokenTest',
    'SSOAudit',
    'TOTPTest',
    'APIKeyTest',
    'CertAuthTest',
    'BiometricBypass',
    'CaptchaTest',
]
