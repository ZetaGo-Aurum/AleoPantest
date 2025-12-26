
import unittest
from aleo_pantest.modules.network.dns_lookup import DNSLookup

class TestDNSLookup(unittest.TestCase):
    def setUp(self):
        self.tool = DNSLookup()

    def test_dns_lookup_fields(self):
        domain = "google.com"
        result = self.tool.run(domain=domain)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('domain'), domain)
        self.assertEqual(result.get('lookup_type'), 'all')
        
        # Check for essential fields
        self.assertIn('a_records', result)
        self.assertIn('mx_records', result)
        self.assertIn('txt_records', result)
        self.assertIn('ns_records', result)
        
        # Check MX record structure
        if result['mx_records']:
            mx = result['mx_records'][0]
            self.assertIn('exchange', mx)
            self.assertIn('preference', mx)
            
    def test_dns_lookup_invalid_domain(self):
        domain = "nonexistent-domain-123456789.com"
        result = self.tool.run(domain=domain)
        
        # Even for nonexistent domains, it should return the structure
        self.assertEqual(result.get('domain'), domain)
        self.assertEqual(result.get('a_records'), [])

if __name__ == '__main__':
    unittest.main()
