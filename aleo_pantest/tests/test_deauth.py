import unittest
from unittest.mock import patch, MagicMock
from aleo_pantest.modules.wireless.deauth import DeauthTool

class TestDeauthTool(unittest.TestCase):
    def setUp(self):
        self.tool = DeauthTool()

    def test_metadata(self):
        self.assertEqual(self.tool.metadata.name, "WiFi Deauthentication")
        self.assertEqual(self.tool.metadata.version, "3.3.0")
        self.assertEqual(self.tool.metadata.risk_level, "HIGH")

    @patch('aleo_pantest.modules.wireless.deauth.sendp')
    @patch('aleo_pantest.modules.wireless.deauth.HAS_SCAPY', True)
    def test_run_success(self, mock_sendp):
        # Mocking scapy components if needed, but since we mock sendp it should be fine
        with patch('aleo_pantest.modules.wireless.deauth.RadioTap'), \
             patch('aleo_pantest.modules.wireless.deauth.Dot11'), \
             patch('aleo_pantest.modules.wireless.deauth.Dot11Deauth'):
            
            results = self.tool.run(
                target="00:11:22:33:44:55",
                client="AA:BB:CC:DD:EE:FF",
                iface="wlan0mon",
                count=10,
                burst=True
            )
            
            # Verify results
            self.assertFalse(self.tool.errors)
            self.assertTrue(any("Initial burst" in r for r in results))
            self.assertTrue(any("Serangan selesai" in r for r in results))
            
            # Verify sendp calls
            # 1 for burst (count=5), 1 for sustained (count=10//2=5)
            self.assertEqual(mock_sendp.call_count, 2)

    def test_invalid_mac(self):
        self.tool.run(target="invalid-mac")
        self.assertTrue(self.tool.errors)
        self.assertIn("Format BSSID tidak valid", self.tool.errors[0])

    @patch('aleo_pantest.modules.wireless.deauth.HAS_SCAPY', False)
    def test_missing_scapy(self):
        self.tool.run(target="00:11:22:33:44:55")
        self.assertTrue(self.tool.errors)
        self.assertIn("scapy' tidak ditemukan", self.tool.errors[0])

    def test_safety_limit(self):
        # 1 hour = 3600 seconds. count=100000, interval=0.1 => 10000s > 3600s
        self.tool.run(target="00:11:22:33:44:55", count=100000, interval=0.1)
        self.assertTrue(self.tool.errors)
        self.assertIn("melebihi batas maksimal", self.tool.errors[0])

if __name__ == '__main__':
    unittest.main()
