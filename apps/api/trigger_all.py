import sys
import os
sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

import asyncio
from app.db.engine import AsyncSessionLocal
from packages.ingestion.jobs.runner import execute_connector

async def run_all():
    async with AsyncSessionLocal() as session:
        print("Triggering Open-Meteo...")
        await execute_connector("open-meteo", session)
        print("Triggering Frankfurter...")
        await execute_connector("frankfurter", session)
        print("Triggering CoinGecko...")
        await execute_connector("coingecko", session)
        await session.commit()
        print("All done!")

if __name__ == "__main__":
    asyncio.run(run_all())
