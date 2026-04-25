"""CoinGecko API contracts."""

from typing import Any
from pydantic import BaseModel, Field


class CoinGeckoInputParams(BaseModel):
    """Input parameters for CoinGecko API requests."""
    
    coin_ids: list[str] = Field(
        default=["bitcoin", "ethereum", "solana"],
        description="CoinGecko coin identifiers"
    )
    vs_currency: str = Field(
        default="usd",
        description="Target currency for prices"
    )
    include_24hr_change: bool = Field(
        default=True,
        description="Include 24h price change percentage"
    )
    include_market_cap: bool = Field(
        default=True,
        description="Include market capitalization"
    )


class CoinGeckoCoinData(BaseModel):
    """Price data for a single coin."""
    
    usd: float
    usd_24h_change: float | None = None
    usd_market_cap: float | None = None
    
    class Config:
        extra = "allow"


class CoinGeckoRawResponse(BaseModel):
    """Raw response envelope from CoinGecko API.
    
    Dynamic structure: keys are coin IDs, values are price data.
    Validates that expected coins are present.
    """
    
    bitcoin: CoinGeckoCoinData | None = None
    ethereum: CoinGeckoCoinData | None = None
    solana: CoinGeckoCoinData | None = None
    
    class Config:
        extra = "allow"


class CoinGeckoExpectedErrors:
    """Known error conditions from CoinGecko API."""
    
    INVALID_COIN_ID = "Invalid coin identifier"
    RATE_LIMIT = "Rate limit exceeded (30 calls/min for free tier)"
    API_KEY_REQUIRED = "API key required for this endpoint"
    TIMEOUT = "Request timeout"
