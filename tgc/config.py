import os
import json
from typing import Any, Dict

CONFIG_FILE = "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "api_id": "",
    "api_hash": "",
    "language": "en",
    "theme": "darkly",
    "last_group_file": "",
    "session_file": "dynamic_session.session"
}

class ConfigManager:
    """Manages application configuration persistence."""

    def __init__(self, file_path: str = CONFIG_FILE):
        self.file_path = file_path
        self.config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> Dict[str, Any]:
        """Loads configuration from JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"[ConfigManager] Error loading config: {e}")
        return self.config

    def save(self) -> bool:
        """Saves current configuration to JSON file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save()

    def update(self, kwargs: Dict[str, Any]) -> None:
        self.config.update(kwargs)
        self.save()
