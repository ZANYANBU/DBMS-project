import sqlite3

def run_query(title, sql, params=()):
    print(f"\n{'='*80}")
    print(f" REPORT: {title}")
    print(f"{'='*80}")
    
    try:
        cursor.execute(sql, params)
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print("(No results found)")
            return

        # Calculate column widths
        widths = [len(c) for c in cols]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        
        # Create format string
        fmt = " | ".join([f"{{:<{w}}}" for w in widths])
        
        # Print Header
        print(fmt.format(*cols))
        print("-" * (sum(widths) + 3 * (len(cols) - 1)))
        
        # Print Rows
        for row in rows:
            # Handle None values
            clean_row = [str(v) if v is not None else "" for v in row]
            print(fmt.format(*clean_row))
            
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# Query 1: Student Schedule
sql_schedule = """
SELECT 
    s.Name as Student,
    c.Name as Class,
    c.Section,
    t.Name as Teacher,
    tt.Day_of_Week,
    tt.Start_Time || ' - ' || tt.End_Time as Time,
    cr.Room_Number
FROM Student s
JOIN Enrollment e ON s.Student_ID = e.Student_ID
JOIN Class c ON e.Class_ID = c.Class_ID
JOIN Teacher t ON c.Teacher_ID = t.Teacher_ID
LEFT JOIN Timetable tt ON c.Class_ID = tt.Class_ID
LEFT JOIN Classroom cr ON tt.Room_ID = cr.Room_ID
WHERE s.Student_ID = ?
ORDER BY 
    CASE tt.Day_of_Week 
        WHEN 'Monday' THEN 1 
        WHEN 'Tuesday' THEN 2 
        WHEN 'Wednesday' THEN 3 
        WHEN 'Thursday' THEN 4 
        WHEN 'Friday' THEN 5 
    END, 
    tt.Start_Time;
"""
run_query("Weekly Schedule for Student ID 1 (James Smith)", sql_schedule, (1,))

# Query 2: Department Summary
sql_dept_stats = """
SELECT 
    d.Name as Department,
    t_head.Name as Head_Teacher,
    COUNT(DISTINCT t.Teacher_ID) as Teachers,
    COUNT(DISTINCT c.Class_ID) as Classes
FROM Department d
LEFT JOIN Teacher t_head ON d.Head_Teacher_ID = t_head.Teacher_ID
LEFT JOIN Teacher t ON d.Dept_ID = t.Dept_ID
LEFT JOIN Class c ON d.Dept_ID = c.Dept_ID
GROUP BY d.Dept_ID
ORDER BY d.Name;
"""
run_query("Department Statistics", sql_dept_stats)

# Query 3: Exam Results
sql_grades = """
SELECT 
    e.Title as Exam,
    st.Name as Student,
    g.Marks_Obtained as Mark,
    g.Grade_Letter as Grade
FROM Grade g
JOIN Student st ON g.Student_ID = st.Student_ID
JOIN Exam e ON g.Exam_ID = e.Exam_ID
WHERE e.Title = 'Algebra Midterm'
ORDER BY g.Marks_Obtained DESC
LIMIT 10;
"""
run_query("Top 10 Results: Algebra Midterm", sql_grades)

# Query 4: Absenteeism
sql_attendance = """
SELECT 
    a.Date,
    st.Name as Student,
    c.Name as Class,
    a.Status
FROM Attendance a
JOIN Student st ON a.Student_ID = st.Student_ID
JOIN Class c ON a.Class_ID = c.Class_ID
WHERE a.Status IN ('Absent', 'Late')
ORDER BY a.Date DESC;
"""
run_query("Absent/Late Record", sql_attendance)

# Query 5: Teachers Loading
sql_teacher_load = """
SELECT 
    t.Name as Teacher,
    d.Name as Dept,
    COUNT(c.Class_ID) as Classes_Taught,
    GROUP_CONCAT(c.Name, ', ') as Course_List
FROM Teacher t
JOIN Department d ON t.Dept_ID = d.Dept_ID
LEFT JOIN Class c ON t.Teacher_ID = c.Teacher_ID
GROUP BY t.Teacher_ID
HAVING COUNT(c.Class_ID) > 0
ORDER BY Classes_Taught DESC;
"""
run_query("Teacher Workload", sql_teacher_load)

conn.close()
