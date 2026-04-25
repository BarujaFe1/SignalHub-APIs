"""Seed the database with initial source definitions."""

import asyncio
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
    async with AsyncSessionLocal() as session:
        for source_data in SOURCES:
            # Check if source already exists
            result = await session.execute(
                select(Source).where(Source.slug == source_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  ⏭ Source '{source_data['slug']}' already exists")
                continue

            source = Source(**source_data)
            session.add(source)
            await session.flush()

            # Create initial freshness record
            session.add(FreshnessStatus(source_id=source.id))

            print(f"  ✓ Created source: {source_data['name']}")

        await session.commit()
        print("\n✅ Seed complete")


if __name__ == "__main__":
    print("🌱 Seeding SignalHub database...\n")
    asyncio.run(seed())
