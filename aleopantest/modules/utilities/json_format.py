from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
import json

class JSONFormatter(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="JSON Formatter",
            category=ToolCategory.UTILITIES,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Memformat string JSON yang berantakan menjadi rapi (pretty-print)",
            usage="aleopantest run json-format --data <json_string>",
            example="aleopantest run json-format --data '{\"a\":1,\"b\":2}'",
            parameters={"data": "String JSON yang akan diformat"},
            requirements=[],
            tags=["utility", "json", "formatter"]
        )
        super().__init__(metadata)

    def run(self, data: str = "", **kwargs):
        if not data: return {"error": "Data is required"}
        try:
            parsed = json.loads(data)
            formatted = json.dumps(parsed, indent=4)
            return {"formatted": formatted}
        except Exception as e:
            return {"error": f"Invalid JSON: {str(e)}"}

    def validate_input(self, data: str = "", **kwargs) -> bool: return bool(data)
