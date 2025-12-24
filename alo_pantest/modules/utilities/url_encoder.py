"""URL Encoder/Decoder Tool"""
import urllib.parse
import base64
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class URLEncoder(BaseTool):
    """URL encoder/decoder untuk encoding dan decoding URLs dan payloads"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="URL Encoder/Decoder",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="AloPantest",
            description="URL encoder/decoder untuk encoding, decoding, dan transformasi URLs",
            usage="encoder = URLEncoder(); encoder.run(text='hello world', operation='encode')",
            requirements=["urllib", "base64"],
            tags=["utilities", "encoding", "url", "payload"]
        )
        super().__init__(metadata)
    
    def validate_input(self, text: str = None, operation: str = 'encode', **kwargs) -> bool:
        """Validate input"""
        if not text:
            self.add_error("Text tidak boleh kosong")
            return False
        
        if operation not in ['encode', 'decode', 'base64', 'base64decode', 'double']:
            self.add_error("Operation tidak valid")
            return False
        
        return True
    
    def url_encode(self, text: str) -> str:
        """URL encode"""
        return urllib.parse.quote(text)
    
    def url_decode(self, text: str) -> str:
        """URL decode"""
        return urllib.parse.unquote(text)
    
    def base64_encode(self, text: str) -> str:
        """Base64 encode"""
        return base64.b64encode(text.encode()).decode()
    
    def base64_decode(self, text: str) -> str:
        """Base64 decode"""
        try:
            return base64.b64decode(text).decode()
        except:
            return "Error decoding"
    
    def html_encode(self, text: str) -> str:
        """HTML entity encode"""
        return ''.join(f'&#x{ord(c):x};' for c in text)
    
    def double_encode(self, text: str) -> str:
        """Double URL encode"""
        return urllib.parse.quote(urllib.parse.quote(text))
    
    def run(self, text: str, operation: str = 'encode', **kwargs):
        """Perform encoding/decoding"""
        if not self.validate_input(text, operation, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Performing {operation} operation")
            
            result = {'input': text, 'operation': operation}
            
            if operation == 'encode':
                result['output'] = self.url_encode(text)
            elif operation == 'decode':
                result['output'] = self.url_decode(text)
            elif operation == 'base64':
                result['output'] = self.base64_encode(text)
            elif operation == 'base64decode':
                result['output'] = self.base64_decode(text)
            elif operation == 'double':
                result['output'] = self.double_encode(text)
            
            # Also provide additional formats
            result['formats'] = {
                'url_encoded': self.url_encode(text),
                'base64': self.base64_encode(text),
                'html': self.html_encode(text),
            }
            
            self.add_result(result)
            logger.info("Encoding/decoding completed")
            return result
            
        except Exception as e:
            self.add_error(f"Encoding failed: {e}")
        finally:
            self.is_running = False
