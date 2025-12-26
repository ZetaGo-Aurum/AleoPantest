from aleo_pantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import base64
import json

class JWTDecoder(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="JWT Decoder",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Men-decode header dan payload dari JWT token tanpa verifikasi signature",
            usage="Aleocrophic run jwt-decoder --token <jwt>",
            example="Aleocrophic run jwt-decoder --token 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'",
            parameters={"token": "JWT token string"},
            requirements=[],
            tags=["utility", "jwt", "crypto"]
        )
        super().__init__(metadata)

    def run(self, token: str = "", **kwargs):
        if not token: return {"error": "Token is required"}
        try:
            parts = token.split('.')
            if len(parts) < 2: return {"error": "Invalid JWT format"}
            header = json.loads(base64.b64decode(parts[0] + '==').decode())
            payload = json.loads(base64.b64decode(parts[1] + '==').decode())
            return {"header": header, "payload": payload}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, token: str = "", **kwargs) -> bool: return bool(token)
