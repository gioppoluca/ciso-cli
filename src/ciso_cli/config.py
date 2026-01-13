import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field


def _env_file() -> str | None:
    """
    Allow disabling dotenv loading by setting CISO_ENV_FILE="".
    Default: ".env"
    """
    v = os.getenv("CISO_ENV_FILE", ".env").strip()
    return v or None


class Settings(BaseSettings):
    # IMPORTANT: don't bind env_file at import time
    model_config = SettingsConfigDict(env_prefix="CISO_", extra="ignore")

    url: AnyHttpUrl = Field(..., description="Base URL of CISO Assistant instance")
    api_token: str = Field(..., min_length=10, description="API token for CISO Assistant")
    timeout: int = Field(default=30, ge=1, le=300)
    verify_tls: bool = Field(default=True)


def get_settings() -> Settings:
    # IMPORTANT: env file chosen at runtime (works with monkeypatch)
    return Settings(_env_file=_env_file())
