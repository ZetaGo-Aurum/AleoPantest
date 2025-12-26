"""Network tools module initialization with robust error handling"""
from aleo_pantest.core.tool_helper import robust_import

PortScanner = robust_import("aleo_pantest.modules.network.port_scanner", "PortScanner")
PacketSniffer = robust_import("aleo_pantest.modules.network.sniffer", "PacketSniffer")
PingTool = robust_import("aleo_pantest.modules.network.ping_tool", "PingTool")
DNSLookup = robust_import("aleo_pantest.modules.network.dns_lookup", "DNSLookup")
TraceRoute = robust_import("aleo_pantest.modules.network.trace_route", "TraceRoute")
WhoisLookup = robust_import("aleo_pantest.modules.network.whois_lookup", "WhoisLookup")
SSLChecker = robust_import("aleo_pantest.modules.network.ssl_checker", "SSLChecker")
IPScanner = robust_import("aleo_pantest.modules.network.ip_scanner", "IPScanner")
DDoSSimulator = robust_import("aleo_pantest.modules.network.ddos_simulator", "DDoSSimulator")
MACLookup = robust_import("aleo_pantest.modules.network.mac_lookup", "MACLookup")
NetSpeed = robust_import("aleo_pantest.modules.network.net_speed", "NetSpeed")
SubnetCalc = robust_import("aleo_pantest.modules.network.subnet_calc", "SubnetCalc")
ArpScanner = robust_import("aleo_pantest.modules.network.arp_scan", "ArpScanner")
VLANScanner = robust_import("aleo_pantest.modules.network.vlan_scanner", "VLANScanner")

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
