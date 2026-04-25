import sqlite3

conn = sqlite3.connect('C:/dev/signalhub-apis/apps/api/signalhub.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables found:", [t[0] for t in tables])

# Get count of sources if table exists
if any('sources' in t for t in tables):
    cursor.execute("SELECT COUNT(*) FROM sources")
    count = cursor.fetchone()[0]
    print(f"Sources count: {count}")
    
    if count > 0:
        cursor.execute("SELECT slug, name FROM sources")
        sources = cursor.fetchall()
        print("Sources:")
        for s in sources:
            print(f"  - {s[0]}: {s[1]}")

conn.close()
