"""API routers — all endpoints for SignalHub APIs."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.db.engine import get_db
from app.db.models import Run
from app.services.queries import (
    get_all_sources, get_source_by_slug, count_signals_by_source,
    count_runs_by_source, get_last_run_status,
    get_runs, get_run_by_id,
    get_signals,
    get_all_freshness,
    get_quality_checks, get_quality_summary, compute_freshness_age,
    get_metrics_summary,
)
from app.schemas.responses import (
    HealthOut, SourceOut, SourceDetailOut, FreshnessOut,
    RunOut, PaginatedRuns,
    SignalOut, PaginatedSignals,
    QualityCheckOut, QualityResponse, QualitySummary,
    MetricsSummaryOut, TriggerOut,
)


def _freshness_out(source, freshness) -> FreshnessOut | None:
    if not freshness:
        return None
    is_stale, minutes = compute_freshness_age(
        freshness.last_success_at,
        source.schedule_interval_minutes,
    )
    return FreshnessOut(
        source_slug=source.slug,
        source_name=source.name,
        last_success_at=freshness.last_success_at,
        last_attempt_at=freshness.last_attempt_at,
        is_stale=is_stale,
        staleness_minutes=minutes,
    )


# ─── Health ───────────────────────────────────────────────

health_router = APIRouter(tags=["health"])


@health_router.get("/health", response_model=HealthOut)
async def health_check(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    sched = getattr(request.app.state, "scheduler", None)
    scheduler_status = "running" if sched is not None and getattr(sched, "running", False) else "stopped"

    return HealthOut(
        status="healthy" if db_status == "connected" else "degraded",
        database=db_status,
        scheduler=scheduler_status,
        timestamp=datetime.now(timezone.utc),
    )


# ─── Sources ─────────────────────────────────────────────

sources_router = APIRouter(prefix="/api/v1", tags=["sources"])


@sources_router.get("/sources", response_model=list[SourceOut])
async def list_sources(db: AsyncSession = Depends(get_db)):
    sources = await get_all_sources(db)
    result = []
    for s in sources:
        total_signals = await count_signals_by_source(db, s.id)
        total_runs = await count_runs_by_source(db, s.id)
        last_status = await get_last_run_status(db, s.id)

        result.append(SourceOut(
            id=s.id,
            slug=s.slug,
            name=s.name,
            description=s.description,
            api_base_url=s.api_base_url,
            schedule_interval_minutes=s.schedule_interval_minutes,
            is_active=s.is_active,
            created_at=s.created_at,
            updated_at=s.updated_at,
            freshness=_freshness_out(s, s.freshness),
            last_run_status=last_status,
            total_signals=total_signals,
            total_runs=total_runs,
        ))
    return result


@sources_router.get("/sources/{slug}", response_model=SourceDetailOut)
async def get_source_detail(slug: str, db: AsyncSession = Depends(get_db)):
    source = await get_source_by_slug(db, slug)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    total_signals = await count_signals_by_source(db, source.id)
    total_runs_count = await count_runs_by_source(db, source.id)
    last_status = await get_last_run_status(db, source.id)

    source_out = SourceOut(
        id=source.id, slug=source.slug, name=source.name,
        description=source.description, api_base_url=source.api_base_url,
        schedule_interval_minutes=source.schedule_interval_minutes,
        is_active=source.is_active, created_at=source.created_at,
        updated_at=source.updated_at, freshness=_freshness_out(source, source.freshness),
        last_run_status=last_status, total_signals=total_signals,
        total_runs=total_runs_count,
    )

    recent_runs, _ = await get_runs(db, source_slug=slug, limit=20)
    runs_out = [_run_to_out(r) for r in recent_runs]

    recent_signals, _ = await get_signals(db, source_slug=slug, limit=20)
    signals_out = [_signal_to_out(s, source.slug) for s in recent_signals]

    checks = await get_quality_checks(db, source_slug=slug, limit=20)
    checks_out = [_check_to_out(c) for c in checks]

    qs = await get_quality_summary(db, source_slug=slug)

    return SourceDetailOut(
        source=source_out,
        recent_runs=runs_out,
        recent_signals=signals_out,
        recent_checks=checks_out,
        quality_summary=QualitySummary(**qs),
    )


# ─── Runs ─────────────────────────────────────────────────

runs_router = APIRouter(prefix="/api/v1", tags=["runs"])


@runs_router.get("/runs", response_model=PaginatedRuns)
async def list_runs(
    source: str | None = None,
    status: str | None = Query(default=None, pattern="^(success|failed|running|partial)$"),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    runs, total = await get_runs(db, source_slug=source, status=status, limit=limit, offset=offset)
    return PaginatedRuns(
        items=[_run_to_out(r) for r in runs],
        total=total, limit=limit, offset=offset,
    )


@runs_router.get("/runs/{run_id}", response_model=RunOut)
async def get_run(run_id: UUID, db: AsyncSession = Depends(get_db)):
    run = await get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return _run_to_out(run)


# ─── Freshness ───────────────────────────────────────────

freshness_router = APIRouter(prefix="/api/v1", tags=["freshness"])


@freshness_router.get("/freshness", response_model=list[FreshnessOut])
async def list_freshness(db: AsyncSession = Depends(get_db)):
    items = await get_all_freshness(db)
    result = []
    for f in items:
        src = f.source if hasattr(f, "source") and f.source else None
        if not src:
            continue
        out = _freshness_out(src, f)
        if out:
            result.append(out)
    return result


# ─── Quality ──────────────────────────────────────────────

quality_router = APIRouter(prefix="/api/v1", tags=["quality"])


@quality_router.get("/quality", response_model=QualityResponse)
async def list_quality(
    source: str | None = None,
    status: str | None = Query(default=None, pattern="^(pass|warn|fail)$"),
    limit: int = Query(default=50, le=100),
    db: AsyncSession = Depends(get_db),
):
    checks = await get_quality_checks(db, source_slug=source, status=status, limit=limit)
    summary = await get_quality_summary(db, source_slug=source)
    return QualityResponse(
        items=[_check_to_out(c) for c in checks],
        summary=QualitySummary(**summary),
    )


# ─── Signals ─────────────────────────────────────────────

signals_router = APIRouter(prefix="/api/v1", tags=["signals"])


@signals_router.get("/signals", response_model=PaginatedSignals)
async def list_signals(
    source: str | None = None,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    signals, total = await get_signals(db, source_slug=source, limit=limit, offset=offset)
    return PaginatedSignals(
        items=[_signal_to_out(s) for s in signals],
        total=total, limit=limit, offset=offset,
    )


# ─── Metrics ─────────────────────────────────────────────

metrics_router = APIRouter(prefix="/api/v1", tags=["metrics"])


@metrics_router.get("/metrics/summary", response_model=MetricsSummaryOut)
async def metrics_summary(db: AsyncSession = Depends(get_db)):
    data = await get_metrics_summary(db)
    return MetricsSummaryOut(**data)


# ─── Trigger ─────────────────────────────────────────────

trigger_router = APIRouter(prefix="/api/v1", tags=["triggers"])


def _require_trigger_auth(x_api_key: str | None) -> None:
    settings = get_settings()
    expected = (settings.trigger_api_key or "").strip()
    if not expected:
        return
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


@trigger_router.post("/runs/trigger/{slug}", response_model=TriggerOut, status_code=202)
async def trigger_run(
    slug: str,
    db: AsyncSession = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    _require_trigger_auth(x_api_key)

    source = await get_source_by_slug(db, slug)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    from packages.ingestion.jobs.runner import execute_connector

    run_id = await execute_connector(slug, db)

    result = await db.execute(
        select(Run).options(selectinload(Run.source)).where(Run.id == run_id)
    )
    run = result.scalar_one_or_none()
    status = run.status if run else "unknown"
    message = (
        "Run completed successfully"
        if status == "success"
        else f"Run finished with status '{status}'"
    )
    if run and run.error_message:
        message = run.error_message

    return TriggerOut(
        run_id=run_id,
        source_slug=slug,
        status=status,
        message=message,
    )


# ─── Helpers ──────────────────────────────────────────────

def _run_to_out(run) -> RunOut:
    source = run.source if hasattr(run, "source") and run.source else None
    return RunOut(
        id=run.id,
        source_id=run.source_id,
        source_slug=source.slug if source else "unknown",
        source_name=source.name if source else "Unknown",
        status=run.status,
        started_at=run.started_at,
        finished_at=run.finished_at,
        duration_ms=run.duration_ms,
        records_fetched=run.records_fetched,
        records_stored=run.records_stored,
        error_message=run.error_message,
        created_at=run.created_at,
    )


def _signal_to_out(signal, source_slug: str | None = None) -> SignalOut:
    slug = source_slug
    if not slug and hasattr(signal, "run") and signal.run and hasattr(signal.run, "source") and signal.run.source:
        slug = signal.run.source.slug
    return SignalOut(
        id=signal.id,
        source_slug=slug or "unknown",
        signal_type=signal.signal_type,
        signal_key=signal.signal_key,
        signal_value=float(signal.signal_value),
        signal_unit=signal.signal_unit,
        observed_at=signal.observed_at,
        metadata=signal.metadata_,
    )


def _check_to_out(check) -> QualityCheckOut:
    run = check.run if hasattr(check, "run") and check.run else None
    source = run.source if run and hasattr(run, "source") and run.source else None
    return QualityCheckOut(
        id=check.id,
        run_id=check.run_id,
        source_slug=source.slug if source else "unknown",
        source_name=source.name if source else "Unknown",
        check_name=check.check_name,
        check_status=check.check_status,
        expected_value=check.expected_value,
        actual_value=check.actual_value,
        message=check.message,
        checked_at=check.checked_at,
    )
