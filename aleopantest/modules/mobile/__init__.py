"""Mobile tools module initialization"""
from aleopantest.core.tool_helper import robust_import

APKAnalyzer = robust_import("aleopantest.modules.mobile.apk_analyzer", "APKAnalyzer")
IOSAppAnalyzer = robust_import("aleopantest.modules.mobile.ios_analyzer", "IOSAppAnalyzer")

__all__ = ['APKAnalyzer', 'IOSAppAnalyzer']
