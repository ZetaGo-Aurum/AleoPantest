from typing import Dict, Any, List
from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class IDSEvasionHelper(BaseTool):
    def __init__(self):
        super().__init__()
        self.metadata = ToolMetadata(
            name="IDS Evasion Helper",
            description="Generate payload variations to bypass Intrusion Detection Systems (IDS/IPS)",
            version="1.0.0",
            author="AleoPantest",
            category=ToolCategory.SECURITY,
            usage="aleopantest run ids-evasion --payload <string> --method <hex/base64/charcode>",
            requirements=[],
            tags=["ids", "evasion", "obfuscation", "payload"],
            parameters={
                "payload": "The payload string to encode/obfuscate",
                "method": "Evasion method (hex, base64, charcode, unicode)"
            },
            example="aleopantest run ids-evasion --payload '<script>alert(1)</script>' --method hex",
            risk_level="MEDIUM"
        )

    def run(self, **kwargs) -> Dict[str, Any]:
        payload = kwargs.get('payload')
        method = kwargs.get('method', 'hex')

        if not payload:
            self.errors.append("Payload is required")
            return {}

        self.log(f"Generating evasion variations for payload using '{method}' method...")
        
        result = {"original": payload, "variations": []}
        
        if method == 'hex':
            hex_payload = "".join([f"\\x{ord(c):02x}" for c in payload])
            result["variations"].append({"name": "Hex Encoding", "encoded": hex_payload})
        elif method == 'base64':
            import base64
            b64_payload = base64.b64encode(payload.encode()).decode()
            result["variations"].append({"name": "Base64 Encoding", "encoded": b64_payload})
        elif method == 'charcode':
            char_payload = ",".join([str(ord(c)) for c in payload])
            result["variations"].append({"name": "JavaScript CharCode", "encoded": f"String.fromCharCode({char_payload})"})
        
        return {
            "status": "completed",
            "method": method,
            "results": result
        }
