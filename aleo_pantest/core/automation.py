"""Intelligent automation and context detection for Aleocrophic"""
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
        if tool_id in ['port-scan', 'ip-scan', 'ping', 'traceroute', 'net-speed', 'arp-scan', 'vlan-scan']:
            params['host'] = info.get('ip') or info.get('domain') or target
            if tool_id == 'port-scan':
                params['port'] = '1-1000'
            if tool_id == 'arp-scan':
                params['range'] = target
            if tool_id == 'vlan-scan':
                params['interface'] = 'eth0'
                
        elif tool_id in ['dns', 'whois', 'subdomain', 'domain-info', 'whois-history', 'api-analyzer']:
            params['domain'] = info.get('domain') or target
            if tool_id == 'api-analyzer':
                params['url'] = target if info['type'] == 'url' else f"http://{target}"
            
        elif tool_id in ['sql-inject', 'xss-detect', 'csrf-detect', 'crawler', 'vuln-scan', 'web-phishing', 'tech-stack', 'dir-brute', 'link-extract', 'admin-finder', 'headers-analyzer']:
            params['url'] = target if info['type'] == 'url' else f"http://{target}"
            
        elif tool_id in ['sql-brute', 'mongodb-audit']:
            params['host'] = info.get('ip') or info.get('domain') or target
            params['port'] = 3306 if tool_id == 'sql-brute' else 27017

        elif tool_id in ['email-find', 'email-phishing', 'breach-check']:
            if info['type'] == 'email':
                params['email'] = target
                params['target'] = target
            else:
                params['domain'] = info.get('domain') or target
                params['target'] = target
                
        elif tool_id in ['ip-geo', 'ip-info', 'shodan-search', 'sql-brute', 'mongodb-audit']:
            params['ip'] = info.get('ip') or target
            params['host'] = info.get('ip') or target
            if tool_id == 'sql-brute':
                params['user'] = 'root'
                params['port'] = 3306

        elif tool_id == 'subnet-calc':
            params['cidr'] = target

        elif tool_id == 'mac-lookup':
            params['mac'] = target

        elif tool_id in ['user-search', 'social-analyzer']:
            params['username'] = target

        elif tool_id == 'git-recon':
            params['org'] = target

        elif tool_id == 'phone-lookup':
            params['phone'] = target

        elif tool_id == 'base64':
            params['data'] = target
            params['action'] = 'encode'

        elif tool_id == 'json-format':
            params['data'] = target

        elif tool_id == 'jwt-decoder':
            params['token'] = target

        elif tool_id in ['hash-cracker', 'hash-gen', 'vigenere', 'xor-cipher', 'ids-evasion']:
            if tool_id == 'hash-cracker':
                params['hash_str'] = target
            elif tool_id == 'ids-evasion':
                params['payload'] = target
                params['method'] = 'hex'
            else:
                params['text'] = target
                if tool_id == 'vigenere':
                    params['key'] = 'ALEO'
                    params['action'] = 'encrypt'
                if tool_id == 'xor-cipher':
                    params['key'] = 'ALEO'

        elif tool_id == 'metadata-exif':
            params['file'] = target

        elif tool_id == 'proxy-finder':
            params['type'] = 'http'

        return params
