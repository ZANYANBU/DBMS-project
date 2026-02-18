"""
Robust School Management System
Complete web application with multi-level authentication and CRUD operations
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime, date
from functools import wraps
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DB_NAME = 'school_management.db'

# =========================================================================================
# DATABASE UTILITIES
# =========================================================================================

def get_db():
    """Create database connection"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def query_db(query, args=(), one=False):
    """Execute a query and return results"""
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute an insert/update/delete query"""
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

# =========================================================================================
# AUTHENTICATION & AUTHORIZATION
# =========================================================================================

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_accounts():
    """Initialize user login accounts (run once)"""
    conn = get_db()
    cur = conn.cursor()
    
    # Create Login table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS User_Login (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password_Hash TEXT NOT NULL,
            Role TEXT CHECK(Role IN ('Admin', 'Staff', 'Student')) NOT NULL,
            Reference_ID INTEGER,
            Is_Active INTEGER DEFAULT 1,
            Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default admin account
    admin_exists = cur.execute("SELECT 1 FROM User_Login WHERE Username = 'admin'").fetchone()
    if not admin_exists:
        cur.execute("""
            INSERT INTO User_Login (Username, Password_Hash, Role, Reference_ID) 
            VALUES ('admin', ?, 'Admin', NULL)
        """, (hash_password('admin123'),))
    
    # Create staff accounts (using email prefix as username)
    staff_list = cur.execute("SELECT Staff_ID, Email FROM Staff").fetchall()
    for staff in staff_list:
        username = staff[1].split('@')[0]
        user_exists = cur.execute("SELECT 1 FROM User_Login WHERE Username = ?", (username,)).fetchone()
        if not user_exists:
            cur.execute("""
                INSERT INTO User_Login (Username, Password_Hash, Role, Reference_ID) 
                VALUES (?, ?, 'Staff', ?)
            """, (username, hash_password('staff123'), staff[0]))
    
    # Create student accounts (using email prefix as username)
    student_list = cur.execute("SELECT Student_ID, Email FROM Student").fetchall()
    for student in student_list:
        username = student[1].split('@')[0]
        user_exists = cur.execute("SELECT 1 FROM User_Login WHERE Username = ?", (username,)).fetchone()
        if not user_exists:
            cur.execute("""
                INSERT INTO User_Login (Username, Password_Hash, Role, Reference_ID) 
                VALUES (?, ?, 'Student', ?)
            """, (username, hash_password('student123'), student[0]))
    
    conn.commit()
    conn.close()

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =========================================================================================
# AUTHENTICATION ROUTES
# =========================================================================================

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        
        user = query_db('SELECT * FROM User_Login WHERE Username = ? AND Password_Hash = ? AND Is_Active = 1',
                       [username, password_hash], one=True)
        
        if user:
            session['user_id'] = user['User_ID']
            session['username'] = user['Username']
            session['role'] = user['Role']
            session['reference_id'] = user['Reference_ID']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - redirects based on role"""
    role = session.get('role')
    
    if role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'Staff':
        return redirect(url_for('staff_dashboard'))
    elif role == 'Student':
        return redirect(url_for('student_dashboard'))
    
    return redirect(url_for('index'))

# =========================================================================================
# ADMIN ROUTES
# =========================================================================================

@app.route('/admin/dashboard')
@login_required
@role_required('Admin')
def admin_dashboard():
    """Admin main dashboard"""
    # Get statistics
    stats = {
        'total_students': query_db('SELECT COUNT(*) as count FROM Student', one=True)['count'],
        'total_staff': query_db('SELECT COUNT(*) as count FROM Staff', one=True)['count'],
        'total_courses': query_db('SELECT COUNT(*) as count FROM Course', one=True)['count'],
        'total_classes': query_db('SELECT COUNT(*) as count FROM Class', one=True)['count'],
        'active_enrollments': query_db('SELECT COUNT(*) as count FROM Enrollment WHERE Status = "Enrolled"', one=True)['count']
    }
    
    # Recent enrollments
    recent_enrollments = query_db('''
        SELECT e.Date_Enrolled, s.First_Name || ' ' || s.Last_Name as Student_Name,
               c.Title as Course_Title, cl.Section, cl.Semester
        FROM Enrollment e
        JOIN Student s ON e.Student_ID = s.Student_ID
        JOIN Class cl ON e.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        ORDER BY e.Date_Enrolled DESC
        LIMIT 10
    ''')
    
    return render_template('admin/dashboard.html', stats=stats, recent_enrollments=recent_enrollments)

# ADMIN - STUDENTS

@app.route('/admin/students')
@login_required
@role_required('Admin')
def admin_students():
    """View all students"""
    students = query_db('SELECT * FROM Student ORDER BY Last_Name, First_Name')
    return render_template('admin/students.html', students=students)

@app.route('/admin/student/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_student_add():
    """Add new student"""
    if request.method == 'POST':
        try:
            student_id = execute_db('''
                INSERT INTO Student (First_Name, Last_Name, DOB, Email, Street_Address, 
                                    City, Zip_Code, Enrollment_Year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['first_name'],
                request.form['last_name'],
                request.form['dob'],
                request.form['email'],
                request.form['street_address'],
                request.form['city'],
                request.form['zip_code'],
                request.form['enrollment_year']
            ))
            
            # Create login account
            username = request.form['email'].split('@')[0]
            execute_db('''
                INSERT INTO User_Login (Username, Password_Hash, Role, Reference_ID)
                VALUES (?, ?, 'Student', ?)
            ''', (username, hash_password('student123'), student_id))
            
            flash(f'Student added successfully! Username: {username}, Password: student123', 'success')
            return redirect(url_for('admin_students'))
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'danger')
    
    return render_template('admin/student_form.html', student=None)

@app.route('/admin/student/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_student_edit(id):
    """Edit student"""
    if request.method == 'POST':
        try:
            execute_db('''
                UPDATE Student 
                SET First_Name = ?, Last_Name = ?, DOB = ?, Email = ?, 
                    Street_Address = ?, City = ?, Zip_Code = ?, Enrollment_Year = ?
                WHERE Student_ID = ?
            ''', (
                request.form['first_name'],
                request.form['last_name'],
                request.form['dob'],
                request.form['email'],
                request.form['street_address'],
                request.form['city'],
                request.form['zip_code'],
                request.form['enrollment_year'],
                id
            ))
            flash('Student updated successfully!', 'success')
            return redirect(url_for('admin_students'))
        except Exception as e:
            flash(f'Error updating student: {str(e)}', 'danger')
    
    student = query_db('SELECT * FROM Student WHERE Student_ID = ?', [id], one=True)
    return render_template('admin/student_form.html', student=student)

@app.route('/admin/student/delete/<int:id>')
@login_required
@role_required('Admin')
def admin_student_delete(id):
    """Delete student"""
    try:
        execute_db('DELETE FROM Student WHERE Student_ID = ?', [id])
        execute_db('DELETE FROM User_Login WHERE Role = "Student" AND Reference_ID = ?', [id])
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'danger')
    return redirect(url_for('admin_students'))

# ADMIN - STAFF

@app.route('/admin/staff')
@login_required
@role_required('Admin')
def admin_staff():
    """View all staff"""
    staff = query_db('SELECT * FROM Staff ORDER BY Last_Name, First_Name')
    return render_template('admin/staff.html', staff=staff)

@app.route('/admin/staff/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_staff_add():
    """Add new staff"""
    if request.method == 'POST':
        try:
            staff_id = execute_db('''
                INSERT INTO Staff (First_Name, Last_Name, Email, Designation, Hire_Date,
                                  Street_Address, City, Zip_Code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['first_name'],
                request.form['last_name'],
                request.form['email'],
                request.form['designation'],
                request.form['hire_date'],
                request.form['street_address'],
                request.form['city'],
                request.form['zip_code']
            ))
            
            # Create login account
            username = request.form['email'].split('@')[0]
            execute_db('''
                INSERT INTO User_Login (Username, Password_Hash, Role, Reference_ID)
                VALUES (?, ?, 'Staff', ?)
            ''', (username, hash_password('staff123'), staff_id))
            
            flash(f'Staff added successfully! Username: {username}, Password: staff123', 'success')
            return redirect(url_for('admin_staff'))
        except Exception as e:
            flash(f'Error adding staff: {str(e)}', 'danger')
    
    return render_template('admin/staff_form.html', staff=None)

# ADMIN - COURSES

@app.route('/admin/courses')
@login_required
@role_required('Admin')
def admin_courses():
    """View all courses"""
    courses = query_db('''
        SELECT c.*, d.Name as Department_Name
        FROM Course c
        LEFT JOIN Department d ON c.Dept_ID = d.Dept_ID
        ORDER BY c.Code
    ''')
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/course/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_course_add():
    """Add new course"""
    if request.method == 'POST':
        try:
            execute_db('''
                INSERT INTO Course (Code, Title, Credits, Dept_ID)
                VALUES (?, ?, ?, ?)
            ''', (
                request.form['code'],
                request.form['title'],
                request.form['credits'],
                request.form['dept_id'] if request.form['dept_id'] else None
            ))
            flash('Course added successfully!', 'success')
            return redirect(url_for('admin_courses'))
        except Exception as e:
            flash(f'Error adding course: {str(e)}', 'danger')
    
    departments = query_db('SELECT * FROM Department ORDER BY Name')
    return render_template('admin/course_form.html', course=None, departments=departments)

# ADMIN - CLASSES

@app.route('/admin/classes')
@login_required
@role_required('Admin')
def admin_classes():
    """View all classes"""
    classes = query_db('''
        SELECT cl.*, c.Code, c.Title, s.First_Name || ' ' || s.Last_Name as Teacher_Name
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        LEFT JOIN Staff s ON cl.Teacher_ID = s.Staff_ID
        ORDER BY cl.Semester DESC, c.Code
    ''')
    return render_template('admin/classes.html', classes=classes)

@app.route('/admin/class/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_class_add():
    """Add new class"""
    if request.method == 'POST':
        try:
            execute_db('''
                INSERT INTO Class (Course_ID, Section, Semester, Teacher_ID)
                VALUES (?, ?, ?, ?)
            ''', (
                request.form['course_id'],
                request.form['section'],
                request.form['semester'],
                request.form['teacher_id'] if request.form['teacher_id'] else None
            ))
            flash('Class added successfully!', 'success')
            return redirect(url_for('admin_classes'))
        except Exception as e:
            flash(f'Error adding class: {str(e)}', 'danger')
    
    courses = query_db('SELECT * FROM Course ORDER BY Code')
    teachers = query_db("SELECT * FROM Staff WHERE Designation IN ('Teacher', 'HOD') ORDER BY Last_Name")
    return render_template('admin/class_form.html', cls=None, courses=courses, teachers=teachers)

# ADMIN - ENROLLMENTS

@app.route('/admin/enrollments')
@login_required
@role_required('Admin')
def admin_enrollments():
    """View all enrollments"""
    enrollments = query_db('''
        SELECT e.*, 
               s.First_Name || ' ' || s.Last_Name as Student_Name,
               c.Code || ' - ' || c.Title as Course_Info,
               cl.Section, cl.Semester
        FROM Enrollment e
        JOIN Student s ON e.Student_ID = s.Student_ID
        JOIN Class cl ON e.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        ORDER BY e.Date_Enrolled DESC
    ''')
    return render_template('admin/enrollments.html', enrollments=enrollments)

@app.route('/admin/enrollment/add', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def admin_enrollment_add():
    """Add new enrollment"""
    if request.method == 'POST':
        try:
            execute_db('''
                INSERT INTO Enrollment (Student_ID, Class_ID, Date_Enrolled, Status)
                VALUES (?, ?, ?, 'Enrolled')
            ''', (
                request.form['student_id'],
                request.form['class_id'],
                datetime.now().date()
            ))
            flash('Enrollment added successfully!', 'success')
            return redirect(url_for('admin_enrollments'))
        except Exception as e:
            flash(f'Error adding enrollment: {str(e)}', 'danger')
    
    students = query_db('SELECT * FROM Student ORDER BY Last_Name, First_Name')
    classes = query_db('''
        SELECT cl.*, c.Code, c.Title
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        ORDER BY cl.Semester DESC, c.Code
    ''')
    return render_template('admin/enrollment_form.html', students=students, classes=classes)

# =========================================================================================
# STAFF ROUTES
# =========================================================================================

@app.route('/staff/dashboard')
@login_required
@role_required('Staff')
def staff_dashboard():
    """Staff main dashboard"""
    staff_id = session.get('reference_id')
    
    # Get staff info
    staff_info = query_db('SELECT * FROM Staff WHERE Staff_ID = ?', [staff_id], one=True)
    
    # Get classes taught by this staff
    classes = query_db('''
        SELECT cl.*, c.Code, c.Title,
               COUNT(DISTINCT e.Student_ID) as Enrollment_Count
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        LEFT JOIN Enrollment e ON cl.Class_ID = e.Class_ID AND e.Status = 'Enrolled'
        WHERE cl.Teacher_ID = ?
        GROUP BY cl.Class_ID
        ORDER BY cl.Semester DESC
    ''', [staff_id])
    
    return render_template('staff/dashboard.html', staff=staff_info, classes=classes)

@app.route('/staff/class/<int:class_id>')
@login_required
@role_required('Staff')
def staff_class_detail(class_id):
    """View class details"""
    staff_id = session.get('reference_id')
    
    # Verify this staff teaches this class
    class_info = query_db('''
        SELECT cl.*, c.Code, c.Title
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE cl.Class_ID = ? AND cl.Teacher_ID = ?
    ''', [class_id, staff_id], one=True)
    
    if not class_info:
        flash('You do not have access to this class.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    # Get enrolled students
    students = query_db('''
        SELECT s.*, e.Enrollment_ID, e.Status
        FROM Student s
        JOIN Enrollment e ON s.Student_ID = e.Student_ID
        WHERE e.Class_ID = ?
        ORDER BY s.Last_Name, s.First_Name
    ''', [class_id])
    
    return render_template('staff/class_detail.html', class_info=class_info, students=students)

@app.route('/staff/attendance/<int:class_id>', methods=['GET', 'POST'])
@login_required
@role_required('Staff')
def staff_attendance(class_id):
    """Mark attendance"""
    staff_id = session.get('reference_id')
    
    # Verify access
    class_info = query_db('''
        SELECT cl.*, c.Code, c.Title
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE cl.Class_ID = ? AND cl.Teacher_ID = ?
    ''', [class_id, staff_id], one=True)
    
    if not class_info:
        flash('Access denied.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    if request.method == 'POST':
        attendance_date = request.form['date']
        for key, value in request.form.items():
            if key.startswith('status_'):
                student_id = int(key.split('_')[1])
                execute_db('''
                    INSERT OR REPLACE INTO Attendance (Class_ID, Student_ID, Date, Status)
                    VALUES (?, ?, ?, ?)
                ''', (class_id, student_id, attendance_date, value))
        flash('Attendance saved successfully!', 'success')
        return redirect(url_for('staff_class_detail', class_id=class_id))
    
    # Get students
    students = query_db('''
        SELECT s.*
        FROM Student s
        JOIN Enrollment e ON s.Student_ID = e.Student_ID
        WHERE e.Class_ID = ? AND e.Status = 'Enrolled'
        ORDER BY s.Last_Name, s.First_Name
    ''', [class_id])
    
    # Get today's attendance if exists
    today = datetime.now().date()
    existing_attendance = {}
    attendance_records = query_db('''
        SELECT Student_ID, Status
        FROM Attendance
        WHERE Class_ID = ? AND Date = ?
    ''', [class_id, today])
    
    for record in attendance_records:
        existing_attendance[record['Student_ID']] = record['Status']
    
    return render_template('staff/attendance.html', class_info=class_info, 
                         students=students, today=today, existing_attendance=existing_attendance)

@app.route('/staff/grades/<int:class_id>')
@login_required
@role_required('Staff')
def staff_grades(class_id):
    """View and manage grades"""
    staff_id = session.get('reference_id')
    
    # Verify access
    class_info = query_db('''
        SELECT cl.*, c.Code, c.Title
        FROM Class cl
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE cl.Class_ID = ? AND cl.Teacher_ID = ?
    ''', [class_id, staff_id], one=True)
    
    if not class_info:
        flash('Access denied.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    # Get exams for this class
    exams = query_db('SELECT * FROM Exam WHERE Class_ID = ? ORDER BY Exam_Date', [class_id])
    
    # Get students and their grades
    students = query_db('''
        SELECT s.Student_ID, s.First_Name, s.Last_Name
        FROM Student s
        JOIN Enrollment e ON s.Student_ID = e.Student_ID
        WHERE e.Class_ID = ? AND e.Status = 'Enrolled'
        ORDER BY s.Last_Name, s.First_Name
    ''', [class_id])
    
    # Get all grades for this class
    grades = query_db('''
        SELECT g.*, e.Exam_ID, e.Title as Exam_Title
        FROM Grade g
        JOIN Exam e ON g.Exam_ID = e.Exam_ID
        WHERE e.Class_ID = ?
    ''', [class_id])
    
    # Organize grades by student and exam
    grade_matrix = {}
    for grade in grades:
        if grade['Student_ID'] not in grade_matrix:
            grade_matrix[grade['Student_ID']] = {}
        grade_matrix[grade['Student_ID']][grade['Exam_ID']] = grade
    
    return render_template('staff/grades.html', class_info=class_info, 
                         exams=exams, students=students, grade_matrix=grade_matrix)

@app.route('/staff/exam/add/<int:class_id>', methods=['GET', 'POST'])
@login_required
@role_required('Staff')
def staff_exam_add(class_id):
    """Add new exam"""
    staff_id = session.get('reference_id')
    
    # Verify access
    class_info = query_db('''
        SELECT cl.Class_ID FROM Class cl WHERE cl.Class_ID = ? AND cl.Teacher_ID = ?
    ''', [class_id, staff_id], one=True)
    
    if not class_info:
        flash('Access denied.', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    if request.method == 'POST':
        try:
            execute_db('''
                INSERT INTO Exam (Class_ID, Title, Total_Marks, Weightage_Percent, Exam_Date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                class_id,
                request.form['title'],
                request.form['total_marks'],
                request.form['weightage_percent'],
                request.form['exam_date']
            ))
            flash('Exam added successfully!', 'success')
            return redirect(url_for('staff_grades', class_id=class_id))
        except Exception as e:
            flash(f'Error adding exam: {str(e)}', 'danger')
    
    return render_template('staff/exam_form.html', class_id=class_id)

@app.route('/staff/grade/edit/<int:exam_id>/<int:student_id>', methods=['POST'])
@login_required
@role_required('Staff')
def staff_grade_edit(exam_id, student_id):
    """Update grade"""
    try:
        marks = request.form['marks']
        comments = request.form.get('comments', '')
        
        execute_db('''
            INSERT OR REPLACE INTO Grade (Exam_ID, Student_ID, Marks_Obtained, Comments)
            VALUES (?, ?, ?, ?)
        ''', (exam_id, student_id, marks, comments))
        
        return jsonify({'success': True, 'message': 'Grade updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# =========================================================================================
# STUDENT ROUTES
# =========================================================================================

@app.route('/student/dashboard')
@login_required
@role_required('Student')
def student_dashboard():
    """Student main dashboard"""
    student_id = session.get('reference_id')
    
    # Get student info
    student_info = query_db('SELECT * FROM Student WHERE Student_ID = ?', [student_id], one=True)
    
    # Get enrolled classes
    classes = query_db('''
        SELECT cl.*, c.Code, c.Title, 
               s.First_Name || ' ' || s.Last_Name as Teacher_Name,
               e.Status, e.Date_Enrolled
        FROM Enrollment e
        JOIN Class cl ON e.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        LEFT JOIN Staff s ON cl.Teacher_ID = s.Staff_ID
        WHERE e.Student_ID = ?
        ORDER BY cl.Semester DESC, c.Code
    ''', [student_id])
    
    return render_template('student/dashboard.html', student=student_info, classes=classes)

@app.route('/student/grades')
@login_required
@role_required('Student')
def student_grades():
    """View all grades"""
    student_id = session.get('reference_id')
    
    # Get all grades
    grades = query_db('''
        SELECT g.*, e.Title as Exam_Title, e.Total_Marks, e.Weightage_Percent,
               c.Code, c.Title as Course_Title, cl.Section, cl.Semester
        FROM Grade g
        JOIN Exam e ON g.Exam_ID = e.Exam_ID
        JOIN Class cl ON e.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE g.Student_ID = ?
        ORDER BY cl.Semester DESC, c.Code, e.Exam_Date
    ''', [student_id])
    
    return render_template('student/grades.html', grades=grades)

@app.route('/student/attendance')
@login_required
@role_required('Student')
def student_attendance():
    """View attendance records"""
    student_id = session.get('reference_id')
    
    # Get attendance records
    attendance = query_db('''
        SELECT a.*, c.Code, c.Title, cl.Section, cl.Semester
        FROM Attendance a
        JOIN Class cl ON a.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE a.Student_ID = ?
        ORDER BY a.Date DESC
    ''', [student_id])
    
    # Calculate attendance statistics per class
    stats = query_db('''
        SELECT cl.Class_ID, c.Code, c.Title,
               COUNT(*) as Total_Days,
               SUM(CASE WHEN a.Status = 'Present' THEN 1 ELSE 0 END) as Present_Days,
               ROUND(100.0 * SUM(CASE WHEN a.Status = 'Present' THEN 1 ELSE 0 END) / COUNT(*), 2) as Percentage
        FROM Attendance a
        JOIN Class cl ON a.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        WHERE a.Student_ID = ?
        GROUP BY cl.Class_ID
    ''', [student_id])
    
    return render_template('student/attendance.html', attendance=attendance, stats=stats)

@app.route('/student/schedule')
@login_required
@role_required('Student')
def student_schedule():
    """View class schedule"""
    student_id = session.get('reference_id')
    
    # Get schedule
    schedule = query_db('''
        SELECT cs.*, c.Code, c.Title, cl.Section,
               r.Room_Number, r.Building,
               s.First_Name || ' ' || s.Last_Name as Teacher_Name
        FROM Enrollment e
        JOIN Class cl ON e.Class_ID = cl.Class_ID
        JOIN Course c ON cl.Course_ID = c.Course_ID
        LEFT JOIN Class_Schedule cs ON cl.Class_ID = cs.Class_ID
        LEFT JOIN Classroom r ON cs.Room_ID = r.Room_ID
        LEFT JOIN Staff s ON cl.Teacher_ID = s.Staff_ID
        WHERE e.Student_ID = ? AND e.Status = 'Enrolled'
        ORDER BY 
            CASE cs.Day_of_Week
                WHEN 'Mon' THEN 1
                WHEN 'Tue' THEN 2
                WHEN 'Wed' THEN 3
                WHEN 'Thu' THEN 4
                WHEN 'Fri' THEN 5
                WHEN 'Sat' THEN 6
            END,
            cs.Start_Time
    ''', [student_id])
    
    return render_template('student/schedule.html', schedule=schedule)

# =========================================================================================
# ERROR HANDLERS
# =========================================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found', code=404), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error='Internal server error', code=500), 500

# =========================================================================================
# MAIN
# =========================================================================================

if __name__ == '__main__':
    # Initialize user accounts
    print("Initializing user accounts...")
    init_user_accounts()
    print("User accounts initialized!")
    print("\nDefault Login Credentials:")
    print("=" * 50)
    print("Admin:    username='admin',     password='admin123'")
    print("Staff:    username=<email_prefix>, password='staff123'")
    print("Student:  username=<email_prefix>, password='student123'")
    print("=" * 50)
    print("\nStarting Flask server on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
