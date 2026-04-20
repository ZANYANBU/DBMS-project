import sqlite3
import os

DB_NAME = 'school_management.db'

def fix_schema():
    if not os.path.exists(DB_NAME):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_NAME)
    
    # Add Dept to Student
    try:
        conn.execute("ALTER TABLE Student ADD COLUMN Dept TEXT")
        print("Added Dept to Student")
    except sqlite3.OperationalError:
        print("Dept already exists in Student")

    # Add Age to Student
    try:
        conn.execute("ALTER TABLE Student ADD COLUMN Age INTEGER")
        print("Added Age to Student")
    except sqlite3.OperationalError:
        print("Age already exists in Student")

    # Add Grade to Enrollment
    try:
        conn.execute("ALTER TABLE Enrollment ADD COLUMN Grade TEXT")
        print("Added Grade to Enrollment")
    except sqlite3.OperationalError:
        print("Grade already exists in Enrollment")

    conn.commit()
    conn.close()
    print("Schema checked/fixed.")

if __name__ == '__main__':
    fix_schema()
