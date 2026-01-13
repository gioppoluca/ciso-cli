from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CISO_", extra="ignore")

    url: AnyHttpUrl = Field(..., description="Base URL of CISO Assistant instance")
    api_token: str = Field(..., min_length=10, description="API token for CISO Assistant")
    timeout: int = Field(default=30, ge=1, le=300)
    verify_tls: bool = Field(default=True)


def get_settings() -> Settings:
    return Settings()
