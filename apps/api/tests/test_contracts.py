"""Contract tests — OpenAPI surface and rate limiter behavior."""

from __future__ import annotations

import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["DATABASE_URL_SYNC"] = "sqlite:///:memory:"
os.environ["TRIGGER_API_KEY"] = "test-secret"
os.environ["TRIGGER_RATE_LIMIT_PER_MINUTE"] = "2"
os.environ["API_DEBUG"] = "false"

from app.config import get_settings
from app.db.base import Base
from app.db.engine import get_db
from app.db.models import FreshnessStatus, Source
from app.main import app
from app.services.rate_limit import SlidingWindowRateLimiter

get_settings.cache_clear()

REQUIRED_PATHS = {
    "/health",
    "/api/v1/sources",
    "/api/v1/sources/{slug}",
    "/api/v1/runs",
    "/api/v1/runs/{run_id}",
    "/api/v1/freshness",
    "/api/v1/quality",
    "/api/v1/signals",
    "/api/v1/metrics/summary",
    "/api/v1/runs/trigger/{slug}",
}


def test_openapi_contains_required_paths():
    schema = app.openapi()
    paths = set(schema.get("paths", {}).keys())
    missing = REQUIRED_PATHS - paths
    assert not missing, f"OpenAPI missing paths: {sorted(missing)}"
    assert schema["info"]["title"] == "SignalHub APIs"
    assert "triggers" in {t["name"] for t in schema.get("tags", [])}


def test_quality_summary_schema_uses_total_not_total_checks():
    schema = app.openapi()
    components = schema["components"]["schemas"]
    qs = components["QualitySummary"]["properties"]
    assert "total" in qs
    assert "total_checks" not in qs


def test_sliding_window_rate_limiter():
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("k")[0] is True
    assert limiter.allow("k")[0] is True
    allowed, retry = limiter.allow("k")
    assert allowed is False
    assert retry >= 1


@pytest_asyncio.fixture
async def client_rate_limited():
    # Reset limiter singleton between tests by clearing module state
    import app.routers.endpoints as endpoints

    endpoints._trigger_limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=60)
    get_settings.cache_clear()

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        source = Source(
            slug="open-meteo",
            name="Open-Meteo Weather",
            description="Test",
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
async def test_trigger_rate_limit_returns_429(client_rate_limited: AsyncClient, monkeypatch):
    """Third trigger in the window should be 429 (before hitting upstream)."""

    async def fake_execute(slug, db):
        from uuid import uuid4
        return uuid4()

    monkeypatch.setattr(
        "packages.ingestion.jobs.runner.execute_connector",
        fake_execute,
    )

    headers = {"X-API-Key": "test-secret"}
    r1 = await client_rate_limited.post("/api/v1/runs/trigger/open-meteo", headers=headers)
    r2 = await client_rate_limited.post("/api/v1/runs/trigger/open-meteo", headers=headers)
    r3 = await client_rate_limited.post("/api/v1/runs/trigger/open-meteo", headers=headers)

    assert r1.status_code == 202
    assert r2.status_code == 202
    assert r3.status_code == 429
    assert "Retry-After" in r3.headers
