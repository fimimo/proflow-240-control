"""Configuration Management"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Application Configuration"""
    
    DEFAULT_CONFIG = {
        'theme': 'dark',
        'window': {
            'width': 1200,
            'height': 800,
            'maximized': False
        },
        'device': {
            'vendor_id': 0x33C3,
            'product_id': 0x7792,
            'auto_connect': True
        },
        'display': {
            'width': 320,
            'height': 480
        },
        'media': {
            'last_directory': str(Path.home()),
            'auto_scale': True,
            'max_video_frames': 100
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".proflow-240"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """
        Load configuration from file
        
        Returns:
            configuration dict
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
                return config
            except Exception as e:
                logger.warning(f"Error loading config, using defaults: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """
        Save configuration to file
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """
        Get configuration value
        
        Args:
            key: configuration key (supports dot notation)
            default: default value if key not found
        
        Returns:
            configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value):
        """
        Set configuration value
        
        Args:
            key: configuration key (supports dot notation)
            value: value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
