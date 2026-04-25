"""Inspect the SQLite database state."""
import sqlite3
import os

DB_PATH = r"C:\dev\signalhub-apis\apps\api\signalhub.db"

if not os.path.exists(DB_PATH):
    print(f"DB file NOT FOUND at {DB_PATH}")
else:
    size = os.path.getsize(DB_PATH)
    print(f"DB file exists: {DB_PATH} ({size} bytes)")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\nTables found: {tables}")
    
    # Count rows in each table
    for table in tables:
        if table == "alembic_version":
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            print(f"  {table}: {rows}")
        else:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} rows")
    
    conn.close()
