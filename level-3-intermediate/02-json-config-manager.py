"""
JSON Config Manager
====================
Difficulty: 2/5
Estimated time: 15 minutes

Problem:
--------
Create a ConfigManager class that:
1. Loads configuration from a JSON file (creates a default if missing).
2. Allows getting values by key (supports nested keys via dot notation).
3. Allows setting values by key (supports nested keys via dot notation).
4. Saves the current configuration back to the JSON file.
5. Resets configuration to defaults.

Concepts practiced:
- json module (load, dump)
- File I/O
- Dictionary traversal with dot-notation keys
- Default/fallback values

Expected output (example):
--------------------------
# Created default config at app_config.json
# theme        = dark
# font.size    = 14
# font.family  = Courier New
#
# Setting theme to 'light' ...
# Setting font.size to 18 ...
# Adding new key 'language' = 'en' ...
#
# theme        = light
# font.size    = 18
# language     = en
#
# Config saved to app_config.json
# Config reset to defaults.
"""

import json
import os


class ConfigManager:
    """Manage application configuration stored as JSON."""

    DEFAULT_CONFIG = {
        "theme": "dark",
        "font": {
            "size": 14,
            "family": "Courier New",
        },
        "window": {
            "width": 1024,
            "height": 768,
        },
        "autosave": True,
    }

    def __init__(self, filepath):
        """
        Initialize the config manager.

        Parameters:
            filepath (str): Path to the JSON config file.
        """
        self.filepath = filepath
        self.config = {}
        self.load()

    def load(self):
        """Load config from file, or create a default config if file does not exist."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            print(f"Loaded config from {self.filepath}")
        else:
            self.config = json.loads(json.dumps(self.DEFAULT_CONFIG))  # deep copy
            self.save()
            print(f"Created default config at {self.filepath}")

    def save(self):
        """Save the current configuration to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
        print(f"Config saved to {self.filepath}")

    def get(self, key, default=None):
        """
        Get a config value by key. Supports dot notation for nested keys.

        Parameters:
            key (str): Dot-separated key path (e.g. 'font.size').
            default: Value to return if the key is not found.

        Returns:
            The value at the key path, or the default.
        """
        keys = key.split(".")
        current = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def set(self, key, value):
        """
        Set a config value by key. Supports dot notation for nested keys.
        Creates intermediate dictionaries as needed.

        Parameters:
            key (str): Dot-separated key path.
            value: Value to set.
        """
        keys = key.split(".")
        current = self.config
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def delete(self, key):
        """
        Delete a config key. Supports dot notation.

        Parameters:
            key (str): Dot-separated key path.

        Returns:
            bool: True if the key was deleted, False if not found.
        """
        keys = key.split(".")
        current = self.config
        for k in keys[:-1]:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return False
        if keys[-1] in current:
            del current[keys[-1]]
            return True
        return False

    def reset(self):
        """Reset configuration to defaults."""
        self.config = json.loads(json.dumps(self.DEFAULT_CONFIG))
        print("Config reset to defaults.")

    def display(self, prefix=""):
        """Recursively display all config key-value pairs."""
        self._display_dict(self.config, prefix)

    def _display_dict(self, d, prefix):
        for key, value in d.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self._display_dict(value, full_key)
            else:
                print(f"  {full_key:20s} = {value}")


if __name__ == "__main__":
    config_path = "app_config.json"

    # Create manager (will create default config)
    mgr = ConfigManager(config_path)

    # Display some values
    print(f"\ntheme        = {mgr.get('theme')}")
    print(f"font.size    = {mgr.get('font.size')}")
    print(f"font.family  = {mgr.get('font.family')}")
    print(f"missing.key  = {mgr.get('missing.key', 'N/A')}")

    # Modify values
    print("\nSetting theme to 'light' ...")
    mgr.set("theme", "light")

    print("Setting font.size to 18 ...")
    mgr.set("font.size", 18)

    print("Adding new key 'language' = 'en' ...")
    mgr.set("language", "en")

    # Show updated
    print(f"\ntheme        = {mgr.get('theme')}")
    print(f"font.size    = {mgr.get('font.size')}")
    print(f"language     = {mgr.get('language')}")

    # Save
    print()
    mgr.save()

    # Display full config
    print("\nFull configuration:")
    mgr.display()

    # Reset
    print()
    mgr.reset()

    # Cleanup
    os.remove(config_path)
    print(f"Cleaned up {config_path}.")
