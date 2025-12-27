"""Unit tests for Aleopantest V3.2 release features"""
import unittest
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Mock missing dependencies before importing modules
sys.modules['shodan'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['pymongo'] = MagicMock()
sys.modules['ngrok'] = MagicMock()
sys.modules['pyngrok'] = MagicMock()

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory
from aleopantest.modules.security.vuln_db import VulnDB
from aleopantest.modules.osint.shodan_search import ShodanSearch
from aleopantest.modules.crypto.stegano import SteganoTool
from aleopantest.core.automation import AutomationEngine

class TestV32Release(unittest.TestCase):
    
    def test_vuln_db_schema(self):
        """Test VulnDB tool schema and functionality"""
        tool = VulnDB()
        self.assertIn('form_schema', tool.metadata.__dict__)
        self.assertTrue(any(field['name'] == 'query' for field in tool.metadata.form_schema))
        self.assertTrue(any(field['name'] == 'timeout' for field in tool.metadata.form_schema))
        
        # Test validation
        self.assertTrue(tool.validate_input(query="CVE-2021-44228"))
        self.assertFalse(tool.validate_input(query=""))

    def test_shodan_search_schema(self):
        """Test ShodanSearch tool schema"""
        tool = ShodanSearch()
        self.assertTrue(any(field['name'] == 'api_key' for field in tool.metadata.form_schema))
        self.assertTrue(tool.validate_input(query="apache", api_key="test_key"))
        self.assertFalse(tool.validate_input(query="", api_key=""))

    def test_stegano_tool_schema(self):
        """Test SteganoTool tool schema"""
        tool = SteganoTool()
        self.assertTrue(any(field['name'] == 'mode' for field in tool.metadata.form_schema))
        self.assertTrue(tool.validate_input(file="test.png"))

    def test_common_form_schema(self):
        """Test that common form schema is added to tools"""
        tools_to_test = [VulnDB(), ShodanSearch(), SteganoTool()]
        for tool in tools_to_test:
            names = [field['name'] for field in tool.metadata.form_schema]
            self.assertIn('timeout', names)
            self.assertIn('headers', names)
            self.assertIn('proxy', names)

    def test_automation_new_tools(self):
        """Test automation for new database tools"""
        params = AutomationEngine.auto_fill_params('sql-brute', '192.168.1.1')
        self.assertEqual(params['host'], '192.168.1.1')
        self.assertEqual(params['port'], 3306)
        
        params = AutomationEngine.auto_fill_params('mongodb-audit', '127.0.0.1')
        self.assertEqual(params['host'], '127.0.0.1')
        self.assertEqual(params['port'], 27017)

if __name__ == '__main__':
    unittest.main()
