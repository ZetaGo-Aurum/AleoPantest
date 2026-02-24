"""Mobile tools module initialization"""
from aleopantest.core.tool_helper import robust_import

APKAnalyzer = robust_import("aleopantest.modules.mobile.apk_analyzer", "APKAnalyzer")
IOSAppAnalyzer = robust_import("aleopantest.modules.mobile.ios_analyzer", "IOSAppAnalyzer")

AndroidDebug = robust_import("aleopantest.modules.mobile.android_debug", "AndroidDebug")
IOSJailbreak = robust_import("aleopantest.modules.mobile.ios_jailbreak", "IOSJailbreak")
MobileSSLPin = robust_import("aleopantest.modules.mobile.mobile_ssl_pin", "MobileSSLPin")
AppPermission = robust_import("aleopantest.modules.mobile.app_permission", "AppPermission")
SmaliDecompile = robust_import("aleopantest.modules.mobile.smali_decompile", "SmaliDecompile")
FridaScripts = robust_import("aleopantest.modules.mobile.frida_scripts", "FridaScripts")
ObjectionWrap = robust_import("aleopantest.modules.mobile.objection_wrap", "ObjectionWrap")
MobileAPITest = robust_import("aleopantest.modules.mobile.mobile_api_test", "MobileAPITest")
CertPinBypass = robust_import("aleopantest.modules.mobile.cert_pin_bypass", "CertPinBypass")
IntentFuzz = robust_import("aleopantest.modules.mobile.intent_fuzz", "IntentFuzz")
MobileStorage = robust_import("aleopantest.modules.mobile.mobile_storage", "MobileStorage")
MobileCrypto = robust_import("aleopantest.modules.mobile.mobile_crypto", "MobileCrypto")
MobileNetwork = robust_import("aleopantest.modules.mobile.mobile_network", "MobileNetwork")
MobileAuth = robust_import("aleopantest.modules.mobile.mobile_auth", "MobileAuth")
AppCloneDetect = robust_import("aleopantest.modules.mobile.app_clone_detect", "AppCloneDetect")
MobileMalware = robust_import("aleopantest.modules.mobile.mobile_malware", "MobileMalware")
MobilePrivacy = robust_import("aleopantest.modules.mobile.mobile_privacy", "MobilePrivacy")
MobileConfig = robust_import("aleopantest.modules.mobile.mobile_config", "MobileConfig")

__all__ = ['APKAnalyzer', 'IOSAppAnalyzer'
    'AndroidDebug',
    'IOSJailbreak',
    'MobileSSLPin',
    'AppPermission',
    'SmaliDecompile',
    'FridaScripts',
    'ObjectionWrap',
    'MobileAPITest',
    'CertPinBypass',
    'IntentFuzz',
    'MobileStorage',
    'MobileCrypto',
    'MobileNetwork',
    'MobileAuth',
    'AppCloneDetect',
    'MobileMalware',
    'MobilePrivacy',
    'MobileConfig',
]
