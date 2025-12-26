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
            version="1.1.0",
            author="AleoPantest",
            description="IP geolocation untuk mendapatkan lokasi geografis dari IP address dengan informasi lengkap",
            usage="""
Examples:
  geo = IPGeolocation(); geo.run(ip='8.8.8.8')
  geo = IPGeolocation(); geo.run(host='1.1.1.1')  # 'host' alias for 'ip'
  
CLI Usage:
  aleopantest run ip-geo --ip 8.8.8.8
  aleopantest run ip-geo --host 1.1.1.1
            """,
            requirements=["requests"],
            tags=["osint", "geolocation", "ip", "reconnaissance", "location-lookup"]
        )
        super().__init__(metadata)
    
    def validate_input(self, ip: str = None, host: str = None, **kwargs) -> bool:
        """Validate input - accept both 'ip' and 'host' parameters"""
        # Support 'host' as alias for 'ip'
        target_ip = ip or host
        
        if not target_ip:
            self.add_error("IP address is required (provide 'ip' or 'host' parameter)")
            return False
        
        # Basic IP validation
        parts = target_ip.strip().split('.')
        if len(parts) != 4:
            self.add_error(f"Invalid IP format: {target_ip}")
            return False
        
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    self.add_error(f"Invalid IP format: {target_ip} (octets must be 0-255)")
                    return False
            except ValueError:
                self.add_error(f"Invalid IP format: {target_ip}")
                return False
        
        return True
    
    def lookup_ip_info(self, ip: str) -> Dict[str, Any]:
        """Lookup IP information using free APIs"""
        info = {'ip': ip, 'source': 'multiple_apis'}
        
        # Try multiple free IP geolocation APIs
        apis = [
            {
                'url': f"https://ipapi.co/{ip}/json/",
                'name': 'ipapi.co',
                'fields': ['country', 'country_code', 'region', 'city',
                          'latitude', 'longitude', 'postal', 'timezone', 'isp', 'org']
            },
            {
                'url': f"https://ip-api.com/json/{ip}",
                'name': 'ip-api.com',
                'fields': ['country', 'countryCode', 'region', 'city',
                          'lat', 'lon', 'zip', 'timezone', 'isp', 'org', 'as']
            },
        ]
        
        for api_config in apis:
            try:
                response = requests.get(api_config['url'], timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract common fields with mapping
                    field_mapping = {
                        'lat': 'latitude',
                        'lon': 'longitude',
                        'zip': 'postal',
                        'countryCode': 'country_code',
                    }
                    
                    for field in api_config['fields']:
                        mapped_field = field_mapping.get(field, field)
                        if field in data:
                            info[mapped_field] = data[field]
                    
                    info['source'] = api_config['name']
                    return info
            except requests.RequestException as e:
                logger.warning(f"API {api_config['name']} failed: {e}")
                continue
            except Exception as e:
                logger.warning(f"Error processing {api_config['name']} response: {e}")
                continue
        
        return info
    
    def run(self, ip: str = None, host: str = None, **kwargs):
        """
        Perform IP geolocation lookup
        
        Args:
            ip: IP address to lookup
            host: Alias for IP address (accepts either parameter)
        """
        # Support 'host' as alias for 'ip'
        target_ip = ip or host
        
        if not self.validate_input(ip=ip, host=host, **kwargs):
            return None
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Performing geolocation lookup for IP: {target_ip}")
            
            info = self.lookup_ip_info(target_ip)
            
            result = {
                'success': True,
                'ip': target_ip,
                'location_info': info,
                'status': 'Geolocation lookup completed successfully'
            }
            
            self.add_result(result)
            logger.info(f"Geolocation lookup completed for {target_ip}")
            return result
            
        except Exception as e:
            self.add_error(f"Geolocation lookup failed: {e}")
            return None
        finally:
            self.is_running = False
