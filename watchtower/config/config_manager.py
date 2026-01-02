"""
Configuration Manager for Watchtower Field System
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Manages Watchtower configuration files.

    Stores:
    - System configuration
    - Glyph-to-trigger mappings
    - Daemon settings
    - Threshold definitions
    """

    DEFAULT_CONFIG = {
        'version': '1.0.0',
        'watchtower': {
            'name': 'Watchtower Field Container',
            'mode': 'production'
        },
        'daemon': {
            'enabled': True,
            'watch_paths': [],
            'trigger_patterns': ['*.field', '*.glyph'],
            'authorization_mode': 'consent_required',
            'log_level': 'info'
        },
        'thresholds': {
            'low': {
                'consent_required': False,
                'log': True,
                'notify': False,
                'audit': False
            },
            'medium': {
                'consent_required': False,
                'log': True,
                'notify': True,
                'audit': False
            },
            'high': {
                'consent_required': True,
                'log': True,
                'notify': True,
                'audit': False
            },
            'critical': {
                'consent_required': True,
                'log': True,
                'notify': True,
                'audit': True
            }
        },
        'ui': {
            'theme': 'symbolic',
            'show_glyphs': True,
            'animations': True,
            'window_size': [1200, 800]
        }
    }

    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            watchtower_dir = Path.home() / '.watchtower'
            watchtower_dir.mkdir(exist_ok=True, parents=True)
            config_path = watchtower_dir / 'config.json'

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from disk or create default"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(self.DEFAULT_CONFIG, config)
        else:
            # Create default config
            config = self.DEFAULT_CONFIG.copy()
            self.save()
            return config

    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Supports nested keys with dot notation: 'daemon.enabled'
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value.

        Supports nested keys with dot notation: 'daemon.enabled'
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self):
        """Save configuration to disk"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()

    def export(self, path: Path):
        """Export configuration to specified path"""
        with open(path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return self.config.copy()
