"""Base connector and shared contracts."""

from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel
from typing import Any


class SignalRecord(BaseModel):
    """A single normalized signal ready for persistence."""
    signal_type: str
    signal_key: str
    signal_value: float
    signal_unit: str
    observed_at: datetime
    metadata: dict[str, Any] = {}


class FetchResult(BaseModel):
    """Result of a raw API fetch."""
    raw_payload: dict[str, Any]
    fetched_at: datetime
    records_count: int


class ConnectorResult(BaseModel):
    """Full result of a connector execution."""
    signals: list[SignalRecord]
    raw_payload: dict[str, Any]
    payload_hash: str
    fetched_at: datetime
    records_fetched: int
    records_normalized: int


class BaseConnector(ABC):
    """Abstract base for all API connectors.

    Each connector implements:
    - fetch(): raw HTTP call
    - validate_raw(): verify response structure
    - normalize(): transform raw → SignalRecords
    """

    source_slug: str
    source_name: str

    @abstractmethod
    async def fetch(self) -> dict[str, Any]:
        """Fetch raw data from the external API."""
        ...

    @abstractmethod
    def validate_raw(self, raw: dict[str, Any]) -> bool:
        """Validate that the raw response has expected structure."""
        ...

    @abstractmethod
    def normalize(self, raw: dict[str, Any]) -> list[SignalRecord]:
        """Transform raw response into normalized signals."""
        ...

    async def execute(self) -> ConnectorResult:
        """Full pipeline: fetch → validate → normalize."""
        import hashlib
        import json
        from datetime import datetime, timezone

        raw = await self.fetch()
        fetched_at = datetime.now(timezone.utc)

        is_valid = self.validate_raw(raw)
        if not is_valid:
            raise ValueError(f"Raw payload validation failed for {self.source_slug}")

        signals = self.normalize(raw)

        payload_str = json.dumps(raw, sort_keys=True, default=str)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

        return ConnectorResult(
            signals=signals,
            raw_payload=raw,
            payload_hash=payload_hash,
            fetched_at=fetched_at,
            records_fetched=len(signals),
            records_normalized=len(signals),
        )
