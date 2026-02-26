import json
import os

class ConfigManager:
    """Manages persistent application configuration."""
    
    CONFIG_FILE = "config.json"
    DEFAULT_CONFIG = {
        "db_host": "localhost",
        "db_user": "root",
        "db_password": "",
        "db_name": "movie_booking"
    }

    @classmethod
    def load_config(cls):
        if not os.path.exists(cls.CONFIG_FILE):
            cls.save_config(cls.DEFAULT_CONFIG)
            return cls.DEFAULT_CONFIG
        
        try:
            with open(cls.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return cls.DEFAULT_CONFIG

    @classmethod
    def save_config(cls, config):
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    @classmethod
    def update_db_credentials(cls, host, user, password, database):
        config = cls.load_config()
        config["db_host"] = host
        config["db_user"] = user
        config["db_password"] = password
        config["db_name"] = database
        cls.save_config(config)
