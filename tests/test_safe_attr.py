import unittest
from aleopantest.core.tool_helper import get_safe_attr
from aleopantest.core.base_tool import ToolMetadata, ToolCategory

class MockObject:
    def __init__(self, metadata=None):
        self.metadata = metadata

class TestSafeAttr(unittest.TestCase):
    def test_get_safe_attr_simple(self):
        """Test basic attribute access"""
        obj = MockObject()
        obj.name = "Test"
        self.assertEqual(get_safe_attr(obj, "name"), "Test")
        self.assertEqual(get_safe_attr(obj, "nonexistent", "Default"), "Default")

    def test_get_safe_attr_nested(self):
        """Test nested attribute access"""
        metadata = ToolMetadata(
            name="Test Tool",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="Author",
            description="Desc",
            usage="Usage",
            requirements=[],
            tags=[]
        )
        obj = MockObject(metadata=metadata)
        
        self.assertEqual(get_safe_attr(obj, "metadata.name"), "Test Tool")
        self.assertEqual(get_safe_attr(obj, "metadata.category.value"), "Network")
        self.assertEqual(get_safe_attr(obj, "metadata.nonexistent", "Default"), "Default")

    def test_get_safe_attr_none_cases(self):
        """Test various None cases"""
        # Case 1: Object is None
        self.assertEqual(get_safe_attr(None, "metadata.name", "Default"), "Default")
        
        # Case 2: Intermediate attribute is None
        obj = MockObject(metadata=None)
        self.assertEqual(get_safe_attr(obj, "metadata.name", "Default"), "Default")
        
        # Case 3: Deeply nested None
        class FakeCategory:
            def __init__(self):
                self.value = None
        
        class FakeMetadata:
            def __init__(self):
                self.category = FakeCategory()
        
        obj = MockObject(metadata=FakeMetadata())
        self.assertEqual(get_safe_attr(obj, "metadata.category.value", "Default"), "Default")

    def test_get_safe_attr_dict(self):
        """Test dictionary access support"""
        obj = {
            "metadata": {
                "category": {
                    "value": "Web"
                }
            }
        }
        self.assertEqual(get_safe_attr(obj, "metadata.category.value"), "Web")
        self.assertEqual(get_safe_attr(obj, "metadata.nonexistent", "Default"), "Default")

if __name__ == '__main__':
    unittest.main()
