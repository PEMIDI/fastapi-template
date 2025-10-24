from functools import lru_cache
import os
from typing import List


class Settings:
    def __init__(self):
        # Default values
        self.PROJECT_NAME: str = "Katana Link"
        self.VERSION: str = "0.1.0"
        self.ENV: str = "development"
        self.DEBUG: bool = True
        self.ENABLE_DOCS: bool = True
        self.LOG_LEVEL: str = "INFO"
        
        # CORS
        self.BACKEND_CORS_ORIGINS: List[str] = ["*"]
        
        # Database - PostgreSQL only
        self.DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/katana"
        self.SQL_ECHO: bool = False
        self.SQL_POOL_SIZE: int = 5
        self.SQL_MAX_OVERFLOW: int = 10
        
        # Load from .env file
        self._load_from_env()
    
    def _load_from_env(self):
        """Load settings from .env file if it exists.

        Looks for the .env file in several locations, in order:
        1) ENV_FILE environment variable if set
        2) Project root relative to this file (two levels up from app/core)
        3) Current working directory
        """
        candidates = []

        # 1) Explicit path from environment variable
        env_file_env = os.getenv("ENV_FILE")
        if env_file_env:
            candidates.append(env_file_env)

        # 2) Project root (two levels up from this file)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        candidates.append(os.path.join(project_root, ".env"))

        # 3) Current working directory
        candidates.append(".env")

        env_file_path = next((p for p in candidates if os.path.exists(p)), None)

        if env_file_path:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse KEY=VALUE format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Set the attribute if it exists
                        self._set_attribute(key, value)

        # Override with environment variables (highest priority)
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Load settings from environment variables"""
        for key in dir(self):
            if key.isupper() and not key.startswith('_'):
                env_value = os.getenv(key)
                if env_value is not None:
                    self._set_attribute(key, env_value)
    
    def _set_attribute(self, key: str, value: str):
        """Set attribute with type conversion"""
        if not hasattr(self, key):
            return
        
        current_value = getattr(self, key)
        
        # Type conversion based on current type
        if isinstance(current_value, bool):
            # Handle boolean conversion
            setattr(self, key, value.lower() in ('true', '1', 'yes', 'on'))
        elif isinstance(current_value, int):
            try:
                setattr(self, key, int(value))
            except ValueError:
                pass
        elif isinstance(current_value, list):
            # Handle list conversion (comma-separated or JSON-like)
            if value.startswith('[') and value.endswith(']'):
                # Simple JSON-like list parsing
                value = value[1:-1]
                items = [item.strip().strip('"').strip("'") for item in value.split(',')]
                setattr(self, key, [item for item in items if item])
            else:
                # Comma-separated
                setattr(self, key, [item.strip() for item in value.split(',') if item.strip()])
        else:
            setattr(self, key, value)


@lru_cache
def get_settings() -> Settings:
    return Settings()
