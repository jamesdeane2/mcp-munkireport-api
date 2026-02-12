"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Backend API configuration
    api_url: str = "http://localhost:5030"
    api_key: str = ""

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    class Config:
        env_prefix = "MUNKIREPORT_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
