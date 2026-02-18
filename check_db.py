import sqlite3

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# Get all tables
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")
    
conn.close()
