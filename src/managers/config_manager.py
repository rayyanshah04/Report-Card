"""
Config Manager - Handles loading/saving configuration files
"""

import json
from pathlib import Path


class ConfigManager:
    """Manages application configuration"""

    # Point to your existing config folder
    CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    @staticmethod
    def load():
        """Load configuration from config/config.json"""
        try:
            if ConfigManager.CONFIG_FILE.exists():
                with open(ConfigManager.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                print(f"Config file not found at {ConfigManager.CONFIG_FILE}")
                return {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    @staticmethod
    def save(config):
        """Save configuration to config/config.json"""
        try:
            ConfigManager.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(ConfigManager.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    @staticmethod
    def get_sessions():
        """Get list of available sessions"""
        config = ConfigManager.load()
        return config.get("sessions", [])

    @staticmethod
    def get_subjects():
        """Get list of subjects"""
        config = ConfigManager.load()
        return config.get("subjects", [])

    @staticmethod
    def get_max_marks_options():
        """Get available max marks options"""
        config = ConfigManager.load()
        return config.get("max_marks_options", [100])

    @staticmethod
    def get_default_session():
        """Get default session"""
        config = ConfigManager.load()
        return config.get("default_session", "2025-2026")

    @staticmethod
    def get_default_max_marks():
        """Get default max marks"""
        config = ConfigManager.load()
        return config.get("default_max_marks", 100)
