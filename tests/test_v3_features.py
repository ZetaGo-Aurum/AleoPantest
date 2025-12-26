"""Unit tests for Aleocrophic V3.0 core features"""
import unittest
import time
from aleo_pantest.core.platform import PlatformDetector, PlatformOptimizer
from aleo_pantest.core.session import SessionManager, SecurityGuard
from aleo_pantest.core.automation import ContextDetector, AutomationEngine

class TestV3Core(unittest.TestCase):
    
    def test_platform_detector(self):
        """Test platform detection logic"""
        info = PlatformDetector.get_info()
        self.assertIn('system', info)
        self.assertIn('is_wsl', info)
        self.assertIn('is_termux', info)
        
        name = PlatformDetector.get_platform_name()
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    def test_platform_optimizer(self):
        """Test resource optimization"""
        threads = PlatformOptimizer.get_optimal_threads()
        self.assertIsInstance(threads, int)
        self.assertGreaterEqual(threads, 1)

    def test_session_manager(self):
        """Test session quota management"""
        session = SessionManager()
        self.assertTrue(session.is_active)
        self.assertGreater(session.get_remaining_time(), 0)
        
        status = session.get_status()
        self.assertIn('session_id', status)
        self.assertTrue(status['is_active'])
        
        # Test quota limit (manually adjust start_time for test)
        session.start_time = time.time() - 601
        self.assertFalse(session.check_quota())
        self.assertEqual(session.get_remaining_time(), 0)

    def test_security_guard(self):
        """Test safety limit enforcement"""
        # Test DDoS duration capping
        params = {'target': 'example.com', 'duration': 120, 'threads': 100}
        safe_params = SecurityGuard.enforce_limits('ddos-sim', params)
        
        self.assertLessEqual(safe_params['duration'], 60)
        self.assertLessEqual(safe_params['threads'], PlatformOptimizer.get_optimal_threads())

    def test_context_detector(self):
        """Test intelligent context detection"""
        # URL
        self.assertEqual(ContextDetector.detect_target_type("https://google.com"), 'url')
        # IP
        self.assertEqual(ContextDetector.detect_target_type("8.8.8.8"), 'ip')
        # Domain
        self.assertEqual(ContextDetector.detect_target_type("example.com"), 'domain')
        # Email
        self.assertEqual(ContextDetector.detect_target_type("test@example.com"), 'email')

    def test_automation_engine(self):
        """Test automatic parameter filling"""
        # Port scan automation
        params = AutomationEngine.auto_fill_params('port-scan', '127.0.0.1')
        self.assertEqual(params['host'], '127.0.0.1')
        self.assertEqual(params['port'], '1-1000')
        
        # DNS automation
        params = AutomationEngine.auto_fill_params('dns', 'example.com')
        self.assertEqual(params['domain'], 'example.com')

if __name__ == '__main__':
    unittest.main()
