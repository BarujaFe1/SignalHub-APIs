"""Pydantic schemas for API responses."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Any


# ─── Source Schemas ────────────────────────────────────────

class FreshnessOut(BaseModel):
    source_slug: str
    source_name: str
    last_success_at: datetime | None
    last_attempt_at: datetime | None
    is_stale: bool
    staleness_minutes: int


class SourceOut(BaseModel):
    id: UUID
    slug: str
    name: str
    description: str
    api_base_url: str
    schedule_interval_minutes: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    freshness: FreshnessOut | None = None
    last_run_status: str | None = None
    total_signals: int = 0
    total_runs: int = 0

    model_config = {"from_attributes": True}


# ─── Run Schemas ──────────────────────────────────────────

class RunOut(BaseModel):
    id: UUID
    source_id: UUID
    source_slug: str
    source_name: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    duration_ms: int | None
    records_fetched: int
    records_stored: int
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedRuns(BaseModel):
    items: list[RunOut]
    total: int
    limit: int
    offset: int


# ─── Signal Schemas ───────────────────────────────────────

class SignalOut(BaseModel):
    id: UUID
    source_slug: str
    signal_type: str
    signal_key: str
    signal_value: float
    signal_unit: str
    observed_at: datetime
    metadata: dict[str, Any] | None = Field(None, validation_alias="metadata_")

    model_config = {"from_attributes": True}


class PaginatedSignals(BaseModel):
    items: list[SignalOut]
    total: int
    limit: int
    offset: int


# ─── Quality Schemas ──────────────────────────────────────

class QualityCheckOut(BaseModel):
    id: UUID
    run_id: UUID
    source_slug: str
    source_name: str
    check_name: str
    check_status: str
    expected_value: str
    actual_value: str
    message: str
    checked_at: datetime

    model_config = {"from_attributes": True}


class QualitySummary(BaseModel):
    total: int
    passed: int
    warnings: int
    failures: int


class QualityResponse(BaseModel):
    items: list[QualityCheckOut]
    summary: QualitySummary


# ─── Metrics Schema ──────────────────────────────────────

class MetricsSummaryOut(BaseModel):
    total_sources: int
    active_sources: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    total_signals: int
    total_quality_checks: int
    quality_pass_rate: float
    sources_stale: int
    last_activity_at: datetime | None


# ─── Source Detail ────────────────────────────────────────

class SourceDetailOut(BaseModel):
    source: SourceOut
    recent_runs: list[RunOut]
    recent_signals: list[SignalOut]
    recent_checks: list[QualityCheckOut]
    quality_summary: QualitySummary


# ─── Health ───────────────────────────────────────────────

class HealthOut(BaseModel):
    status: str
    database: str
    scheduler: str
    timestamp: datetime


# ─── Trigger ──────────────────────────────────────────────

class TriggerOut(BaseModel):
    run_id: UUID
    source_slug: str
    status: str
    message: str
