# 🎓 School Management System

A comprehensive, enterprise-level classroom management system built with Flask and SQLite.

## Features

### 🔐 Multi-Level Authentication
- **Admin Access**: Full system control with complete CRUD operations
- **Staff Access**: Class management, attendance tracking, and grade entry
- **Student Access**: View grades, attendance, and class schedules

### 📚 Complete Management Capabilities
- Student Management (Add, Edit, Delete, View)
- Staff Management (Add, Edit, View)
- Course Management (Add, Edit, View)
- Class Management (Add, Edit, View)
- Enrollment Management (Add, View)
- Attendance Tracking (Mark and View)
- Grade Management (Create exams, enter grades)
- Class Scheduling (View schedules)

### 💾 Robust Database Design
- Normalized schema (3NF/BCNF)
- Referential integrity enforced
- Multi-valued attributes handled
- Composite attributes split appropriately
- Weak entities included (Guardians)

## Quick Start

### Prerequisites
- Python 3.7+ installed
- pip (Python package manager)

### Installation & Running

#### Option 1: Using PowerShell Script (Recommended)
```powershell
.\start.ps1
```

#### Option 2: Manual Setup
```powershell
# Install Flask
pip install flask

# Initialize database
python init_db.py

# Run the application
python app.py
```

The application will start at: **http://127.0.0.1:5000**

## Default Login Credentials

### Admin
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system administration

### Staff (Examples)
- **Username**: `snape` (or any staff email prefix)
- **Password**: `staff123`
- **Access**: Class management, attendance, grades

Some other staff usernames:
- `lupin`, `slughorn`, `sprout`, `flit`

### Student (Examples)
- **Username**: `harry` (or any student email prefix)
- **Password**: `student123`
- **Access**: View grades, attendance, schedule

Some other student usernames:
- `hermione`, `ron`, `draco`, `luna`, `neville`

## System Structure

```
SQL/
├── app.py                      # Main Flask application
├── init_db.py                  # Database initialization script
├── start.ps1                   # PowerShell startup script
├── school_management.sql       # SQL schema and data
├── school_management.db        # SQLite database (created on first run)
├── static/
│   └── css/
│       └── style.css          # Modern CSS styling
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Landing page
    ├── login.html             # Login page
    ├── error.html             # Error page
    ├── admin/                 # Admin templates
    │   ├── dashboard.html
    │   ├── students.html
    │   ├── student_form.html
    │   ├── staff.html
    │   ├── staff_form.html
    │   ├── courses.html
    │   ├── course_form.html
    │   ├── classes.html
    │   ├── class_form.html
    │   ├── enrollments.html
    │   └── enrollment_form.html
    ├── staff/                 # Staff templates
    │   ├── dashboard.html
    │   ├── class_detail.html
    │   ├── attendance.html
    │   ├── grades.html
    │   └── exam_form.html
    └── student/               # Student templates
        ├── dashboard.html
        ├── grades.html
        ├── attendance.html
        └── schedule.html
```

## User Workflows

### Admin Workflow
1. Login with admin credentials
2. Access admin dashboard with system statistics
3. Manage students, staff, courses, classes, and enrollments
4. Add/Edit/Delete records as needed
5. View comprehensive reports

### Staff Workflow
1. Login with staff credentials
2. View assigned classes
3. Mark attendance for classes
4. Create exams and enter grades
5. View student rosters

### Student Workflow
1. Login with student credentials
2. View enrolled classes
3. Check grades for all exams
4. View attendance records and statistics
5. See class schedule

## Database Schema

The system uses 15 interconnected tables:
- **Staff**: Staff members with designations
- **Staff_Phone**: Multiple phone numbers per staff
- **Staff_Qualification**: Academic qualifications
- **Department**: Academic departments
- **Student**: Student records
- **Student_Phone**: Multiple phone numbers per student
- **Guardian**: Student guardians/emergency contacts
- **Classroom**: Physical classrooms
- **Course**: Course catalog
- **Class**: Class instances (course offerings)
- **Class_Schedule**: Time and room allocation
- **Enrollment**: Student-Class relationships
- **Exam**: Examinations
- **Grade**: Exam scores
- **Attendance**: Daily attendance records

## Security Features
- Password hashing (SHA-256)
- Session-based authentication
- Role-based access control
- SQL injection prevention (parameterized queries)
- CSRF protection via Flask sessions

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Session-based with password hashing

## Development Notes
- The application runs in debug mode by default
- The database is automatically initialized on first run
- User accounts are automatically created for all staff and students
- Foreign key constraints are enforced

## Support & Customization
This system is designed to be easily customizable. Key areas for customization:
- Add more designations in the Staff table
- Extend the grading system
- Add more reports and analytics
- Implement email notifications
- Add file upload capabilities
- Integrate with external systems

## License
Educational/Academic Use

## Contact
For issues or questions, refer to the application logs or database schema.

---

**Enjoy managing your school with this comprehensive system!** 🎓✨
