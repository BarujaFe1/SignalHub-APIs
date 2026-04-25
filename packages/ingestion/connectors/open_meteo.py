"""Open-Meteo Weather Connector.

Fetches current weather data for Berlin (V1 fixed location).
No API key required.
"""

import httpx
from datetime import datetime, timezone
from typing import Any

from packages.ingestion.base import BaseConnector, SignalRecord


class OpenMeteoConnector(BaseConnector):
    source_slug = "open-meteo"
    source_name = "Open-Meteo Weather"

    def __init__(self, latitude: float = 52.52, longitude: float = 13.41):
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    async def fetch(self) -> dict[str, Any]:
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "UTC",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()

    def validate_raw(self, raw: dict[str, Any]) -> bool:
        if "current" not in raw:
            return False
        current = raw["current"]
        required = ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]
        return all(k in current for k in required)

    def normalize(self, raw: dict[str, Any]) -> list[SignalRecord]:
        current = raw["current"]
        observed_at = datetime.now(timezone.utc)

        # Parse time if available
        if "time" in current:
            try:
                observed_at = datetime.fromisoformat(current["time"].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass

        return [
            SignalRecord(
                signal_type="weather",
                signal_key="temperature_celsius",
                signal_value=float(current["temperature_2m"]),
                signal_unit="°C",
                observed_at=observed_at,
                metadata={"location": "Berlin", "latitude": self.latitude, "longitude": self.longitude},
            ),
            SignalRecord(
                signal_type="weather",
                signal_key="humidity_percent",
                signal_value=float(current["relative_humidity_2m"]),
                signal_unit="%",
                observed_at=observed_at,
                metadata={"location": "Berlin"},
            ),
            SignalRecord(
                signal_type="weather",
                signal_key="wind_speed_kmh",
                signal_value=float(current["wind_speed_10m"]),
                signal_unit="km/h",
                observed_at=observed_at,
                metadata={"location": "Berlin"},
            ),
        ]
