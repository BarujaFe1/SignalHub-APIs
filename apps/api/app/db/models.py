"""SignalHub APIs — Database Models.

All 7 tables for V1:
- sources
- runs
- raw_payloads
- normalized_signals
- freshness_status
- quality_checks
- event_logs
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String, Text, Integer, Boolean, Numeric, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, JSON

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


# ─── Sources ──────────────────────────────────────────────

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    api_base_url: Mapped[str] = mapped_column(String(255), default="")
    schedule_interval_minutes: Mapped[int] = mapped_column(Integer, default=30)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    runs: Mapped[list["Run"]] = relationship(back_populates="source", lazy="selectin")
    freshness: Mapped["FreshnessStatus | None"] = relationship(back_populates="source", uselist=False, lazy="selectin")


# ─── Runs ─────────────────────────────────────────────────

class Run(Base):
    __tablename__ = "runs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    source_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sources.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running")  # running, success, failed, partial
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    records_fetched: Mapped[int] = mapped_column(Integer, default=0)
    records_stored: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    source: Mapped["Source"] = relationship(back_populates="runs", lazy="selectin")
    raw_payloads: Mapped[list["RawPayload"]] = relationship(back_populates="run", lazy="noload")
    signals: Mapped[list["NormalizedSignal"]] = relationship(back_populates="run", lazy="noload")
    quality_checks: Mapped[list["QualityCheck"]] = relationship(back_populates="run", lazy="noload")

    __table_args__ = (
        Index("ix_runs_source_started", "source_id", "started_at"),
    )


# ─── Raw Payloads ─────────────────────────────────────────

class RawPayload(Base):
    __tablename__ = "raw_payloads"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("runs.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sources.id"), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    payload_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    run: Mapped["Run"] = relationship(back_populates="raw_payloads")

    __table_args__ = (
        Index("ix_raw_payloads_source_fetched", "source_id", "fetched_at"),
    )


# ─── Normalized Signals ───────────────────────────────────

class NormalizedSignal(Base):
    __tablename__ = "normalized_signals"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("runs.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sources.id"), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)  # weather, exchange_rate, crypto_price
    signal_key: Mapped[str] = mapped_column(String(100), nullable=False)
    signal_value: Mapped[float] = mapped_column(Numeric(20, 6), nullable=False)
    signal_unit: Mapped[str] = mapped_column(String(30), default="")
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    run: Mapped["Run"] = relationship(back_populates="signals")

    __table_args__ = (
        Index("ix_signals_source_type", "source_id", "signal_type"),
        Index("ix_signals_observed", "observed_at"),
    )


# ─── Freshness Status ─────────────────────────────────────

class FreshnessStatus(Base):
    __tablename__ = "freshness_status"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    source_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sources.id"), unique=True, nullable=False)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_run_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("runs.id"), nullable=True)
    is_stale: Mapped[bool] = mapped_column(Boolean, default=False)
    staleness_minutes: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    source: Mapped["Source"] = relationship(back_populates="freshness", lazy="selectin")


# ─── Quality Checks ───────────────────────────────────────

class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    run_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("runs.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sources.id"), nullable=False)
    check_name: Mapped[str] = mapped_column(String(100), nullable=False)
    check_status: Mapped[str] = mapped_column(String(20), nullable=False)  # pass, warn, fail
    expected_value: Mapped[str] = mapped_column(String(255), default="")
    actual_value: Mapped[str] = mapped_column(String(255), default="")
    message: Mapped[str] = mapped_column(Text, default="")
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    run: Mapped["Run"] = relationship(back_populates="quality_checks")

    __table_args__ = (
        Index("ix_quality_source_status", "source_id", "check_status"),
    )


# ─── Event Logs ───────────────────────────────────────────

class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    source_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("sources.id"), nullable=True)
    run_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("runs.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="info")  # info, warning, error
    message: Mapped[str] = mapped_column(Text, default="")
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    __table_args__ = (
        Index("ix_events_type_created", "event_type", "created_at"),
    )
