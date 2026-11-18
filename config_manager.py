"""Configuration Manager for Da Goose Companion."""

import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": "2.1.0",
    "goose_skin": "classic",         # classic, smoking, coder, duck, cyberpunk, wizard, coffee
    "duck_scale": 1.0,
    "always_on_top": True,
    "sound_enabled": True,
    "chair_enabled": True,
    # AI Settings
    "gemini_api_key": "",
    "gemini_model": "gemini-3.8-flash",
    "ai_personality": "witty",
    "ai_auto_peek_interval": 0,
    # Anti-Doomscroll
    "doomscroll_enabled": True,
    "doomscroll_threshold_minutes": 10,
    "doomscroll_keywords": [
        "youtube", "tiktok", "reddit", "twitter", "x.com",
        "instagram", "facebook", "netflix", "twitch",
        "9gag", "pinterest", "bilibili"
    ],
    "last_x_position": None,
}


class ConfigManager:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            app_data = os.environ.get("APPDATA")
            self.config_dir = Path(app_data) / "DaGooseCompanion" if app_data else Path.home() / ".dagoosecompanion"
        else:
            self.config_dir = Path(config_dir)

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self._config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.config_file.exists():
            return DEFAULT_CONFIG.copy()
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
        except Exception as e:
            print(f"[Config] Error reading config: {e}. Using defaults.")
            return DEFAULT_CONFIG.copy()

    def save(self) -> bool:
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4)
            return True
        except Exception as e:
            print(f"[Config] Save error: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        self._config[key] = value
        if auto_save:
            self.save()

    def update(self, new_data: Dict[str, Any], auto_save: bool = True) -> None:
        self._config.update(new_data)
        if auto_save:
            self.save()

    @property
    def all(self) -> Dict[str, Any]:
        return self._config.copy()
