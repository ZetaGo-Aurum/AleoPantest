from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import time

class NetSpeed(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Network Speed Test (Simulated)",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AleoPantest",
            description="Menguji kecepatan unduh dan unggah jaringan",
            usage="aleopantest run net-speed",
            example="aleopantest run net-speed",
            parameters={},
            requirements=[],
            tags=["network", "utility", "speed"]
        )
        super().__init__(metadata)

    def run(self, **kwargs):
        return {"download": "45.2 Mbps", "upload": "12.8 Mbps", "latency": "25ms", "status": "success"}

    def validate_input(self, **kwargs) -> bool: return True
