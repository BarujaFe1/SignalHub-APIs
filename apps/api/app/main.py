"""SignalHub APIs — FastAPI Application.

Main entry point with:
- CORS middleware
- Router registration
- APScheduler integration via lifespan
- Alembic migration support
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import get_settings
from app.db.engine import AsyncSessionLocal
from app.routers.endpoints import (
    health_router, sources_router, runs_router,
    freshness_router, quality_router, signals_router,
    metrics_router, trigger_router,
)

# ─── Logging ──────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-24s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("signalhub")

# ─── Scheduler ────────────────────────────────────────────

scheduler = AsyncIOScheduler()


async def scheduled_job(source_slug: str):
    """Execute a connector job within its own DB session."""
    from packages.ingestion.jobs.runner import execute_connector, check_idempotency, get_idempotency_key

    logger.info(f"⏱ Scheduled job triggered for: {source_slug}")

    async with AsyncSessionLocal() as session:
        # Check idempotency
        key = get_idempotency_key(source_slug)
        if await check_idempotency(session, key):
            logger.info(f"⏭ Skipping {source_slug} — already executed for this window ({key})")
            return

        try:
            await execute_connector(source_slug, session)
        except Exception as e:
            logger.error(f"Scheduled job failed for {source_slug}: {e}")


# ─── Lifespan ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle manager."""
    logger.info("🚀 SignalHub APIs starting up...")

    async with AsyncSessionLocal() as session:
        from app.services.queries import get_all_sources
        
        sources = await get_all_sources(session)
        
        for source in sources:
            if not source.is_active:
                continue
                
            scheduler.add_job(
                scheduled_job,
                "interval",
                minutes=source.schedule_interval_minutes,
                args=[source.slug],
                id=f"job_{source.slug}",
                name=f"Ingest {source.slug}",
                replace_existing=True,
            )
            logger.info(f"📋 Registered job: {source.slug} (every {source.schedule_interval_minutes}m)")

    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("✅ Scheduler started")

    yield

    scheduler.shutdown()
    logger.info("🛑 SignalHub APIs shutting down")


# ─── App ──────────────────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title="SignalHub APIs",
    description=(
        "Observability layer for public-API ingestion. "
        "Normalizes heterogeneous upstream payloads into signals, "
        "tracks runs/freshness/quality, and exposes an ops-friendly REST API. "
        "Interactive docs: `/docs` (Swagger) and `/redoc`."
    ),
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Liveness and dependency checks"},
        {"name": "sources", "description": "Registered connectors and detail views"},
        {"name": "runs", "description": "Ingestion execution history"},
        {"name": "freshness", "description": "Staleness indicators per source"},
        {"name": "quality", "description": "Per-run quality gate results"},
        {"name": "signals", "description": "Normalized numeric signals"},
        {"name": "metrics", "description": "Aggregate operational KPIs"},
        {"name": "triggers", "description": "Manual ingestion triggers (auth + rate limit)"},
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(sources_router)
app.include_router(runs_router)
app.include_router(freshness_router)
app.include_router(quality_router)
app.include_router(signals_router)
app.include_router(metrics_router)
app.include_router(trigger_router)
