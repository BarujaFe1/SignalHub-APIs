"""Job runner — executes a connector's full pipeline.

Pipeline: fetch → validate → normalize → persist raw → persist signals →
          update run → update freshness → run quality checks
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import (
    Source, Run, RawPayload, NormalizedSignal,
    FreshnessStatus, QualityCheck, EventLog,
)
from packages.ingestion.base import BaseConnector
from packages.ingestion.connectors.open_meteo import OpenMeteoConnector
from packages.ingestion.connectors.frankfurter import FrankfurterConnector
from packages.ingestion.connectors.coingecko import CoinGeckoConnector
from packages.ingestion.quality.checks import run_quality_checks

logger = logging.getLogger("signalhub.runner")

# Registry of connectors by slug
CONNECTORS: dict[str, type[BaseConnector]] = {
    "open-meteo": OpenMeteoConnector,
    "frankfurter": FrankfurterConnector,
    "coingecko": CoinGeckoConnector,
}


def get_idempotency_key(slug: str) -> str:
    """Generate idempotency key for current time window."""
    now = datetime.now(timezone.utc)
    return f"{slug}:{now.strftime('%Y-%m-%d')}:{now.strftime('%H')}"


async def check_idempotency(db: AsyncSession, key: str) -> bool:
    """Return True if a successful run already exists for this key."""
    result = await db.execute(
        select(Run.id).where(Run.idempotency_key == key, Run.status == "success").limit(1)
    )
    return result.scalar_one_or_none() is not None


async def execute_connector(slug: str, db: AsyncSession) -> UUID:
    """Execute a connector's full pipeline and return the run ID."""

    # Get source from DB
    result = await db.execute(select(Source).where(Source.slug == slug))
    source = result.scalar_one_or_none()
    if not source:
        raise ValueError(f"Source '{slug}' not found in database")

    # Create run record
    run = Run(
        source_id=source.id,
        status="running",
        started_at=datetime.now(timezone.utc),
        idempotency_key=get_idempotency_key(slug),
    )
    db.add(run)
    await db.flush()  # Get the ID

    # Log start event
    db.add(EventLog(
        source_id=source.id,
        run_id=run.id,
        event_type="job_started",
        severity="info",
        message=f"Started ingestion for {source.name}",
    ))

    try:
        # Create connector instance
        connector_cls = CONNECTORS.get(slug)
        if not connector_cls:
            raise ValueError(f"No connector registered for '{slug}'")

        connector = connector_cls()
        result = await connector.execute()

        # Store raw payload
        raw_payload = RawPayload(
            run_id=run.id,
            source_id=source.id,
            payload=result.raw_payload,
            fetched_at=result.fetched_at,
            payload_hash=result.payload_hash,
        )
        db.add(raw_payload)

        # Store normalized signals
        for signal in result.signals:
            db.add(NormalizedSignal(
                run_id=run.id,
                source_id=source.id,
                signal_type=signal.signal_type,
                signal_key=signal.signal_key,
                signal_value=signal.signal_value,
                signal_unit=signal.signal_unit,
                observed_at=signal.observed_at,
                metadata_=signal.metadata,
            ))

        # Update run status
        finished_at = datetime.now(timezone.utc)
        duration_ms = int((finished_at - run.started_at).total_seconds() * 1000)
        run.status = "success"
        run.finished_at = finished_at
        run.duration_ms = duration_ms
        run.records_fetched = result.records_fetched
        run.records_stored = result.records_normalized

        # Run quality checks
        checks = run_quality_checks(slug, result.signals, result.raw_payload)
        for check in checks:
            db.add(QualityCheck(
                run_id=run.id,
                source_id=source.id,
                check_name=check["check_name"],
                check_status=check["check_status"],
                expected_value=check["expected_value"],
                actual_value=check["actual_value"],
                message=check["message"],
            ))

        # Update freshness
        await _update_freshness(db, source, run)

        # Log success
        db.add(EventLog(
            source_id=source.id,
            run_id=run.id,
            event_type="job_completed",
            severity="info",
            message=f"Completed ingestion for {source.name}: {result.records_normalized} signals",
            details={"records_fetched": result.records_fetched, "records_stored": result.records_normalized},
        ))

        await db.commit()
        logger.info(f"✓ {source.name}: {result.records_normalized} signals stored in {duration_ms}ms")

    except Exception as e:
        # Update run as failed
        run.status = "failed"
        run.finished_at = datetime.now(timezone.utc)
        run.duration_ms = int((run.finished_at - run.started_at).total_seconds() * 1000)
        run.error_message = str(e)

        # Update freshness attempt
        await _update_freshness(db, source, run)

        # Log failure
        db.add(EventLog(
            source_id=source.id,
            run_id=run.id,
            event_type="job_failed",
            severity="error",
            message=f"Failed ingestion for {source.name}: {str(e)}",
        ))

        await db.commit()
        logger.error(f"✗ {source.name}: {str(e)}")

    return run.id


async def _update_freshness(db: AsyncSession, source: Source, run: Run):
    """Update the freshness status for a source."""
    result = await db.execute(
        select(FreshnessStatus).where(FreshnessStatus.source_id == source.id)
    )
    freshness = result.scalar_one_or_none()

    now = datetime.now(timezone.utc)

    if not freshness:
        freshness = FreshnessStatus(source_id=source.id)
        db.add(freshness)

    freshness.last_attempt_at = now
    freshness.last_run_id = run.id

    if run.status == "success":
        freshness.last_success_at = now
        freshness.is_stale = False
        freshness.staleness_minutes = 0
    else:
        # Compute staleness
        if freshness.last_success_at:
            delta = now - freshness.last_success_at
            freshness.staleness_minutes = int(delta.total_seconds() / 60)
            freshness.is_stale = freshness.staleness_minutes > source.schedule_interval_minutes * 2
        else:
            freshness.is_stale = True
            freshness.staleness_minutes = 0
