from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import base64

class Base64Tool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Base64 Encoder/Decoder",
            category=ToolCategory.UTILITIES,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Encode atau decode string menggunakan format Base64",
            usage="aleopantest run base64 --action <encode|decode> --data <string>",
            example="aleopantest run base64 --action encode --data 'hello world'",
            parameters={
                "action": "Tindakan yang dilakukan (encode atau decode)",
                "data": "String yang akan diproses"
            },
            requirements=[],
            tags=["utility", "encoding", "base64"]
        )
        super().__init__(metadata)

    def run(self, action: str = "encode", data: str = "", **kwargs):
        if not data: return {"error": "Data is required"}
        
        try:
            if action.lower() == "encode":
                encoded = base64.b64encode(data.encode()).decode()
                return {"action": "encode", "original": data, "result": encoded}
            elif action.lower() == "decode":
                decoded = base64.b64decode(data.encode()).decode()
                return {"action": "decode", "original": data, "result": decoded}
            else:
                return {"error": "Invalid action. Use 'encode' or 'decode'."}
        except Exception as e:
            return {"error": str(e)}

    def validate_input(self, data: str = "", **kwargs) -> bool:
        return bool(data)
