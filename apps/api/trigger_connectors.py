"""Trigger a connector manually to generate fresh data."""
import sys
sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

import asyncio
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
