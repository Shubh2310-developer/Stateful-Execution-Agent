import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class AppConfig(BaseModel):
    name: str = "Stateful Execution Agent"
    version: str = "0.1.0"
    env: EnvType = EnvType.DEVELOPMENT


class LLMConfig(BaseModel):
    provider: str = "groq"
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.0
    max_tokens: int = 4096
    api_key: Optional[str] = None


class DatabaseConfig(BaseModel):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "agent_state"
    postgres_uri: str = "postgresql://postgres:postgres@localhost:5432/agent_db"


class StorageConfig(BaseModel):
    local_root: str = "./data/storage"


class SecurityConfig(BaseModel):
    api_key_header: str = "X-API-KEY"
    jwt_secret: str = "super-secret-key"
    jwt_algorithm: str = "HS256"


def load_yaml_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AGENT_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    app: AppConfig = AppConfig()
    llm: LLMConfig = LLMConfig()
    database: DatabaseConfig = DatabaseConfig()
    storage: StorageConfig = StorageConfig()
    security: SecurityConfig = SecurityConfig()

    @classmethod
    def load(cls) -> "Settings":
        config_dir = Path(__file__).parent.parent.parent / "config"

        # Load default
        config_data = load_yaml_config(config_dir / "default.yaml")

        # Determine environment
        env = os.getenv("AGENT_APP__ENV", config_data.get("app", {}).get("env", "development"))

        # Load environment specific config
        env_config = load_yaml_config(config_dir / f"{env}.yaml")

        # Deep merge (simple version for this structure)
        for key, value in env_config.items():
            if key in config_data and isinstance(config_data[key], dict) and isinstance(value, dict):
                config_data[key].update(value)
            else:
                config_data[key] = value

        return cls(**config_data)


# Global settings instance
settings = Settings.load()
