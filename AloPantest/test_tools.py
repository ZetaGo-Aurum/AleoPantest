#!/usr/bin/env python3
"""
Test script untuk AloPantest
Untuk verify semua tools berfungsi dengan baik
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from alo_pantest.core.logger import logger
from alo_pantest.modules.network import PortScanner, PingTool, DNSLookup
from alo_pantest.modules.web import SQLInjector, SubdomainFinder
from alo_pantest.modules.osint import IPGeolocation, DomainInfo
from alo_pantest.modules.utilities import PasswordGenerator, HashTools, URLEncoder

def test_network_tools():
    """Test network tools"""
    print("\n" + "="*50)
    print("Testing Network Tools")
    print("="*50)
    
    # Test DNS
    print("\n[*] Testing DNS Lookup...")
    dns = DNSLookup()
    result = dns.run(domain='example.com')
    assert result, "DNS lookup failed"
    print(f"[✓] DNS Lookup: {result}")
    
    # Test Ping
    print("\n[*] Testing Ping...")
    ping = PingTool()
    result = ping.run(host='8.8.8.8', count=2)
    assert result, "Ping failed"
    print(f"[✓] Ping: Host reachable")

def test_web_tools():
    """Test web tools"""
    print("\n" + "="*50)
    print("Testing Web Tools")
    print("="*50)
    
    # Test Subdomain Finder
    print("\n[*] Testing Subdomain Finder...")
    finder = SubdomainFinder()
    result = finder.run(domain='example.com')
    assert result, "Subdomain finder failed"
    print(f"[✓] Subdomain Finder: Found {result.get('subdomains_found', 0)} subdomains")

def test_osint_tools():
    """Test OSINT tools"""
    print("\n" + "="*50)
    print("Testing OSINT Tools")
    print("="*50)
    
    # Test IP Geolocation
    print("\n[*] Testing IP Geolocation...")
    geo = IPGeolocation()
    result = geo.run(ip='8.8.8.8')
    assert result, "Geolocation failed"
    print(f"[✓] IP Geolocation: Success")
    
    # Test Domain Info
    print("\n[*] Testing Domain Info...")
    info = DomainInfo()
    result = info.run(domain='example.com')
    assert result, "Domain info failed"
    print(f"[✓] Domain Info: Success")

def test_utility_tools():
    """Test utility tools"""
    print("\n" + "="*50)
    print("Testing Utility Tools")
    print("="*50)
    
    # Test Password Generator
    print("\n[*] Testing Password Generator...")
    gen = PasswordGenerator()
    result = gen.run(length=16, count=1)
    assert result and 'passwords' in result, "Password generation failed"
    print(f"[✓] Password Generator: {result['passwords'][0]}")
    
    # Test Hash Tools
    print("\n[*] Testing Hash Tools...")
    hasher = HashTools()
    result = hasher.run(text='test', algorithm='sha256')
    assert result and 'sha256' in result, "Hash generation failed"
    print(f"[✓] Hash Tools: {result['sha256'][:16]}...")
    
    # Test URL Encoder
    print("\n[*] Testing URL Encoder...")
    encoder = URLEncoder()
    result = encoder.run(text='hello world', operation='encode')
    assert result and 'output' in result, "URL encoding failed"
    print(f"[✓] URL Encoder: {result['output']}")

def run_all_tests():
    """Run semua tests"""
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " AloPantest - Tool Test Suite ".center(48) + "║")
    print("╚" + "="*48 + "╝")
    
    tests = [
        ("Network Tools", test_network_tools),
        ("Web Tools", test_web_tools),
        ("OSINT Tools", test_osint_tools),
        ("Utility Tools", test_utility_tools),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n[✗] {test_name} failed: {e}")
            logger.exception(f"Test failed: {test_name}")
            failed += 1
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"[✓] Passed: {passed}")
    print(f"[✗] Failed: {failed}")
    print(f"[*] Total: {passed + failed}")
    
    if failed == 0:
        print("\n✓ All tests passed! AloPantest is ready to use.")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed. Please check your installation.")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
