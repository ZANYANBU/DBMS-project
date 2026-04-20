import sqlite3
import pandas as pd
import os

# Set pandas display options to ensure columns align nicely
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 10)  # Show top 10 rows

DB_NAME = 'school_management.db'

def inspect_data():
    if not os.path.exists(DB_NAME):
        print(f"Error: {DB_NAME} not found.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nScanning Database: {DB_NAME}")
    print("="*60)
    
    if not tables:
        print("No tables found in the database.")
        conn.close()
        return

    for table in tables:
        table_name = table[0]
        if table_name == 'sqlite_sequence': continue 
        
        print(f"\nTABLE: {table_name}")
        print("-" * 30)
        
        # Count rows
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Total Rows: {count}")
        
        if count > 0:
            print("Preview (Top 5 rows):")
            try:
                # Use pandas for pretty printing if available, else raw fetch
                df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
                print(df.to_string(index=False))
            except ImportError:
                # Fallback if pandas not installed
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                cols = [description[0] for description in cursor.description]
                print(f"| {' | '.join(cols)} |")
                for row in cursor.fetchall():
                    print(f"| {' | '.join(map(str, row))} |")
        else:
            print("(Table is empty)")
        print("="*60)

    conn.close()

if __name__ == "__main__":
    try:
        import pandas
    except ImportError:
        print("Note: Install pandas (`pip install pandas`) for prettier table output, looking for basic view...")
    
    inspect_data()
