"""Test backend endpoints without starting the server."""
import sys
sys.path.insert(0, r"C:\dev\signalhub-apis\apps\api")
sys.path.insert(0, r"C:\dev\signalhub-apis")

import asyncio
from app.db.engine import AsyncSessionLocal
from sqlalchemy import select, func
from app.db.models import Source, Run, NormalizedSignal, QualityCheck, FreshnessStatus

async def test_queries():
    async with AsyncSessionLocal() as session:
        # Test 1: Get all sources
        result = await session.execute(select(Source))
        sources = result.scalars().all()
        print(f"[OK] Sources query: {len(sources)} sources found")
        for s in sources:
            print(f"  - {s.slug}: {s.name}")
        
        # Test 2: Get runs with source relationship
        result = await session.execute(
            select(Run).order_by(Run.started_at.desc()).limit(5)
        )
        runs = result.scalars().all()
        print(f"\n[OK] Runs query: {len(runs)} recent runs")
        for r in runs:
            print(f"  - {r.source.slug}: {r.status} | {r.records_stored} records")
        
        # Test 3: Get signals count by source
        result = await session.execute(
            select(Source.slug, func.count(NormalizedSignal.id))
            .join(NormalizedSignal, Source.id == NormalizedSignal.source_id)
            .group_by(Source.slug)
        )
        signal_counts = result.all()
        print(f"\n[OK] Signals by source:")
        for slug, count in signal_counts:
            print(f"  - {slug}: {count} signals")
        
        # Test 4: Get quality checks
        result = await session.execute(
            select(func.count(QualityCheck.id))
        )
        quality_count = result.scalar()
        print(f"\n[OK] Quality checks: {quality_count} total")
        
        # Test 5: Get freshness with source
        result = await session.execute(
            select(FreshnessStatus).options()
        )
        freshness_list = result.scalars().all()
        print(f"\n[OK] Freshness status:")
        for f in freshness_list:
            stale = "STALE" if f.is_stale else "FRESH"
            print(f"  - {f.source.slug}: {stale} ({f.staleness_minutes} min)")
        
        print("\n[SUCCESS] All database queries working correctly!")

if __name__ == "__main__":
    asyncio.run(test_queries())
