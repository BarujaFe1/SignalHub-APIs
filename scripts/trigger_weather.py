import asyncio

from scripts._paths import ensure_repo_paths

ensure_repo_paths()

from app.db.engine import AsyncSessionLocal
from packages.ingestion.jobs.runner import execute_connector


async def run_weather():
    async with AsyncSessionLocal() as session:
        print("Triggering Open-Meteo...")
        await execute_connector("open-meteo", session)
        print("Done!")


if __name__ == "__main__":
    asyncio.run(run_weather())
