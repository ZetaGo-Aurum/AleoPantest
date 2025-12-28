import unittest
from aleopantest.cli import TOOLS_REGISTRY
from aleopantest.core.base_tool import ToolCategory
from aleopantest.core.tool_helper import get_safe_attr

class TestToolCategories(unittest.TestCase):
    def test_all_tools_have_valid_category(self):
        """Verify that all tools in the registry have a valid category from ToolCategory Enum"""
        unknown_tools = []
        
        for tool_id, tool_class in TOOLS_REGISTRY.items():
            try:
                instance = tool_class()
                # Get the category value using the same logic as the CLI info command
                cat_value = get_safe_attr(instance, "metadata.category.value", None)
                
                # Check if it's "Unknown" or None
                if cat_value is None or cat_value == "Unknown":
                    unknown_tools.append(tool_id)
                
                # Verify it's actually in the Enum
                valid_values = [c.value for c in ToolCategory]
                if cat_value not in valid_values:
                    unknown_tools.append(f"{tool_id} (Invalid value: {cat_value})")
                    
            except Exception as e:
                unknown_tools.append(f"{tool_id} (Error: {str(e)})")
        
        self.assertEqual(len(unknown_tools), 0, f"The following tools have invalid or 'Unknown' categories: {unknown_tools}")

    def test_clickjacking_tools_categorization(self):
        """Specifically verify that clickjacking tools are correctly categorized"""
        cj_tools = ['clickjacking-check', 'clickjacking-make', 'anti-clickjacking']
        for tool_id in cj_tools:
            instance = TOOLS_REGISTRY[tool_id]()
            self.assertEqual(instance.metadata.category, ToolCategory.CLICKJACKING)

if __name__ == "__main__":
    unittest.main()
