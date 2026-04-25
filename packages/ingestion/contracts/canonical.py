"""Canonical signal format — the unified data model for all sources."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class NormalizedSignal(BaseModel):
    """Unified signal format across all data sources.
    
    All connectors transform their raw data into this canonical structure.
    """
    
    signal_type: str = Field(
        ...,
        description="Type of signal: 'weather', 'exchange_rate', 'crypto_price'"
    )
    signal_key: str = Field(
        ...,
        description="Unique identifier for this signal: 'temperature_celsius', 'EUR_USD', 'bitcoin_usd'"
    )
    signal_value: float = Field(
        ...,
        description="Numeric value of the signal"
    )
    signal_unit: str = Field(
        ...,
        description="Unit of measurement: '°C', 'USD', '%', 'km/h'"
    )
    observed_at: datetime = Field(
        ...,
        description="Timestamp when this data was observed (UTC)"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (location, source, etc.)"
    )
