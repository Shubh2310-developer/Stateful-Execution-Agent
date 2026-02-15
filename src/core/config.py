import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class AppConfig(BaseModel):
    name: str = "Stateful Execution Agent"
    version: str = "0.1.0"
    env: EnvType = EnvType.DEVELOPMENT
    api_v1_str: str = "/api/v1"
    debug: bool = True


class LLMConfig(BaseModel):
    provider: str = "groq"
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.0
    max_tokens: int = 4096
    api_key: Optional[str] = None


class DatabaseConfig(BaseModel):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "agent_state"
    postgres_uri: str = "postgresql://postgres:postgres@localhost:5432/agent_db"


class StorageConfig(BaseModel):
    local_root: str = "./data/storage"


class CacheConfig(BaseModel):
    enabled: bool = True
    redis_uri: str = "redis://localhost:6379/0"
    ttl: Dict[str, int] = {
        "task_state": 300,      # 5 minutes
        "user_memory": 600,     # 10 minutes
        "task_artifacts": 300,  # 5 minutes
    }



class RateLimitConfig(BaseModel):
    requests_per_minute: int = 3000
    enabled: bool = False


class SecurityConfig(BaseModel):
    api_key_header: str = "X-API-KEY"
    api_key: str = "dev-api-key-12345"
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
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app: AppConfig = AppConfig()
    llm: LLMConfig = LLMConfig()
    database: DatabaseConfig = DatabaseConfig()
    storage: StorageConfig = StorageConfig()
    cache: CacheConfig = CacheConfig()
    security: SecurityConfig = SecurityConfig()
    ratelimit: RateLimitConfig = RateLimitConfig()

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

        # Override with environment variable for GROQ_API_KEY if available
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            if "llm" not in config_data:
                config_data["llm"] = {}
            config_data["llm"]["api_key"] = groq_key

        # Update Database Config from Environment
        mongodb_url = os.getenv("MONGODB_URL")
        if mongodb_url:
            if "database" not in config_data:
                config_data["database"] = {}
            config_data["database"]["mongodb_uri"] = mongodb_url

        postgres_url = os.getenv("POSTGRES_URL")
        if postgres_url:
            if "database" not in config_data:
                config_data["database"] = {}
            config_data["database"]["postgres_uri"] = postgres_url

        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_server = os.getenv("POSTGRES_SERVER")
        postgres_port = os.getenv("POSTGRES_PORT")
        postgres_db = os.getenv("POSTGRES_DB")

        if postgres_user and postgres_password and postgres_server:
             # Construct URI if individual components are present but full URL might be missing or we want to be safe
             # prioritizing full URL if exists, but for now let's just stick to the direct URL map
             pass

        # Update Cache Config from Environment
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        if redis_host:
             if "cache" not in config_data:
                config_data["cache"] = {}
             # Construct redis URI. Defaulting port to 6379 if not set but host is set
             r_port = redis_port if redis_port else "6379"
             config_data["cache"]["redis_uri"] = f"redis://{redis_host}:{r_port}/0"

        # Update Rate Limit Config from Environment
        rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE")
        if rate_limit:
            if "ratelimit" not in config_data:
                config_data["ratelimit"] = {}
            try:
                config_data["ratelimit"]["requests_per_minute"] = int(rate_limit)
            except ValueError:
                pass # Use default if invalid


        return cls(**config_data)


# Global settings instance
settings = Settings.load()
