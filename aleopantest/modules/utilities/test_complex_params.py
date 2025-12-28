import json
from datetime import datetime
from typing import Dict, Any, List
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class ComplexParamTester(BaseTool):
    """
    Module for testing complex parameter types (JSON, Boolean, Number, Date, List)
    """
    
    def __init__(self):
        # Define form schema with various types
        form_schema = [
            {
                "name": "target",
                "type": "text",
                "label": "Test Target",
                "placeholder": "Enter any test target",
                "required": True
            },
            {
                "name": "test_number",
                "type": "number",
                "label": "Number Test",
                "default": 42,
                "description": "An integer value"
            },
            {
                "name": "test_float",
                "type": "float",
                "label": "Float Test",
                "default": 3.14,
                "description": "A decimal value"
            },
            {
                "name": "test_bool",
                "type": "boolean",
                "label": "Boolean Test",
                "default": True,
                "description": "A toggle switch"
            },
            {
                "name": "test_date",
                "type": "date",
                "label": "Date Test",
                "default": datetime.now().strftime("%Y-%m-%d"),
                "description": "A date picker"
            },
            {
                "name": "test_json",
                "type": "json",
                "label": "JSON Test",
                "default": '{"status": "ok", "value": 100}',
                "description": "A JSON object input"
            },
            {
                "name": "test_list",
                "type": "list",
                "label": "List Test",
                "default": "item1,item2,item3",
                "description": "Comma separated list"
            }
        ]

        metadata = ToolMetadata(
            name="Complex Param Tester",
            category=ToolCategory.UTILITIES,
            version="3.0.0",
            author="Aleocrophic Team",
            description="Tests and displays various parameter types for verification",
            usage="aleopantest run complex-tester --target test --test-number 123",
            requirements=[],
            tags=["test", "utilities", "development"],
            form_schema=form_schema
        )
        super().__init__(metadata)

    def run(self, target: str, **kwargs) -> Dict[str, Any]:
        self.logger.info(f"Starting Complex Param Test on: {target}")
        
        # Process parameters using the base tool helper
        processed_params = self.process_parameters(kwargs)
        
        # Prepare results
        results = {
            "target": target,
            "raw_params": kwargs,
            "processed_params": processed_params,
            "type_check": {
                "test_number": str(type(processed_params.get("test_number"))),
                "test_float": str(type(processed_params.get("test_float"))),
                "test_bool": str(type(processed_params.get("test_bool"))),
                "test_json": str(type(processed_params.get("test_json"))),
                "test_list": str(type(processed_params.get("test_list")))
            }
        }
        
        self.logger.info("Complex Param Test completed successfully")
        return results

def get_tool():
    return ComplexParamTester()
