import sqlite3
import os

db_file = 'school_management.db'
sql_file = 'school_management.sql'

if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Removed existing database: {db_file}")

print(f"Creating new database: {db_file}")
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

print(f"Reading SQL script: {sql_file}")
with open(sql_file, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Execute the entire script at once
try:
    cursor.executescript(sql_script)
    conn.commit()
    print("✓ Database initialized successfully!")
    
    # Verify tables
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"\n✓ Created {len(tables)} tables:")
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        print(f"  - {table[0]}: {count} rows")
    
except sqlite3.Error as e:
    print(f"✗ An error occurred: {e}")
finally:
    conn.close()
