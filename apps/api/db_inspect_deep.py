"""Deeper inspection of the SQLite database."""
import sqlite3

DB_PATH = r"C:\dev\signalhub-apis\apps\api\signalhub.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=== SOURCES ===")
cursor.execute("SELECT id, slug, name, is_active FROM sources")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== RUNS (last 5) ===")
cursor.execute("SELECT id, source_id, status, duration_ms, records_fetched, records_stored, error_message, idempotency_key FROM runs ORDER BY started_at DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"  status={row[2]}, duration={row[3]}ms, fetched={row[4]}, stored={row[5]}, err={row[6]}, key={row[7]}")

print("\n=== FRESHNESS ===")
cursor.execute("SELECT source_id, last_success_at, last_attempt_at, is_stale, staleness_minutes FROM freshness_status")
for row in cursor.fetchall():
    print(f"  src={row[0][:8]}... success={row[1]}, attempt={row[2]}, stale={row[3]}, mins={row[4]}")

print("\n=== SIGNALS (sample 5) ===")
cursor.execute("SELECT signal_type, signal_key, signal_value, signal_unit FROM normalized_signals LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== QUALITY CHECKS (sample 5) ===")
cursor.execute("SELECT check_name, check_status, expected_value, actual_value FROM quality_checks LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n=== RUN STATUS DISTRIBUTION ===")
cursor.execute("SELECT status, COUNT(*) FROM runs GROUP BY status")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
