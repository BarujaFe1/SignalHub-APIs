"""Quality check functions.

Run after each connector execution to validate data quality.
Each check returns a result dict ready for persistence.
"""

from datetime import datetime, timezone
from typing import Any

from packages.ingestion.base import SignalRecord


def null_check(signals: list[SignalRecord], source_slug: str) -> dict:
    """Check that no critical signal values are null."""
    nulls = [s for s in signals if s.signal_value is None]
    if nulls:
        return {
            "check_name": "null_check",
            "check_status": "fail",
            "expected_value": "non-null",
            "actual_value": f"{len(nulls)} null values",
            "message": f"Found {len(nulls)} signals with null values.",
        }
    return {
        "check_name": "null_check",
        "check_status": "pass",
        "expected_value": "non-null",
        "actual_value": "all fields present",
        "message": "All critical fields are present and non-null.",
    }


def volume_check(signals: list[SignalRecord], expected_count: int, source_slug: str) -> dict:
    """Check that the expected number of signals was produced."""
    actual = len(signals)
    if actual == expected_count:
        return {
            "check_name": "volume_check",
            "check_status": "pass",
            "expected_value": str(expected_count),
            "actual_value": str(actual),
            "message": f"Expected {expected_count} signals, received {actual}.",
        }
    elif actual > 0:
        return {
            "check_name": "volume_check",
            "check_status": "warn",
            "expected_value": str(expected_count),
            "actual_value": str(actual),
            "message": f"Expected {expected_count} signals but received {actual}.",
        }
    else:
        return {
            "check_name": "volume_check",
            "check_status": "fail",
            "expected_value": str(expected_count),
            "actual_value": "0",
            "message": "No signals produced.",
        }


def range_check(signals: list[SignalRecord], ranges: dict[str, tuple[float, float]]) -> dict:
    """Check that signal values are within expected ranges."""
    out_of_range = []
    for signal in signals:
        if signal.signal_key in ranges:
            low, high = ranges[signal.signal_key]
            if not (low <= signal.signal_value <= high):
                out_of_range.append(f"{signal.signal_key}={signal.signal_value}")

    if out_of_range:
        return {
            "check_name": "range_check",
            "check_status": "warn",
            "expected_value": "within range",
            "actual_value": ", ".join(out_of_range),
            "message": f"Values out of expected range: {', '.join(out_of_range)}.",
        }
    return {
        "check_name": "range_check",
        "check_status": "pass",
        "expected_value": "within range",
        "actual_value": "all within range",
        "message": "All signal values are within expected ranges.",
    }


def schema_drift_check(raw: dict[str, Any], expected_keys: set[str], source_slug: str) -> dict:
    """Check for unexpected fields in the raw response."""
    actual_keys = set(_flatten_keys(raw))
    unexpected = actual_keys - expected_keys

    if unexpected:
        sample = list(unexpected)[:5]
        return {
            "check_name": "schema_drift",
            "check_status": "warn",
            "expected_value": "stable schema",
            "actual_value": f"new fields: {', '.join(sample)}",
            "message": f"Unexpected fields found in response: {', '.join(sample)}.",
        }
    return {
        "check_name": "schema_drift",
        "check_status": "pass",
        "expected_value": "stable schema",
        "actual_value": "no drift",
        "message": "Response schema matches expected structure.",
    }


def _flatten_keys(d: dict, prefix: str = "") -> list[str]:
    """Flatten dict keys into dot-notation paths."""
    keys = []
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        keys.append(full_key)
        if isinstance(v, dict):
            keys.extend(_flatten_keys(v, full_key))
    return keys


# ─── Per-source quality check configurations ─────────────

EXPECTED_COUNTS = {
    "open-meteo": 3,
    "frankfurter": 4,
    "coingecko": 3,
}

EXPECTED_RANGES = {
    "open-meteo": {
        "temperature_celsius": (-60.0, 60.0),
        "humidity_percent": (0.0, 100.0),
        "wind_speed_kmh": (0.0, 400.0),
    },
    "frankfurter": {
        "EUR_USD": (0.5, 2.0),
        "EUR_GBP": (0.3, 1.5),
        "EUR_BRL": (2.0, 15.0),
        "EUR_JPY": (80.0, 250.0),
    },
    "coingecko": {
        "bitcoin_usd": (1000.0, 500000.0),
        "ethereum_usd": (100.0, 50000.0),
        "solana_usd": (1.0, 5000.0),
    },
}


def run_quality_checks(source_slug: str, signals: list[SignalRecord], raw: dict[str, Any]) -> list[dict]:
    """Run all quality checks for a given source."""
    checks = []

    # Null check
    checks.append(null_check(signals, source_slug))

    # Volume check
    expected = EXPECTED_COUNTS.get(source_slug, len(signals))
    checks.append(volume_check(signals, expected, source_slug))

    # Range check
    ranges = EXPECTED_RANGES.get(source_slug, {})
    if ranges:
        checks.append(range_check(signals, ranges))

    return checks
