"""SignalHub APIs — Configuration."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite+aiosqlite:///./signalhub.db"
    database_url_sync: str = "sqlite:///./signalhub.db"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    # Connectors
    coingecko_api_key: str = ""

    # Open-Meteo
    open_meteo_latitude: float = 52.52
    open_meteo_longitude: float = 13.41

    # Mock Data for restricted environments
    use_mock_data: bool = False

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
