import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aleo_pantest.modules.network.ddos_simulator import DDoSSimulator

class TestDDoSSimulator(unittest.TestCase):
    def setUp(self):
        self.tool = DDoSSimulator()

    @patch('requests.get')
    def test_http_flood(self, mock_get):
        # Test HTTP flood with 1 thread and 1 second duration
        # We use a short duration to keep tests fast
        results = self.tool.run(target="localhost", type="http", duration=1, threads=1)
        self.assertIn("[*] Memulai simulasi HTTP flood ke localhost...", results)
        self.assertTrue(any("[+] Simulasi selesai" in r for r in results))
        self.assertEqual(len(self.tool.errors), 0)

    @patch('aleo_pantest.modules.network.ddos_simulator.send')
    @patch('aleo_pantest.modules.network.ddos_simulator.HAS_SCAPY', True)
    def test_syn_flood(self, mock_send):
        # Mock Scapy classes
        with patch('aleo_pantest.modules.network.ddos_simulator.IP'), \
             patch('aleo_pantest.modules.network.ddos_simulator.TCP'):
            results = self.tool.run(target="127.0.0.1", type="syn", duration=1)
            self.assertIn("[*] Memulai simulasi SYN flood ke 127.0.0.1...", results)
            self.assertTrue(any("[+] Simulasi selesai" in r for r in results))
            self.assertEqual(len(self.tool.errors), 0)

    @patch('aleo_pantest.modules.network.ddos_simulator.send')
    @patch('aleo_pantest.modules.network.ddos_simulator.HAS_SCAPY', True)
    def test_udp_flood(self, mock_send):
        with patch('aleo_pantest.modules.network.ddos_simulator.IP'), \
             patch('aleo_pantest.modules.network.ddos_simulator.UDP'), \
             patch('aleo_pantest.modules.network.ddos_simulator.Raw'):
            results = self.tool.run(target="127.0.0.1", type="udp", duration=1)
            self.assertIn("[*] Memulai simulasi UDP flood ke 127.0.0.1...", results)
            self.assertTrue(any("[+] Simulasi selesai" in r for r in results))
            self.assertEqual(len(self.tool.errors), 0)

    @patch('aleo_pantest.modules.network.ddos_simulator.send')
    @patch('aleo_pantest.modules.network.ddos_simulator.HAS_SCAPY', True)
    def test_dns_flood(self, mock_send):
        with patch('aleo_pantest.modules.network.ddos_simulator.IP'), \
             patch('aleo_pantest.modules.network.ddos_simulator.UDP'), \
             patch('aleo_pantest.modules.network.ddos_simulator.DNS'), \
             patch('aleo_pantest.modules.network.ddos_simulator.DNSQR'):
            results = self.tool.run(target="example.com", type="dns", duration=1)
            self.assertIn("[*] Memulai simulasi DNS flood ke example.com...", results)
            self.assertTrue(any("[+] Simulasi selesai" in r for r in results))
            self.assertEqual(len(self.tool.errors), 0)

    @patch('socket.socket')
    def test_slowloris(self, mock_socket):
        mock_s = MagicMock()
        mock_socket.return_value = mock_s
        
        # Test slowloris with 1 thread and 1 second duration
        # Slowloris has a 15s sleep in its loop, so we need to be careful with timing
        # or mock time.sleep
        with patch('time.sleep'):
            results = self.tool.run(target="localhost", type="slowloris", duration=1, threads=1)
            self.assertIn("[*] Memulai simulasi SLOWLORIS flood ke localhost...", results)
            self.assertTrue(any("[+] Simulasi selesai" in r for r in results))
            self.assertEqual(len(self.tool.errors), 0)
            mock_s.close.assert_called()

    def test_safety_limit(self):
        # Test duration > 3600s (1 hour)
        results = self.tool.run(target="localhost", type="http", duration=3601)
        self.assertTrue(any("Safety Limit" in e for e in self.tool.errors))

if __name__ == '__main__':
    unittest.main()
