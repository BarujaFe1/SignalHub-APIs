"""Open-Meteo API contracts."""

from pydantic import BaseModel, ConfigDict, Field


class OpenMeteoInputParams(BaseModel):
    """Input parameters for Open-Meteo API requests."""
    
    latitude: float = Field(
        default=52.52,
        description="Latitude coordinate (Berlin default)"
    )
    longitude: float = Field(
        default=13.41,
        description="Longitude coordinate (Berlin default)"
    )


class OpenMeteoCurrentWeather(BaseModel):
    """Current weather data structure from Open-Meteo."""
    
    time: str
    temperature_2m: float
    relative_humidity_2m: float
    wind_speed_10m: float
    weather_code: int | None = None
    
    model_config = ConfigDict(extra="allow")


class OpenMeteoRawResponse(BaseModel):
    """Raw response envelope from Open-Meteo API.
    
    Validates minimum required structure while allowing extra fields.
    """
    
    latitude: float
    longitude: float
    timezone: str
    current: OpenMeteoCurrentWeather
    
    model_config = ConfigDict(extra="allow")


class OpenMeteoExpectedErrors:
    """Known error conditions from Open-Meteo API."""
    
    INVALID_COORDINATES = "Invalid latitude or longitude"
    TIMEOUT = "Request timeout"
    RATE_LIMIT = "Rate limit exceeded"
