"""SSL Certificate Checker Tool"""
import socket
import ssl
from datetime import datetime
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class SSLChecker(BaseTool):
    """SSL certificate checker untuk menganalisis sertifikat SSL/TLS"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="SSL Checker",
            category=ToolCategory.NETWORK,
            version="1.0.0",
            author="AloPantest",
            description="SSL certificate checker untuk analisis sertifikat SSL/TLS dan keamanan",
            usage="ssl = SSLChecker(); ssl.run(host='google.com', port=443)",
            requirements=["socket", "ssl"],
            tags=["network", "ssl", "tls", "certificate", "security"]
        )
        super().__init__(metadata)
    
    def validate_input(self, host: str, port: int = 443, **kwargs) -> bool:
        """Validate input"""
        if not host:
            self.add_error("Host tidak boleh kosong")
            return False
        if port < 1 or port > 65535:
            self.add_error("Port harus antara 1-65535")
            return False
        return True
    
    def run(self, host: str, port: int = 443, timeout: int = 10, **kwargs):
        """Get SSL certificate info"""
        if not self.validate_input(host, port, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Checking SSL certificate for {host}:{port}")
            
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Connect to server
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
            
            # Parse certificate information
            result = {
                'host': host,
                'port': port,
                'ssl_version': version,
                'cipher_suite': cipher[0] if cipher else None,
                'cipher_bits': cipher[2] if cipher else None,
            }
            
            # Subject
            if 'subject' in cert:
                subject = dict(x[0] for x in cert['subject'])
                result['subject'] = {
                    'commonName': subject.get('commonName'),
                    'organizationName': subject.get('organizationName'),
                    'countryName': subject.get('countryName'),
                }
            
            # Issuer
            if 'issuer' in cert:
                issuer = dict(x[0] for x in cert['issuer'])
                result['issuer'] = {
                    'commonName': issuer.get('commonName'),
                    'organizationName': issuer.get('organizationName'),
                }
            
            # Validity dates
            if 'notBefore' in cert:
                result['not_before'] = cert['notBefore']
            if 'notAfter' in cert:
                result['not_after'] = cert['notAfter']
                
                # Check expiration
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry - datetime.now()).days
                result['expires_in_days'] = days_left
                result['is_expired'] = days_left < 0
            
            # Alternative names
            if 'subjectAltName' in cert:
                result['alt_names'] = [name[1] for name in cert['subjectAltName']]
            
            # Serial number
            if 'serialNumber' in cert:
                result['serial_number'] = cert['serialNumber']
            
            self.add_result(result)
            logger.info(f"SSL check completed for {host}:{port}")
            return result
            
        except socket.timeout:
            self.add_error(f"Connection timeout to {host}:{port}")
        except ssl.SSLError as e:
            self.add_error(f"SSL error: {e}")
        except socket.gaierror:
            self.add_error(f"Cannot resolve hostname: {host}")
        except Exception as e:
            self.add_error(f"SSL check failed: {e}")
        finally:
            self.is_running = False
