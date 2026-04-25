"""Frankfurter API contracts."""

from typing import Any
from pydantic import BaseModel, Field


class FrankfurterInputParams(BaseModel):
    """Input parameters for Frankfurter API requests."""
    
    base: str = Field(
        default="EUR",
        description="Base currency code"
    )
    symbols: list[str] = Field(
        default=["USD", "GBP", "BRL", "JPY"],
        description="Target currency codes"
    )


class FrankfurterRawResponse(BaseModel):
    """Raw response envelope from Frankfurter API.
    
    Validates minimum required structure while allowing extra fields.
    """
    
    amount: float
    base: str
    date: str
    rates: dict[str, float] = Field(
        ...,
        description="Currency code to exchange rate mapping"
    )
    
    class Config:
        extra = "allow"


class FrankfurterExpectedErrors:
    """Known error conditions from Frankfurter API."""
    
    INVALID_CURRENCY = "Invalid currency code"
    TIMEOUT = "Request timeout"
    NO_DATA = "No exchange rate data available"
