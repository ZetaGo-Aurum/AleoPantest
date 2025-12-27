from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import socket

class PortKnocker(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Port Knocker",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Melakukan port knocking pada urutan port tertentu",
            usage="aleopantest run port-knocker --host <ip> --ports <port1,port2,port3>",
            example="aleopantest run port-knocker --host 192.168.1.1 --ports 1000,2000,3000",
            parameters={"host": "Target IP", "ports": "Urutan port (dipisahkan koma)"},
            requirements=[],
            tags=["network", "stealth", "knocking"]
        )
        super().__init__(metadata)

    def run(self, host: str = "", ports: str = "", **kwargs):
        if not host or not ports: return {"error": "Host and ports are required"}
        port_list = [int(p.strip()) for p in ports.split(",")]
        results = []
        for port in port_list:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect_ex((host, port))
                s.close()
                results.append(f"Knocked on {port}")
            except:
                results.append(f"Failed to knock on {port}")
        return {"host": host, "sequence": port_list, "results": results}

    def validate_input(self, host: str = "", **kwargs) -> bool: return bool(host)
