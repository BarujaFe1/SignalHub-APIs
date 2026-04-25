"""Data contracts for SignalHub connectors.

This module defines explicit input/output contracts for each data source,
making the data pipeline transparent and maintainable.
"""

from packages.ingestion.contracts.canonical import NormalizedSignal
from packages.ingestion.contracts.open_meteo import (
    OpenMeteoInputParams,
    OpenMeteoRawResponse,
)
from packages.ingestion.contracts.frankfurter import (
    FrankfurterInputParams,
    FrankfurterRawResponse,
)
from packages.ingestion.contracts.coingecko import (
    CoinGeckoInputParams,
    CoinGeckoRawResponse,
)

__all__ = [
    "NormalizedSignal",
    "OpenMeteoInputParams",
    "OpenMeteoRawResponse",
    "FrankfurterInputParams",
    "FrankfurterRawResponse",
    "CoinGeckoInputParams",
    "CoinGeckoRawResponse",
]
