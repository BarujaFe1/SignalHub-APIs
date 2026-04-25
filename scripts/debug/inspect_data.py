import sqlite3
from datetime import datetime

conn = sqlite3.connect('C:/dev/signalhub-apis/apps/api/signalhub.db')
cursor = conn.cursor()

# Check runs
cursor.execute("SELECT COUNT(*) FROM runs")
runs_count = cursor.fetchone()[0]
print(f"Runs count: {runs_count}")

if runs_count > 0:
    cursor.execute("""
        SELECT r.status, s.slug, r.started_at, r.records_stored 
        FROM runs r 
        JOIN sources s ON r.source_id = s.id 
        ORDER BY r.started_at DESC 
        LIMIT 10
    """)
    runs = cursor.fetchall()
    print("\nRecent runs:")
    for r in runs:
        print(f"  - {r[1]}: {r[0]} | {r[2]} | {r[3]} records")

# Check signals
cursor.execute("SELECT COUNT(*) FROM normalized_signals")
signals_count = cursor.fetchone()[0]
print(f"\nNormalized signals count: {signals_count}")

# Check quality checks
cursor.execute("SELECT COUNT(*) FROM quality_checks")
quality_count = cursor.fetchone()[0]
print(f"Quality checks count: {quality_count}")

# Check freshness
cursor.execute("""
    SELECT s.slug, f.is_stale, f.staleness_minutes, f.last_success_at
    FROM freshness_status f
    JOIN sources s ON f.source_id = s.id
""")
freshness = cursor.fetchall()
print("\nFreshness status:")
for f in freshness:
    stale_status = "STALE" if f[1] else "FRESH"
    print(f"  - {f[0]}: {stale_status} ({f[2]} min) | Last success: {f[3]}")

conn.close()
