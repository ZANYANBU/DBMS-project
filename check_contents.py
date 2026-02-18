import sqlite3

def print_table(cursor, table_name, limit=10):
    print(f"\n{'='*60}")
    print(f" TABLE: {table_name}")
    print(f"{'='*60}")
    
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        col_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        count = len(rows)
        
        print(f"Total Records: {count}")
        print(f"Columns: {', '.join(col_names)}")
        print("-" * 60)
        
        if count == 0:
            print("(No Data)")
            return

        display_rows = rows
        is_truncated = False
        if count > limit:
            display_rows = rows[:5] + [("...",) * len(col_names)] + rows[-5:]
            is_truncated = True

        # Calculate column widths based on display_rows
        widths = [len(c) for c in col_names]
        for row in display_rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        
        # Create format string
        fmt = " | ".join([f"{{:<{w}}}" for w in widths])
        
        # Print Header
        print(fmt.format(*col_names))
        print("-" * (sum(widths) + 3 * (len(col_names) - 1)))
        
        # Print Rows
        for row in display_rows:
            # Handle None values
            clean_row = [str(v) if v is not None else "" for v in row]
            print(fmt.format(*clean_row))
            
        if is_truncated:
            print(f"\n... (Showing 5 first and 5 last of {count} records) ...")

    except sqlite3.Error as e:
        print(f"Error: {e}")

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
all_tables = [r[0] for r in cursor.fetchall()]

# Order tables specifically
preferred_order = ['Department', 'Teacher', 'Classroom', 'Student', 'Class', 'Exam', 'Enrollment', 'Timetable', 'Grade', 'Attendance']
ordered_tables = [t for t in preferred_order if t in all_tables]
remaining = [t for t in all_tables if t not in preferred_order]

for table in ordered_tables + remaining:
    print_table(cursor, table, limit=12)

conn.close()
