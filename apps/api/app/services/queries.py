"""Service layer for database queries."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    Source, Run, NormalizedSignal, FreshnessStatus,
    QualityCheck, EventLog
)


# ─── Source Service ───────────────────────────────────────

async def get_all_sources(db: AsyncSession) -> list[Source]:
    result = await db.execute(select(Source).order_by(Source.name))
    return list(result.scalars().all())


async def get_source_by_slug(db: AsyncSession, slug: str) -> Source | None:
    result = await db.execute(select(Source).where(Source.slug == slug))
    return result.scalar_one_or_none()


async def count_signals_by_source(db: AsyncSession, source_id: UUID) -> int:
    result = await db.execute(
        select(func.count()).select_from(NormalizedSignal).where(NormalizedSignal.source_id == source_id)
    )
    return result.scalar() or 0


async def count_runs_by_source(db: AsyncSession, source_id: UUID) -> int:
    result = await db.execute(
        select(func.count()).select_from(Run).where(Run.source_id == source_id)
    )
    return result.scalar() or 0


async def get_last_run_status(db: AsyncSession, source_id: UUID) -> str | None:
    result = await db.execute(
        select(Run.status)
        .where(Run.source_id == source_id)
        .order_by(desc(Run.started_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


# ─── Run Service ──────────────────────────────────────────

async def get_runs(
    db: AsyncSession,
    source_slug: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[Run], int]:
    query = select(Run).join(Source)

    if source_slug:
        query = query.where(Source.slug == source_slug)
    if status:
        query = query.where(Run.status == status)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    query = query.order_by(desc(Run.started_at)).limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def get_run_by_id(db: AsyncSession, run_id: UUID) -> Run | None:
    result = await db.execute(select(Run).where(Run.id == run_id))
    return result.scalar_one_or_none()


# ─── Signal Service ───────────────────────────────────────

async def get_signals(
    db: AsyncSession,
    source_slug: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[NormalizedSignal], int]:
    query = select(NormalizedSignal).join(Source, NormalizedSignal.source_id == Source.id)

    if source_slug:
        query = query.where(Source.slug == source_slug)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    query = query.order_by(desc(NormalizedSignal.observed_at)).limit(limit).offset(offset)
    query = query.options(selectinload(NormalizedSignal.run).selectinload(Run.source))
    result = await db.execute(query)
    return list(result.scalars().all()), total


# ─── Freshness Service ───────────────────────────────────

async def get_all_freshness(db: AsyncSession) -> list[FreshnessStatus]:
    result = await db.execute(select(FreshnessStatus))
    return list(result.scalars().all())


# ─── Quality Service ─────────────────────────────────────

async def get_quality_checks(
    db: AsyncSession,
    source_slug: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[QualityCheck]:
    query = select(QualityCheck).join(Run).join(Source)

    if source_slug:
        query = query.where(Source.slug == source_slug)
    if status:
        query = query.where(QualityCheck.check_status == status)

    query = query.order_by(desc(QualityCheck.checked_at)).limit(limit)
    query = query.options(selectinload(QualityCheck.run).selectinload(Run.source))
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_quality_summary(db: AsyncSession) -> dict:
    total = (await db.execute(select(func.count()).select_from(QualityCheck))).scalar() or 0
    passed = (await db.execute(
        select(func.count()).select_from(QualityCheck).where(QualityCheck.check_status == "pass")
    )).scalar() or 0
    warnings = (await db.execute(
        select(func.count()).select_from(QualityCheck).where(QualityCheck.check_status == "warn")
    )).scalar() or 0
    failures = (await db.execute(
        select(func.count()).select_from(QualityCheck).where(QualityCheck.check_status == "fail")
    )).scalar() or 0
    return {"total": total, "passed": passed, "warnings": warnings, "failures": failures}


# ─── Metrics Service ─────────────────────────────────────

async def get_metrics_summary(db: AsyncSession) -> dict:
    total_sources = (await db.execute(select(func.count()).select_from(Source))).scalar() or 0
    active_sources = (await db.execute(
        select(func.count()).select_from(Source).where(Source.is_active == True)
    )).scalar() or 0
    total_runs = (await db.execute(select(func.count()).select_from(Run))).scalar() or 0
    successful_runs = (await db.execute(
        select(func.count()).select_from(Run).where(Run.status == "success")
    )).scalar() or 0
    failed_runs = (await db.execute(
        select(func.count()).select_from(Run).where(Run.status == "failed")
    )).scalar() or 0
    total_signals = (await db.execute(select(func.count()).select_from(NormalizedSignal))).scalar() or 0

    quality_summary = await get_quality_summary(db)
    total_qc = quality_summary["total"]
    pass_rate = quality_summary["passed"] / total_qc if total_qc > 0 else 1.0

    stale = (await db.execute(
        select(func.count()).select_from(FreshnessStatus).where(FreshnessStatus.is_stale == True)
    )).scalar() or 0

    last_run = await db.execute(select(Run.started_at).order_by(desc(Run.started_at)).limit(1))
    last_activity = last_run.scalar_one_or_none()

    return {
        "total_sources": total_sources,
        "active_sources": active_sources,
        "total_runs": total_runs,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "total_signals": total_signals,
        "total_quality_checks": total_qc,
        "quality_pass_rate": round(pass_rate, 3),
        "sources_stale": stale,
        "last_activity_at": last_activity,
    }
