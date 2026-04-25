"""Tests for connectors — validate fetch, validate, normalize."""

import pytest
from datetime import datetime, timezone


# ─── Open-Meteo ───────────────────────────────────────────

class TestOpenMeteoConnector:
    def test_validate_raw_valid(self):
        from packages.ingestion.connectors.open_meteo import OpenMeteoConnector

        connector = OpenMeteoConnector()
        raw = {
            "current": {
                "temperature_2m": 8.2,
                "relative_humidity_2m": 73,
                "wind_speed_10m": 14.5,
                "time": "2024-01-15T10:00",
            }
        }
        assert connector.validate_raw(raw) is True

    def test_validate_raw_missing_field(self):
        from packages.ingestion.connectors.open_meteo import OpenMeteoConnector

        connector = OpenMeteoConnector()
        raw = {"current": {"temperature_2m": 8.2}}
        assert connector.validate_raw(raw) is False

    def test_validate_raw_no_current(self):
        from packages.ingestion.connectors.open_meteo import OpenMeteoConnector

        connector = OpenMeteoConnector()
        assert connector.validate_raw({}) is False

    def test_normalize(self):
        from packages.ingestion.connectors.open_meteo import OpenMeteoConnector

        connector = OpenMeteoConnector()
        raw = {
            "current": {
                "temperature_2m": 8.2,
                "relative_humidity_2m": 73,
                "wind_speed_10m": 14.5,
                "time": "2024-01-15T10:00",
            }
        }
        signals = connector.normalize(raw)
        assert len(signals) == 3
        assert signals[0].signal_key == "temperature_celsius"
        assert signals[0].signal_value == 8.2
        assert signals[1].signal_key == "humidity_percent"
        assert signals[2].signal_key == "wind_speed_kmh"


# ─── Frankfurter ──────────────────────────────────────────

class TestFrankfurterConnector:
    def test_validate_raw_valid(self):
        from packages.ingestion.connectors.frankfurter import FrankfurterConnector

        connector = FrankfurterConnector()
        raw = {
            "base": "EUR",
            "date": "2024-01-15",
            "rates": {"USD": 1.08, "GBP": 0.86, "BRL": 5.40, "JPY": 161.5},
        }
        assert connector.validate_raw(raw) is True

    def test_validate_raw_missing_symbol(self):
        from packages.ingestion.connectors.frankfurter import FrankfurterConnector

        connector = FrankfurterConnector()
        raw = {"rates": {"USD": 1.08}}
        assert connector.validate_raw(raw) is False

    def test_normalize(self):
        from packages.ingestion.connectors.frankfurter import FrankfurterConnector

        connector = FrankfurterConnector()
        raw = {
            "base": "EUR",
            "date": "2024-01-15",
            "rates": {"USD": 1.08, "GBP": 0.86, "BRL": 5.40, "JPY": 161.5},
        }
        signals = connector.normalize(raw)
        assert len(signals) == 4
        keys = {s.signal_key for s in signals}
        assert keys == {"EUR_USD", "EUR_GBP", "EUR_BRL", "EUR_JPY"}


# ─── CoinGecko ────────────────────────────────────────────

class TestCoinGeckoConnector:
    def test_validate_raw_valid(self):
        from packages.ingestion.connectors.coingecko import CoinGeckoConnector

        connector = CoinGeckoConnector()
        raw = {
            "bitcoin": {"usd": 97000, "usd_24h_change": 2.3, "usd_market_cap": 1900000000000},
            "ethereum": {"usd": 3400, "usd_24h_change": -0.5, "usd_market_cap": 400000000000},
            "solana": {"usd": 190, "usd_24h_change": 5.1, "usd_market_cap": 85000000000},
        }
        assert connector.validate_raw(raw) is True

    def test_validate_raw_missing_coin(self):
        from packages.ingestion.connectors.coingecko import CoinGeckoConnector

        connector = CoinGeckoConnector()
        raw = {"bitcoin": {"usd": 97000}}
        assert connector.validate_raw(raw) is False

    def test_normalize(self):
        from packages.ingestion.connectors.coingecko import CoinGeckoConnector

        connector = CoinGeckoConnector()
        raw = {
            "bitcoin": {"usd": 97000, "usd_24h_change": 2.3, "usd_market_cap": 1900000000000},
            "ethereum": {"usd": 3400, "usd_24h_change": -0.5, "usd_market_cap": 400000000000},
            "solana": {"usd": 190, "usd_24h_change": 5.1, "usd_market_cap": 85000000000},
        }
        signals = connector.normalize(raw)
        assert len(signals) == 3
        btc = next(s for s in signals if s.signal_key == "bitcoin_usd")
        assert btc.signal_value == 97000
        assert btc.metadata["change_24h"] == 2.3


# ─── Quality Checks ──────────────────────────────────────

class TestQualityChecks:
    def test_null_check_pass(self):
        from packages.ingestion.quality.checks import null_check
        from packages.ingestion.base import SignalRecord

        signals = [
            SignalRecord(signal_type="test", signal_key="k", signal_value=1.0, signal_unit="u", observed_at=datetime.now(timezone.utc)),
        ]
        result = null_check(signals, "test")
        assert result["check_status"] == "pass"

    def test_volume_check_pass(self):
        from packages.ingestion.quality.checks import volume_check
        from packages.ingestion.base import SignalRecord

        signals = [
            SignalRecord(signal_type="test", signal_key="k", signal_value=1.0, signal_unit="u", observed_at=datetime.now(timezone.utc)),
        ]
        result = volume_check(signals, 1, "test")
        assert result["check_status"] == "pass"

    def test_volume_check_fail(self):
        from packages.ingestion.quality.checks import volume_check

        result = volume_check([], 3, "test")
        assert result["check_status"] == "fail"

    def test_range_check_pass(self):
        from packages.ingestion.quality.checks import range_check
        from packages.ingestion.base import SignalRecord

        signals = [
            SignalRecord(signal_type="weather", signal_key="temperature_celsius", signal_value=20.0, signal_unit="°C", observed_at=datetime.now(timezone.utc)),
        ]
        result = range_check(signals, {"temperature_celsius": (-60.0, 60.0)})
        assert result["check_status"] == "pass"

    def test_range_check_warn(self):
        from packages.ingestion.quality.checks import range_check
        from packages.ingestion.base import SignalRecord

        signals = [
            SignalRecord(signal_type="weather", signal_key="temperature_celsius", signal_value=75.0, signal_unit="°C", observed_at=datetime.now(timezone.utc)),
        ]
        result = range_check(signals, {"temperature_celsius": (-60.0, 60.0)})
        assert result["check_status"] == "warn"
