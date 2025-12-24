"""IP Geolocation Tool"""
import requests
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class IPGeolocation(BaseTool):
    """IP geolocation tool untuk dapatkan informasi geografis dari IP address"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="IP Geolocation",
            category=ToolCategory.OSINT,
            version="1.0.0",
            author="AloPantest",
            description="IP geolocation untuk mendapatkan lokasi geografis dari IP address",
            usage="geo = IPGeolocation(); geo.run(ip='8.8.8.8')",
            requirements=["requests"],
            tags=["osint", "geolocation", "ip", "reconnaissance"]
        )
        super().__init__(metadata)
    
    def validate_input(self, ip: str, **kwargs) -> bool:
        """Validate input"""
        if not ip:
            self.add_error("IP tidak boleh kosong")
            return False
        
        # Basic IP validation
        parts = ip.split('.')
        if len(parts) != 4:
            self.add_error("Invalid IP format")
            return False
        
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    self.add_error("Invalid IP format")
                    return False
            except ValueError:
                self.add_error("Invalid IP format")
                return False
        
        return True
    
    def lookup_ip_info(self, ip: str) -> Dict[str, Any]:
        """Lookup IP information using free API"""
        info = {'ip': ip}
        
        # Try multiple free IP geolocation APIs
        apis = [
            f"https://ipapi.co/{ip}/json/",
            f"https://ip-api.com/json/{ip}",
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract common fields
                    fields = [
                        'country', 'country_code', 'region', 'city',
                        'latitude', 'latitude', 'longitude', 'postal',
                        'timezone', 'isp', 'org', 'as',
                    ]
                    
                    for field in fields:
                        if field in data:
                            info[field] = data[field]
                    
                    return info
            except:
                pass
        
        return info
    
    def run(self, ip: str, **kwargs):
        """Perform IP geolocation lookup"""
        if not self.validate_input(ip, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Performing geolocation lookup for IP: {ip}")
            
            info = self.lookup_ip_info(ip)
            
            result = {
                'ip': ip,
                'location_info': info
            }
            
            self.add_result(result)
            logger.info(f"Geolocation lookup completed for {ip}")
            return result
            
        except Exception as e:
            self.add_error(f"Geolocation lookup failed: {e}")
        finally:
            self.is_running = False
