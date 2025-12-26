from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import ipaddress

class SubnetCalc(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Subnet Calculator",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Menghitung detail subnet IP (mask, network, broadcast, host range)",
            usage="Aleocrophic run subnet-calc --cidr <ip/prefix>",
            example="Aleocrophic run subnet-calc --cidr 192.168.1.0/24",
            parameters={"cidr": "IP Address dengan prefix CIDR"},
            requirements=[],
            tags=["network", "ip", "subnet"]
        )
        super().__init__(metadata)

    def run(self, cidr: str = "", **kwargs):
        if not cidr: return {"error": "CIDR is required"}
        try:
            net = ipaddress.ip_network(cidr, strict=False)
            return {
                "network": str(net.network_address),
                "netmask": str(net.netmask),
                "broadcast": str(net.broadcast_address),
                "num_addresses": net.num_addresses,
                "first_host": str(next(net.hosts())),
                "last_host": str(list(net.hosts())[-1])
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, cidr: str = "", **kwargs) -> bool: return bool(cidr)
