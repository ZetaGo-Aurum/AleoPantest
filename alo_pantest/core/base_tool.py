"""Base tool framework untuk semua tools"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

from ..core.logger import logger


class ToolCategory(Enum):
    """Tool categories"""
    NETWORK = "Network"
    WEB = "Web"
    OSINT = "OSINT"
    CRYPTO = "Crypto"
    WIRELESS = "Wireless"
    DATABASE = "Database"
    UTILITIES = "Utilities"
    REVERSE = "Reverse Engineering"
    PHISHING = "Phishing"
    SECURITY = "Security"
    CLICKJACKING = "Clickjacking"


@dataclass
class ToolMetadata:
    """Metadata untuk setiap tool"""
    name: str
    category: ToolCategory
    version: str
    author: str
    description: str
    usage: str
    requirements: list
    tags: list
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    legal_disclaimer: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'category': self.category.value,
            'version': self.version,
            'author': self.author,
            'description': self.description,
            'usage': self.usage,
            'requirements': self.requirements,
            'tags': self.tags,
            'risk_level': self.risk_level,
            'legal_disclaimer': self.legal_disclaimer,
        }


class BaseTool(ABC):
    """Base class untuk semua tools"""
    
    def __init__(self, metadata: ToolMetadata):
        self.metadata = metadata
        self.results = []
        self.errors = []
        self.is_running = False
    
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute tool"""
        pass
    
    @abstractmethod
    def validate_input(self, *args, **kwargs) -> bool:
        """Validate input parameters"""
        pass
    
    def add_result(self, result: Any):
        """Add result"""
        self.results.append(result)
    
    def add_error(self, error: str):
        """Add error"""
        self.errors.append(error)
        logger.error(f"[{self.metadata.name}] {error}")
    
    def get_results(self) -> list:
        """Get all results"""
        return self.results
    
    def clear_results(self):
        """Clear results"""
        self.results.clear()
        self.errors.clear()
    
    def export_json(self, filepath: str):
        """Export results to JSON"""
        try:
            data = {
                'tool': self.metadata.name,
                'results': self.results,
                'errors': self.errors,
            }
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Results exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
    
    def __repr__(self):
        return f"<{self.metadata.name} v{self.metadata.version}>"
