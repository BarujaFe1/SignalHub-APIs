import asyncio
import logging
import sys
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import get_settings
from packages.ingestion.jobs.runner import execute_connector

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-24s │ %(levelname)-7s │ %(message)s",
    stream=sys.stdout,
)

async def run_all():
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    sources = ["open-meteo", "frankfurter", "coingecko"]
    
    print(f"🚀 Starting manual ingestion for {len(sources)} sources...\n")
    
    async with AsyncSessionLocal() as session:
        for slug in sources:
            print(f"📡 Processing {slug}...")
            try:
                run_id = await execute_connector(slug, session)
                print(f"✅ Success! Run ID: {run_id}\n")
            except Exception as e:
                print(f"❌ Failed {slug}: {e}\n")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_all())
