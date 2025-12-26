"""Password Generator Tool"""
import random
import string
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class PasswordGenerator(BaseTool):
    """Password generator untuk generate strong passwords"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Password Generator",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="AleoPantest",
            description="Password generator untuk generate secure dan random passwords",
            usage="gen = PasswordGenerator(); gen.run(length=16, count=5)",
            requirements=["random", "string"],
            tags=["utilities", "password", "security", "generator"]
        )
        super().__init__(metadata)
    
    def validate_input(self, length: int = 16, count: int = 1, **kwargs) -> bool:
        """Validate input"""
        if length < 4 or length > 256:
            self.add_error("Length harus antara 4-256")
            return False
        if count < 1 or count > 100:
            self.add_error("Count harus antara 1-100")
            return False
        return True
    
    def generate_password(self, length: int, include_special: bool = True) -> str:
        """Generate single password"""
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
    
    def generate_wordlist_password(self, length: int = 3) -> str:
        """Generate password menggunakan random words"""
        # Common words untuk generate
        words = [
            'alpha', 'beta', 'delta', 'gamma', 'epsilon', 'zeta',
            'blue', 'red', 'green', 'yellow', 'purple', 'orange',
            'cat', 'dog', 'bird', 'fish', 'tiger', 'eagle',
            'fast', 'slow', 'quick', 'swift', 'rapid', 'steady',
            'mountain', 'river', 'ocean', 'forest', 'desert', 'valley',
        ]
        
        selected_words = [random.choice(words) for _ in range(length)]
        password = '-'.join(selected_words)
        password += f"{random.randint(0, 9999)}"
        password += random.choice(string.punctuation)
        
        return password
    
    def run(self, length: int = 16, count: int = 1, include_special: bool = True, 
            use_wordlist: bool = False, **kwargs):
        """Generate passwords"""
        if not self.validate_input(length, count, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            logger.info(f"Generating {count} passwords (length: {length})")
            
            passwords = []
            
            for i in range(count):
                if use_wordlist:
                    pwd = self.generate_wordlist_password(length=3)
                else:
                    pwd = self.generate_password(length, include_special)
                
                passwords.append(pwd)
                self.add_result({'password': pwd, 'index': i + 1})
                logger.debug(f"Generated: {pwd}")
            
            result = {
                'count': count,
                'length': length,
                'include_special': include_special,
                'passwords': passwords
            }
            
            logger.info(f"Password generation completed")
            return result
            
        except Exception as e:
            self.add_error(f"Password generation failed: {e}")
        finally:
            self.is_running = False
