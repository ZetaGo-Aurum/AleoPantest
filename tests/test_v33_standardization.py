import unittest
import time
from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class MockTool(BaseTool):
    def run(self, duration=0, **kwargs):
        self.start_time = time.time()
        if not self.check_safety(duration):
            return self.get_results()
        
        # Simulate some work
        self.add_result({"data": "test_result"})
        return self.get_results()

class TestV33Standardization(unittest.TestCase):
    def setUp(self):
        self.metadata = ToolMetadata(
            name="Test Tool",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="Test",
            description="Test Description",
            usage="test",
            requirements=[],
            tags=["test"],
            risk_level="HIGH"
        )
        self.tool = MockTool(self.metadata)

    def test_check_safety_integer(self):
        """Test check_safety with integer duration"""
        self.assertTrue(self.tool.check_safety(60))
        self.assertEqual(len(self.tool.errors), 0)

    def test_check_safety_string(self):
        """Test check_safety with string duration that should be converted"""
        self.assertTrue(self.tool.check_safety("60"))
        self.assertEqual(len(self.tool.errors), 0)

    def test_check_safety_invalid_string(self):
        """Test check_safety with non-numeric string"""
        self.assertFalse(self.tool.check_safety("invalid"))
        self.assertIn("Type Error", self.tool.errors[0])

    def test_check_safety_negative(self):
        """Test check_safety with negative duration"""
        self.assertFalse(self.tool.check_safety(-10))
        self.assertIn("tidak boleh negatif", self.tool.errors[0])

    def test_check_safety_none(self):
        """Test check_safety with None"""
        self.assertTrue(self.tool.check_safety(None))
        self.assertEqual(len(self.tool.errors), 0)

    def test_check_safety_limit(self):
        """Test check_safety with duration exceeding limit (3600s)"""
        self.assertFalse(self.tool.check_safety(3601))
        self.assertIn("Safety Limit", self.tool.errors[0])

    def test_json_output_format(self):
        """Test the standardized JSON output format"""
        self.tool.run(duration=10)
        output = self.tool.get_results()
        
        # Check required fields
        self.assertIn("status", output)
        self.assertIn("tool_metadata", output)
        self.assertIn("results", output)
        self.assertIn("error_message", output)
        self.assertIn("execution_details", output)
        
        # Check execution_details fields
        details = output["execution_details"]
        self.assertIn("duration_seconds", details)
        self.assertIn("results_count", details)
        self.assertIn("errors_count", details)
        self.assertIn("warnings_count", details)
        self.assertIn("timestamp", details)
        self.assertIn("admin_info", details)
        
        # Check values
        self.assertEqual(output["status"], "completed")
        self.assertEqual(len(output["results"]), 1)
        self.assertEqual(details["results_count"], 1)

if __name__ == "__main__":
    unittest.main()
