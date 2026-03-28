"""
Jarvis Settings - Extends the existing ConfigManager with Jarvis-specific config.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Import the existing config system
sys_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
sys.path.insert(0, sys_path)
from multi_ai_framework.config.config_manager import ConfigManager


DEFAULT_JARVIS_CONFIG = {
    "assistant": {
        "name": "Jarvis",
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 4096,
        "wake_word": "hey jarvis",
    },
    "voice": {
        "enabled": False,
        "stt_engine": "whisper_api",  # whisper_api, whisper_local, google
        "tts_engine": "elevenlabs",   # elevenlabs, pyttsx3
        "elevenlabs_voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "pyttsx3_rate": 175,
        "pyttsx3_volume": 0.9,
        "wake_word_enabled": False,
        "push_to_talk_key": "ctrl+space",
        "toggle_key": "ctrl+shift+v",
    },
    "tools": {
        "macos_enabled": True,
        "web_enabled": True,
        "code_enabled": True,
        "smart_home_enabled": False,
        "hivemind_enabled": False,
    },
    "smart_home": {
        "backend": "homeassistant",  # homeassistant, homekit
        "homeassistant_url": "",
        "homeassistant_token": "",
    },
    "web": {
        "search_engine": "brave",  # brave, tavily, serpapi
        "brave_api_key": "",
        "tavily_api_key": "",
    },
}


class JarvisSettings:
    """Manages Jarvis-specific settings, built on top of ConfigManager."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._default_path()
        self.config: Dict[str, Any] = {}
        self._load()

        # Reuse ConfigManager for API keys
        self.api_keys = ConfigManager()

    def _default_path(self) -> str:
        config_dir = Path.home() / ".jarvis"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")

    def _load(self) -> None:
        """Load config from file, merged with defaults."""
        self.config = dict(DEFAULT_JARVIS_CONFIG)

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    loaded = json.load(f)
                self._deep_merge(self.config, loaded)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

    def _deep_merge(self, base: dict, override: dict) -> None:
        """Recursively merge override into base."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def save(self) -> None:
        """Save current config to file (excludes API keys)."""
        save_data = {k: v for k, v in self.config.items()}
        # Strip any sensitive fields
        if "smart_home" in save_data:
            save_data["smart_home"] = {
                k: v for k, v in save_data["smart_home"].items()
                if k not in ("homeassistant_token",)
            }
        with open(self.config_path, "w") as f:
            json.dump(save_data, f, indent=2)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a config value by section and key."""
        return self.config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        """Set a config value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    @property
    def model(self) -> str:
        return self.get("assistant", "model", "claude-sonnet-4-5-20250929")

    @property
    def max_tokens(self) -> int:
        return self.get("assistant", "max_tokens", 4096)

    @property
    def assistant_name(self) -> str:
        return self.get("assistant", "name", "Jarvis")

    @property
    def anthropic_api_key(self) -> Optional[str]:
        return os.getenv("ANTHROPIC_API_KEY") or self.api_keys.get_api_key("anthropic")
