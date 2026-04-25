"""Frankfurter Exchange Rate Connector.

Fetches EUR-based exchange rates for USD, GBP, BRL, JPY.
No API key required. Data sourced from ECB.
"""

import httpx
from datetime import datetime, timezone
from typing import Any

from packages.ingestion.base import BaseConnector, SignalRecord


SYMBOLS = ["USD", "GBP", "BRL", "JPY"]


class FrankfurterConnector(BaseConnector):
    source_slug = "frankfurter"
    source_name = "Frankfurter Exchange"

    def __init__(self):
        self.base_url = "https://api.frankfurter.dev/v1/latest"

    async def fetch(self) -> dict[str, Any]:
        params = {
            "base": "EUR",
            "symbols": ",".join(SYMBOLS),
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()

    def validate_raw(self, raw: dict[str, Any]) -> bool:
        if "rates" not in raw:
            return False
        rates = raw["rates"]
        return all(s in rates for s in SYMBOLS)

    def normalize(self, raw: dict[str, Any]) -> list[SignalRecord]:
        rates = raw["rates"]
        observed_at = datetime.now(timezone.utc)

        # Use the date from the API if available
        if "date" in raw:
            try:
                observed_at = datetime.strptime(raw["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                pass

        signals = []
        for symbol in SYMBOLS:
            if symbol in rates:
                signals.append(SignalRecord(
                    signal_type="exchange_rate",
                    signal_key=f"EUR_{symbol}",
                    signal_value=float(rates[symbol]),
                    signal_unit=symbol,
                    observed_at=observed_at,
                    metadata={"base": "EUR", "source": "ECB"},
                ))
        return signals
