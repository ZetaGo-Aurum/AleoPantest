from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import dns.resolver
import dns.query
import dns.zone

class DNSZoneTransfer(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="DNS Zone Transfer",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Mencoba melakukan DNS zone transfer (AXFR)",
            usage="Aleocrophic run dns-zone --domain <domain>",
            example="Aleocrophic run dns-zone --domain example.com",
            parameters={"domain": "Target domain"},
            requirements=["dnspython"],
            tags=["network", "dns", "recon"]
        )
        super().__init__(metadata)

    def run(self, domain: str = "", **kwargs):
        if not domain: return {"error": "Domain is required"}
        try:
            ns_answers = dns.resolver.resolve(domain, 'NS')
            ns_servers = [str(ns.target) for ns in ns_answers]
            results = {}
            for ns in ns_servers:
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns, domain))
                    if zone:
                        results[ns] = [str(name) + " " + str(rd) for name, node in zone.nodes.items() for rd in node.rdatasets]
                except:
                    results[ns] = "Zone transfer failed"
            return {"domain": domain, "results": results}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, domain: str = "", **kwargs) -> bool: return bool(domain)
