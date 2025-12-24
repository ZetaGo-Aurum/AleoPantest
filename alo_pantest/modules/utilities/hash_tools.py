"""Hash Tools untuk berbagai hashing algorithms"""
import hashlib
from typing import Dict, Any

from ...core.base_tool import BaseTool, ToolMetadata, ToolCategory
from ...core.logger import logger


class HashTools(BaseTool):
    """Hash tools untuk generate dan verify berbagai hash types"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="Hash Tools",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="AloPantest",
            description="Hash tools untuk generate MD5, SHA1, SHA256, SHA512 dan hash lainnya",
            usage="hasher = HashTools(); hasher.run(text='hello world', algorithm='sha256')",
            requirements=["hashlib"],
            tags=["utilities", "hash", "security", "cryptography"]
        )
        super().__init__(metadata)
        
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512,
        }
    
    def validate_input(self, text: str = None, file_path: str = None, algorithm: str = 'sha256', **kwargs) -> bool:
        """Validate input"""
        if not text and not file_path:
            self.add_error("Text atau file_path harus disediakan")
            return False
        
        if algorithm.lower() not in self.algorithms:
            self.add_error(f"Algorithm {algorithm} tidak didukung")
            return False
        
        return True
    
    def hash_text(self, text: str, algorithm: str) -> str:
        """Hash text"""
        hash_func = self.algorithms[algorithm.lower()]
        return hash_func(text.encode()).hexdigest()
    
    def hash_file(self, file_path: str, algorithm: str) -> str:
        """Hash file"""
        try:
            hash_func = self.algorithms[algorithm.lower()]
            hasher = hash_func()
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except FileNotFoundError:
            self.add_error(f"File not found: {file_path}")
            return None
        except Exception as e:
            self.add_error(f"Error hashing file: {e}")
            return None
    
    def run(self, text: str = None, file_path: str = None, algorithm: str = 'sha256', 
            all_algorithms: bool = False, **kwargs):
        """Generate hash"""
        if not self.validate_input(text, file_path, algorithm, **kwargs):
            return
        
        self.is_running = True
        self.clear_results()
        
        try:
            result = {}
            
            if text:
                logger.info(f"Hashing text with {algorithm}")
                
                if all_algorithms:
                    # Hash dengan semua algorithms
                    for algo in self.algorithms.keys():
                        hash_result = self.hash_text(text, algo)
                        result[algo] = hash_result
                        self.add_result({'algorithm': algo, 'hash': hash_result})
                else:
                    # Hash dengan algorithm tertentu
                    hash_result = self.hash_text(text, algorithm)
                    result[algorithm] = hash_result
                    self.add_result({'algorithm': algorithm, 'hash': hash_result})
                
                result['input'] = text[:50]  # Limit display
            
            elif file_path:
                logger.info(f"Hashing file: {file_path}")
                
                if all_algorithms:
                    for algo in self.algorithms.keys():
                        hash_result = self.hash_file(file_path, algo)
                        if hash_result:
                            result[algo] = hash_result
                            self.add_result({'algorithm': algo, 'hash': hash_result})
                else:
                    hash_result = self.hash_file(file_path, algorithm)
                    if hash_result:
                        result[algorithm] = hash_result
                        self.add_result({'algorithm': algorithm, 'hash': hash_result})
                
                result['file'] = file_path
            
            logger.info("Hash generation completed")
            return result
            
        except Exception as e:
            self.add_error(f"Hash generation failed: {e}")
        finally:
            self.is_running = False
