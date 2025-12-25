"""Configuration management for AloPantest"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
import yaml

from .logger import logger


class Config:
    """Global configuration manager"""
    
    # Default configuration
    DEFAULTS = {
        'timeout': 30,
        'retries': 3,
        'thread_count': 5,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'proxy': None,
        'verbose': False,
        'output_dir': 'output',
        'log_dir': 'logs',
        'cache_enabled': True,
        'cache_ttl': 3600,
    }
    
    def __init__(self, config_file: Optional[str] = None):
        self.config: Dict[str, Any] = self.DEFAULTS.copy()
        self.config_file = config_file
        
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories"""
        dirs = [self.config['output_dir'], self.config['log_dir']]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def load_config(self, config_file: str):
        """Load configuration from file (JSON or YAML)"""
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.json'):
                    data = json.load(f)
                elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    data = yaml.safe_load(f)
                else:
                    logger.warning(f"Unknown config file format: {config_file}")
                    return
            
            self.config.update(data)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    
    def save_config(self, config_file: str):
        """Save configuration to file"""
        try:
            Path(config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                if config_file.endswith('.json'):
                    json.dump(self.config, f, indent=2)
                elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    yaml.dump(self.config, f)
            logger.info(f"Configuration saved to {config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any):
        self.config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config.copy()


# Global config instance
config = Config()
