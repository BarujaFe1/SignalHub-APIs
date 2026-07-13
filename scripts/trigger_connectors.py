"""Trigger connectors manually to generate fresh data."""

import asyncio

from scripts._paths import ensure_repo_paths

ensure_repo_paths()

from app.db.engine import AsyncSessionLocal
from packages.ingestion.jobs.runner import execute_connector


async def trigger_connector(slug: str):
    print(f"Triggering connector: {slug}")
    async with AsyncSessionLocal() as session:
        try:
            run_id = await execute_connector(slug, session)
            print(f"[SUCCESS] Run completed: {run_id}")
        except Exception as e:
            print(f"[ERROR] {e}")


async def main():
    print("Triggering all 3 connectors...\n")
    await trigger_connector("open-meteo")
    await trigger_connector("frankfurter")
    await trigger_connector("coingecko")
    print("\nAll connectors triggered!")


if __name__ == "__main__":
    asyncio.run(main())
