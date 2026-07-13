"""API integration tests using SQLite in-memory / temp file."""

from __future__ import annotations

import os
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Force SQLite before app imports settings
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["DATABASE_URL_SYNC"] = "sqlite:///:memory:"
os.environ["TRIGGER_API_KEY"] = "test-secret"
os.environ["API_DEBUG"] = "false"

from app.config import get_settings
from app.db.base import Base
from app.db.engine import get_db
from app.db.models import FreshnessStatus, Source
from app.main import app
from app.services.queries import compute_freshness_age


get_settings.cache_clear()


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        source = Source(
            slug="open-meteo",
            name="Open-Meteo Weather",
            description="Test source",
            api_base_url="https://api.open-meteo.com",
            schedule_interval_minutes=30,
            is_active=True,
        )
        session.add(source)
        await session.flush()
        session.add(FreshnessStatus(source_id=source.id))
        await session.commit()

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    res = await client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["database"] == "connected"
    assert "status" in body


@pytest.mark.asyncio
async def test_list_sources(client: AsyncClient):
    res = await client.get("/api/v1/sources")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["slug"] == "open-meteo"


@pytest.mark.asyncio
async def test_source_not_found(client: AsyncClient):
    res = await client.get("/api/v1/sources/does-not-exist")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_trigger_requires_api_key(client: AsyncClient):
    res = await client.post("/api/v1/runs/trigger/open-meteo")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_metrics_summary(client: AsyncClient):
    res = await client.get("/api/v1/metrics/summary")
    assert res.status_code == 200
    body = res.json()
    assert body["total_sources"] == 1
    assert body["active_sources"] == 1


def test_compute_freshness_age_fresh():
    now = datetime.now(timezone.utc)
    is_stale, minutes = compute_freshness_age(now, schedule_interval_minutes=30)
    assert is_stale is False
    assert minutes == 0


def test_compute_freshness_age_stale():
    old = datetime(2020, 1, 1, tzinfo=timezone.utc)
    is_stale, minutes = compute_freshness_age(old, schedule_interval_minutes=30)
    assert is_stale is True
    assert minutes > 60
