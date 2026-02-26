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
        # 1. Start with Default
        config = cls.DEFAULT_CONFIG.copy()
        
        # 2. Try to load from .env (Minimal parser to avoid dependencies)
        if os.path.exists(".env"):
            try:
                with open(".env", 'r') as f:
                    for line in f:
                        if "=" in line and not line.startswith("#"):
                            k, v = line.strip().split("=", 1)
                            # Map .env keys to config keys
                            env_map = {
                                "DB_HOST": "db_host",
                                "DB_USER": "db_user",
                                "DB_PASSWORD": "db_password",
                                "DB_NAME": "db_name"
                            }
                            if k in env_map:
                                config[env_map[k]] = v
            except Exception:
                pass

        # 3. Overlay with config.json if it exists
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    json_config = json.load(f)
                    config.update(json_config)
            except Exception:
                pass
                
        return config

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
