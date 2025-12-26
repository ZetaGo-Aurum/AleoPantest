"""Intelligent automation and context detection for AleoPantest"""
import re
import socket
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

class ContextDetector:
    """Detect context from input targets to automate tool selection and parameters"""
    
    @staticmethod
    def detect_target_type(target: str) -> str:
        """Detect if target is URL, IP, Domain, or Email"""
        target = target.strip()
        
        # URL detection
        if target.startswith(('http://', 'https://')):
            return 'url'
            
        # Email detection
        if re.match(r"[^@]+@[^@]+\.[^@]+", target):
            return 'email'
            
        # IP detection
        try:
            socket.inet_aton(target)
            return 'ip'
        except socket.error:
            pass
            
        # Domain detection (simplified)
        if '.' in target and not target.endswith('.'):
            return 'domain'
            
        return 'unknown'

    @staticmethod
    def extract_info(target: str) -> Dict[str, str]:
        """Extract relevant info from target based on its type"""
        target_type = ContextDetector.detect_target_type(target)
        info = {'type': target_type, 'original': target}
        
        if target_type == 'url':
            parsed = urlparse(target)
            info['domain'] = parsed.netloc
            info['path'] = parsed.path
            # Try to get IP for the domain
            try:
                info['ip'] = socket.gethostbyname(parsed.netloc.split(':')[0])
            except:
                pass
        elif target_type == 'domain':
            info['domain'] = target
            try:
                info['ip'] = socket.gethostbyname(target)
            except:
                pass
        elif target_type == 'ip':
            info['ip'] = target
            try:
                info['domain'] = socket.gethostbyaddr(target)[0]
            except:
                pass
        elif target_type == 'email':
            info['domain'] = target.split('@')[1]
            
        return info

class AutomationEngine:
    """Automate tool parameter mapping and execution workflow"""
    
    @staticmethod
    def auto_fill_params(tool_id: str, target: str) -> Dict[str, Any]:
        """Automatically fill parameters based on target context"""
        info = ContextDetector.extract_info(target)
        params = {}
        
        # Tool-specific automation logic
        if tool_id in ['port-scan', 'ip-scan', 'ping', 'traceroute']:
            params['host'] = info.get('ip') or info.get('domain') or target
            if tool_id == 'port-scan':
                params['port'] = '1-1000'
                
        elif tool_id in ['dns', 'whois', 'subdomain', 'domain-info']:
            params['domain'] = info.get('domain') or target
            
        elif tool_id in ['sql-inject', 'xss-detect', 'csrf-detect', 'crawler', 'vuln-scan', 'web-phishing']:
            params['url'] = target if info['type'] == 'url' else f"http://{target}"
            
        elif tool_id in ['email-find', 'email-phishing']:
            if info['type'] == 'email':
                params['email'] = target
            else:
                params['domain'] = info.get('domain') or target
                
        elif tool_id == 'ip-geo':
            params['ip'] = info.get('ip') or target

        return params
