"""CoinGecko Crypto Connector.

Fetches Bitcoin, Ethereum, Solana prices in USD.
API key optional via COINGECKO_API_KEY env var.
"""

import httpx
import os
from datetime import datetime, timezone
from typing import Any

from packages.ingestion.base import BaseConnector, SignalRecord


COINS = ["bitcoin", "ethereum", "solana"]


class CoinGeckoConnector(BaseConnector):
    source_slug = "coingecko"
    source_name = "CoinGecko Crypto"

    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
        self.api_key = os.environ.get("COINGECKO_API_KEY", "")

    async def fetch(self) -> dict[str, Any]:
        params = {
            "ids": ",".join(COINS),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
        }
        headers = {}
        if self.api_key:
            headers["x-cg-demo-api-key"] = self.api_key

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    def validate_raw(self, raw: dict[str, Any]) -> bool:
        return all(coin in raw for coin in COINS)

    def normalize(self, raw: dict[str, Any]) -> list[SignalRecord]:
        observed_at = datetime.now(timezone.utc)
        signals = []

        for coin in COINS:
            if coin in raw and "usd" in raw[coin]:
                data = raw[coin]
                signals.append(SignalRecord(
                    signal_type="crypto_price",
                    signal_key=f"{coin}_usd",
                    signal_value=float(data["usd"]),
                    signal_unit="USD",
                    observed_at=observed_at,
                    metadata={
                        "change_24h": data.get("usd_24h_change"),
                        "market_cap": data.get("usd_market_cap"),
                    },
                ))
        return signals
