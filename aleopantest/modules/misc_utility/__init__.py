"""Misc module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

PayloadEncode = robust_import("aleopantest.modules.misc_utility.payload_encode", "PayloadEncode")
C2Detect = robust_import("aleopantest.modules.misc_utility.c2_detect", "C2Detect")
HoneypotDetect = robust_import("aleopantest.modules.misc_utility.honeypot_detect", "HoneypotDetect")
SandboxDetect = robust_import("aleopantest.modules.misc_utility.sandbox_detect", "SandboxDetect")
ProxyChain = robust_import("aleopantest.modules.misc_utility.proxy_chain", "ProxyChain")
TorCheck = robust_import("aleopantest.modules.misc_utility.tor_check", "TorCheck")
VPNLeakTest = robust_import("aleopantest.modules.misc_utility.vpn_leak_test", "VPNLeakTest")
DNSLeakTest = robust_import("aleopantest.modules.misc_utility.dns_leak_test", "DNSLeakTest")
IPRotate = robust_import("aleopantest.modules.misc_utility.ip_rotate", "IPRotate")
UserAgentGen = robust_import("aleopantest.modules.misc_utility.user_agent_gen", "UserAgentGen")
ReverseShell = robust_import("aleopantest.modules.misc_utility.reverse_shell", "ReverseShell")
BindShell = robust_import("aleopantest.modules.misc_utility.bind_shell", "BindShell")
FileServer = robust_import("aleopantest.modules.misc_utility.file_server", "FileServer")
PortForward = robust_import("aleopantest.modules.misc_utility.port_forward", "PortForward")
NetworkPivot = robust_import("aleopantest.modules.misc_utility.network_pivot", "NetworkPivot")
DataExfilDetect = robust_import("aleopantest.modules.misc_utility.data_exfil_detect", "DataExfilDetect")
LogCleanerDetect = robust_import("aleopantest.modules.misc_utility.log_cleaner_detect", "LogCleanerDetect")
RootkitDetect = robust_import("aleopantest.modules.misc_utility.rootkit_detect", "RootkitDetect")
BackdoorDetect = robust_import("aleopantest.modules.misc_utility.backdoor_detect", "BackdoorDetect")
WebshellDetect = robust_import("aleopantest.modules.misc_utility.webshell_detect", "WebshellDetect")
ConfigAudit = robust_import("aleopantest.modules.misc_utility.config_audit", "ConfigAudit")
ServiceEnum = robust_import("aleopantest.modules.misc_utility.service_enum", "ServiceEnum")
CronAudit = robust_import("aleopantest.modules.misc_utility.cron_audit", "CronAudit")
SUIDCheck = robust_import("aleopantest.modules.misc_utility.suid_check", "SUIDCheck")
KernelExploit = robust_import("aleopantest.modules.misc_utility.kernel_exploit", "KernelExploit")

__all__ = [
    'PayloadEncode',
    'C2Detect',
    'HoneypotDetect',
    'SandboxDetect',
    'ProxyChain',
    'TorCheck',
    'VPNLeakTest',
    'DNSLeakTest',
    'IPRotate',
    'UserAgentGen',
    'ReverseShell',
    'BindShell',
    'FileServer',
    'PortForward',
    'NetworkPivot',
    'DataExfilDetect',
    'LogCleanerDetect',
    'RootkitDetect',
    'BackdoorDetect',
    'WebshellDetect',
    'ConfigAudit',
    'ServiceEnum',
    'CronAudit',
    'SUIDCheck',
    'KernelExploit',
]
