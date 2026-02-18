import sqlite3

def run_file():
    db_file = 'school_management.db'
    sql_file = 'custom_query.sql'
    
    try:
        with open(sql_file, 'r') as f:
            sql_script = f.read()
    except FileNotFoundError:
        print(f"Error: {sql_file} not found.")
        return

    print(f"Executing SQL from {sql_file}...\n")

    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        
        # Split by semicolon to handle multiple statements if needed
        # But allow simple script execution
        cursor.executescript(sql_script)
        conn.commit() # Ensure changes are saved
        
        # Note: executescript doesn't return rows directly for all statements easily like execute()
        # So we often use execute() for single queries to see results
        # Let's try to detect if it's a SELECT and use execute to show results
        
        conn.close()
        
        # Re-connect for a single result fetch (better for "SELECT *" type usage)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Trim and check if it looks like a SELECT
        stripped = sql_script.strip().upper()
        if stripped.startswith("SELECT") or stripped.startswith("WITH"):
            cursor.execute(sql_script)
            
            if cursor.description:
                cols = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                
                # Formatting
                widths = [len(c) for c in cols]
                for row in rows:
                    for i, val in enumerate(row):
                        widths[i] = max(widths[i], len(str(val)))
                
                fmt = " | ".join([f"{{:<{w}}}" for w in widths])
                print(fmt.format(*cols))
                print("-" * (sum(widths) + 3 * (len(cols)-1)))
                
                for row in rows:
                    clean = [str(v) if v is not None else "" for v in row]
                    print(fmt.format(*clean))
                print(f"\n({len(rows)} rows)")
        else:
             print("Script executed. (Output only shown for single SELECT queries in this mode)")

        conn.close()

    except sqlite3.Error as e:
        print(f"SQL Error: {e}")

if __name__ == "__main__":
    run_file()