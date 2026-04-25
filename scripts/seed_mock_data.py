"""Seed the database with mock ingestion data, bypassing network calls."""
import sys
import os

sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

import asyncio
import uuid
import hashlib
import json
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.db.engine import AsyncSessionLocal
from app.db.models import (
    Source, Run, RawPayload, NormalizedSignal,
    FreshnessStatus, QualityCheck, EventLog
)

def get_idempotency_key(slug: str) -> str:
    now = datetime.now(timezone.utc)
    return f"{slug}:{now.strftime('%Y-%m-%d')}:{now.strftime('%H')}"

async def inject_mock_data(slug: str, session, raw_data: dict, signals_data: list, quality_data: list):
    # 1. Get source
    result = await session.execute(select(Source).where(Source.slug == slug))
    source = result.scalar_one_or_none()
    if not source:
        print(f"Source {slug} not found.")
        return

    key = get_idempotency_key(slug)
    
    # Check idempotency
    result = await session.execute(
        select(Run.id).where(Run.idempotency_key == key, Run.status == "success").limit(1)
    )
    if result.scalar_one_or_none():
        print(f"Run for {slug} already exists.")
        return

    print(f"Injecting mock data for {slug}...")

    # 2. Run
    run = Run(
        source_id=source.id,
        status="success",
        started_at=datetime.now(timezone.utc) - timedelta(seconds=2),
        finished_at=datetime.now(timezone.utc),
        duration_ms=450,
        records_fetched=len(signals_data),
        records_stored=len(signals_data),
        idempotency_key=key,
    )
    session.add(run)
    await session.flush()

    # 3. Raw Payload
    payload_str = json.dumps(raw_data, sort_keys=True, default=str)
    payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
    
    raw_payload = RawPayload(
        run_id=run.id,
        source_id=source.id,
        payload=raw_data,
        fetched_at=run.started_at,
        payload_hash=payload_hash,
    )
    session.add(raw_payload)

    # 4. Signals
    for s in signals_data:
        session.add(NormalizedSignal(
            run_id=run.id,
            source_id=source.id,
            signal_type=s["signal_type"],
            signal_key=s["signal_key"],
            signal_value=s["signal_value"],
            signal_unit=s["signal_unit"],
            observed_at=run.finished_at,
            metadata_=s.get("metadata", {}),
        ))

    # 5. Quality Checks
    for q in quality_data:
        session.add(QualityCheck(
            run_id=run.id,
            source_id=source.id,
            check_name=q["check_name"],
            check_status=q["check_status"],
            expected_value=q["expected_value"],
            actual_value=q["actual_value"],
            message=q["message"],
        ))

    # 6. Event Logs
    session.add(EventLog(
        source_id=source.id,
        run_id=run.id,
        event_type="job_completed",
        severity="info",
        message=f"Completed ingestion for {source.name} (MOCK)",
        details={"records_fetched": len(signals_data), "records_stored": len(signals_data)},
    ))

    # 7. Freshness
    result = await session.execute(select(FreshnessStatus).where(FreshnessStatus.source_id == source.id))
    freshness = result.scalar_one_or_none()
    if not freshness:
        freshness = FreshnessStatus(source_id=source.id)
        session.add(freshness)
    
    freshness.last_attempt_at = run.finished_at
    freshness.last_success_at = run.finished_at
    freshness.last_run_id = run.id
    freshness.is_stale = False
    freshness.staleness_minutes = 0

async def run_all():
    async with AsyncSessionLocal() as session:
        # Open-Meteo
        await inject_mock_data(
            "open-meteo", session,
            raw_data={"current": {"temperature_2m": 15.5, "relative_humidity_2m": 60, "wind_speed_10m": 12.0}},
            signals_data=[
                {"signal_type": "weather", "signal_key": "temperature_celsius", "signal_value": 15.5, "signal_unit": "C", "metadata": {"location": "Berlin"}},
                {"signal_type": "weather", "signal_key": "humidity_percent", "signal_value": 60.0, "signal_unit": "%", "metadata": {"location": "Berlin"}},
            ],
            quality_data=[
                {"check_name": "Valid Temperature Range", "check_status": "pass", "expected_value": "-50 to 50", "actual_value": "15.5", "message": "Temperature within realistic bounds"}
            ]
        )

        # Frankfurter
        await inject_mock_data(
            "frankfurter", session,
            raw_data={"amount": 1.0, "base": "EUR", "date": "2026-04-23", "rates": {"USD": 1.08, "GBP": 0.85, "BRL": 5.40}},
            signals_data=[
                {"signal_type": "exchange_rate", "signal_key": "EUR_USD", "signal_value": 1.08, "signal_unit": "rate", "metadata": {}},
                {"signal_type": "exchange_rate", "signal_key": "EUR_BRL", "signal_value": 5.40, "signal_unit": "rate", "metadata": {}},
            ],
            quality_data=[
                {"check_name": "Rates Not Empty", "check_status": "pass", "expected_value": "> 0 rates", "actual_value": "3 rates", "message": "Rates found"}
            ]
        )

        # CoinGecko
        await inject_mock_data(
            "coingecko", session,
            raw_data={"bitcoin": {"usd": 65000, "usd_24h_change": 2.5}, "ethereum": {"usd": 3500, "usd_24h_change": 1.2}},
            signals_data=[
                {"signal_type": "crypto_price", "signal_key": "bitcoin_usd", "signal_value": 65000.0, "signal_unit": "USD", "metadata": {"change_24h": 2.5}},
                {"signal_type": "crypto_price", "signal_key": "ethereum_usd", "signal_value": 3500.0, "signal_unit": "USD", "metadata": {"change_24h": 1.2}},
            ],
            quality_data=[
                {"check_name": "Prices Positive", "check_status": "pass", "expected_value": "> 0", "actual_value": "65000, 3500", "message": "Prices are positive"}
            ]
        )

        await session.commit()
        print("All mock data injected successfully!")

if __name__ == "__main__":
    asyncio.run(run_all())
