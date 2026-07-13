"""Seed the database with initial source definitions."""

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "apps" / "api"
for path in (str(API), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from sqlalchemy import select
from app.db.engine import AsyncSessionLocal
from app.db.models import Source, FreshnessStatus


SOURCES = [
    {
        "slug": "open-meteo",
        "name": "Open-Meteo Weather",
        "description": "Current weather conditions for Berlin — temperature, humidity, and wind speed.",
        "api_base_url": "https://api.open-meteo.com",
        "schedule_interval_minutes": 30,
    },
    {
        "slug": "frankfurter",
        "name": "Frankfurter Exchange",
        "description": "EUR exchange rates — USD, GBP, BRL, JPY from the European Central Bank.",
        "api_base_url": "https://api.frankfurter.dev",
        "schedule_interval_minutes": 60,
    },
    {
        "slug": "coingecko",
        "name": "CoinGecko Crypto",
        "description": "Cryptocurrency prices — Bitcoin, Ethereum, Solana in USD with 24h changes.",
        "api_base_url": "https://api.coingecko.com",
        "schedule_interval_minutes": 15,
    },
]


async def seed():
    from app.db.base import Base
    from app.db.engine import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for source_data in SOURCES:
            result = await session.execute(
                select(Source).where(Source.slug == source_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  skip: source '{source_data['slug']}' already exists")
                continue

            source = Source(**source_data)
            session.add(source)
            await session.flush()
            session.add(FreshnessStatus(source_id=source.id))
            print(f"  ok: created source {source_data['name']}")

        await session.commit()
        print("\nSeed complete")


if __name__ == "__main__":
    print("Seeding SignalHub database...\n")
    asyncio.run(seed())
