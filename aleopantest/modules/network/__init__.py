"""Network tools module initialization with robust error handling"""
from aleopantest.core.tool_helper import robust_import

PortScanner = robust_import("aleopantest.modules.network.port_scanner", "PortScanner")
PacketSniffer = robust_import("aleopantest.modules.network.sniffer", "PacketSniffer")
PingTool = robust_import("aleopantest.modules.network.ping_tool", "PingTool")
DNSLookup = robust_import("aleopantest.modules.network.dns_lookup", "DNSLookup")
TraceRoute = robust_import("aleopantest.modules.network.trace_route", "TraceRoute")
WhoisLookup = robust_import("aleopantest.modules.network.whois_lookup", "WhoisLookup")
SSLChecker = robust_import("aleopantest.modules.network.ssl_checker", "SSLChecker")
IPScanner = robust_import("aleopantest.modules.network.ip_scanner", "IPScanner")
DDoSSimulator = robust_import("aleopantest.modules.network.ddos_simulator", "DDoSSimulator")
MACLookup = robust_import("aleopantest.modules.network.mac_lookup", "MACLookup")
NetSpeed = robust_import("aleopantest.modules.network.net_speed", "NetSpeed")
SubnetCalc = robust_import("aleopantest.modules.network.subnet_calc", "SubnetCalc")
ArpScanner = robust_import("aleopantest.modules.network.arp_scan", "ArpScanner")
VLANScanner = robust_import("aleopantest.modules.network.vlan_scanner", "VLANScanner")

__all__ = [
    'PortScanner',
    'PacketSniffer',
    'PingTool',
    'DNSLookup',
    'TraceRoute',
    'WhoisLookup',
    'SSLChecker',
    'IPScanner',
    'DDoSSimulator',
    'MACLookup',
    'NetSpeed',
    'SubnetCalc',
    'ArpScanner',
    'VLANScanner'
]
