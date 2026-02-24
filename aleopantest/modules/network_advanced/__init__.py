"""Network Advanced module - Aleopantest V4.0.0"""
from aleopantest.core.tool_helper import robust_import

BGPHijack = robust_import("aleopantest.modules.network_advanced.bgp_hijack", "BGPHijack")
DNSTunnel = robust_import("aleopantest.modules.network_advanced.dns_tunnel", "DNSTunnel")
ICMPTunnel = robust_import("aleopantest.modules.network_advanced.icmp_tunnel", "ICMPTunnel")
TCPHijack = robust_import("aleopantest.modules.network_advanced.tcp_hijack", "TCPHijack")
MITMDetect = robust_import("aleopantest.modules.network_advanced.mitm_detect", "MITMDetect")
RogueDHCP = robust_import("aleopantest.modules.network_advanced.rogue_dhcp", "RogueDHCP")
IPv6Recon = robust_import("aleopantest.modules.network_advanced.ipv6_recon", "IPv6Recon")
NetBIOSEnum = robust_import("aleopantest.modules.network_advanced.netbios_enum", "NetBIOSEnum")
SMBEnum = robust_import("aleopantest.modules.network_advanced.smb_enum", "SMBEnum")
RPCEnum = robust_import("aleopantest.modules.network_advanced.rpc_enum", "RPCEnum")
NTPAmp = robust_import("aleopantest.modules.network_advanced.ntp_amp", "NTPAmp")
SSDPScan = robust_import("aleopantest.modules.network_advanced.ssdp_scan", "SSDPScan")
LDAPEnum = robust_import("aleopantest.modules.network_advanced.ldap_enum", "LDAPEnum")
FTPAudit = robust_import("aleopantest.modules.network_advanced.ftp_audit", "FTPAudit")
SMTPEnum = robust_import("aleopantest.modules.network_advanced.smtp_enum", "SMTPEnum")
POP3Audit = robust_import("aleopantest.modules.network_advanced.pop3_audit", "POP3Audit")
IMAPAudit = robust_import("aleopantest.modules.network_advanced.imap_audit", "IMAPAudit")
RedisAudit = robust_import("aleopantest.modules.network_advanced.redis_audit", "RedisAudit")
MemcacheAudit = robust_import("aleopantest.modules.network_advanced.memcache_audit", "MemcacheAudit")
ElasticAudit = robust_import("aleopantest.modules.network_advanced.elastic_audit", "ElasticAudit")
KafkaAudit = robust_import("aleopantest.modules.network_advanced.kafka_audit", "KafkaAudit")
RabbitAudit = robust_import("aleopantest.modules.network_advanced.rabbit_audit", "RabbitAudit")
VNCAudit = robust_import("aleopantest.modules.network_advanced.vnc_audit", "VNCAudit")
RDPAudit = robust_import("aleopantest.modules.network_advanced.rdp_audit", "RDPAudit")
TelnetAudit = robust_import("aleopantest.modules.network_advanced.telnet_audit", "TelnetAudit")

__all__ = [
    'BGPHijack',
    'DNSTunnel',
    'ICMPTunnel',
    'TCPHijack',
    'MITMDetect',
    'RogueDHCP',
    'IPv6Recon',
    'NetBIOSEnum',
    'SMBEnum',
    'RPCEnum',
    'NTPAmp',
    'SSDPScan',
    'LDAPEnum',
    'FTPAudit',
    'SMTPEnum',
    'POP3Audit',
    'IMAPAudit',
    'RedisAudit',
    'MemcacheAudit',
    'ElasticAudit',
    'KafkaAudit',
    'RabbitAudit',
    'VNCAudit',
    'RDPAudit',
    'TelnetAudit',
]
