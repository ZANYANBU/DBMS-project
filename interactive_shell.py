import sqlite3
import sys

def print_results(cursor):
    if cursor.description:
        # Fetch results for SELECT queries
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        
        # Calculate widths
        widths = [len(c) for c in cols]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        
        # Print
        fmt = " | ".join([f"{{:<{w}}}" for w in widths])
        print("-" * (sum(widths) + 3 * (len(cols)-1)))
        print(fmt.format(*cols))
        print("-" * (sum(widths) + 3 * (len(cols)-1)))
        
        for row in rows:
            clean = [str(v) if v is not None else "" for v in row]
            print(fmt.format(*clean))
        print(f"\n({len(rows)} rows)")
    else:
        # For INSERT, UPDATE, DELETE
        print(f"\nQuery executed successfully. Rows affected: {cursor.rowcount}")

def run_shell():
    db_file = 'school_management.db'
    print(f"Connecting to {db_file}...")
    
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;") # Enforce FKs
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    print("================================================================")
    print(" SQLite Interactive Shell")
    print("----------------------------------------------------------------")
    print(" Enter your SQL commands below.")
    print(" Ends with ';' to execute.")
    print(" Type 'exit' or 'quit' to leave.")
    print("================================================================")

    buffer = ""
    
    while True:
        try:
            if not buffer:
                line = input("SQL> ")
            else:
                line = input("   > ")

            if line.strip().lower() in ('exit', 'quit'):
                break
                
            buffer += " " + line
            
            if buffer.strip().endswith(';'):
                command = buffer.strip()
                try:
                    cursor.execute(command)
                    print_results(cursor)
                    conn.commit()
                except sqlite3.Error as e:
                    print(f"Error: {e}")
                
                buffer = ""
                
        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")
            buffer = ""
        except EOFError:
            break

    conn.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    run_shell()
