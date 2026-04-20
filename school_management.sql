-- 1. STAFF (Strong Entity)
CREATE TABLE Staff (
    Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Hire_Date DATE NOT NULL,
    Role TEXT CHECK(Role IN ('Teacher', 'Admin', 'Support'))
);

-- 2. STAFF_PHONE (Multi-valued Attribute)
CREATE TABLE Staff_Phone (
    Phone_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Staff_ID INTEGER NOT NULL,
    Phone_Number TEXT NOT NULL,
    Type TEXT CHECK(Type IN ('Mobile', 'Home', 'Work')),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE CASCADE
);

-- 3. STAFF_QUALIFICATION (Multi-valued Attribute)
CREATE TABLE Staff_Qualification (
    Qual_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Staff_ID INTEGER NOT NULL,
    Degree TEXT NOT NULL, -- e.g., 'PhD', 'MSc', 'BEd'
    Institution TEXT NOT NULL,
    Year_Obtained INTEGER,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE CASCADE
);

-- 4. DEPARTMENT
CREATE TABLE Department (
    Dept_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    HOD_Staff_ID INTEGER UNIQUE, -- 1:1 Relationship for HOD
    Office_Location TEXT,
    FOREIGN KEY (HOD_Staff_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
);

-- 5. STUDENT (Strong Entity)
CREATE TABLE Student (
    Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    DOB DATE NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Street_Address TEXT,
    City TEXT,
    Zip_Code TEXT,
    Enrollment_Year INTEGER NOT NULL
);

-- 6. STUDENT_PHONE (Multi-valued Attribute)
CREATE TABLE Student_Phone (
    Phone_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Phone_Number TEXT NOT NULL,
    Type TEXT DEFAULT 'Mobile',
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE
);

-- 7. GUARDIAN (Weak Entity - depends on Student)
CREATE TABLE Guardian (
    Guardian_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Relationship TEXT CHECK(Relationship IN ('Father', 'Mother', 'Guardian', 'Sibling')),
    Phone_Number TEXT NOT NULL,
    Email TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE
);

-- 8. CLASSROOM
CREATE TABLE Classroom (
    Room_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Room_Number TEXT NOT NULL UNIQUE,
    Capacity INTEGER NOT NULL,
    Type TEXT CHECK(Type IN ('Lecture Hall', 'Lab', 'Seminar Room')),
    Building TEXT NOT NULL
);

-- 9. COURSE (Catalog of subjects offered)
CREATE TABLE Course (
    Course_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code TEXT UNIQUE NOT NULL, -- e.g., 'CS101'
    Title TEXT NOT NULL,
    Credits INTEGER NOT NULL,
    Dept_ID INTEGER,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dept_ID) ON DELETE CASCADE
);

-- 10. CLASS (Specific offering of a course in a term)
CREATE TABLE Class (
    Class_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Course_ID INTEGER NOT NULL,
    Section TEXT NOT NULL, -- 'A', 'B'
    Semester TEXT NOT NULL, -- 'Spring 2026'
    Teacher_ID INTEGER,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE,
    FOREIGN KEY (Teacher_ID) REFERENCES Staff(Staff_ID) ON DELETE SET NULL
);

-- 11. CLASS_SCHEDULE (Time and Room allocation)
CREATE TABLE Class_Schedule (
    Schedule_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Class_ID INTEGER NOT NULL,
    Room_ID INTEGER NOT NULL,
    Day_of_Week TEXT CHECK(Day_of_Week IN ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')),
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE,
    FOREIGN KEY (Room_ID) REFERENCES Classroom(Room_ID) ON DELETE CASCADE
);

-- 12. ENROLLMENT (M:N Relationship between Student and Class)
CREATE TABLE Enrollment (
    Enrollment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Class_ID INTEGER NOT NULL,
    Status TEXT CHECK(Status IN ('Enrolled', 'Dropped', 'Completed', 'Waitlisted')) DEFAULT 'Enrolled',
    Enrollment_Date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE,
    UNIQUE(Student_ID, Class_ID) -- Prevent duplicate enrollment
);

-- 13. ATTENDANCE
CREATE TABLE Attendance (
    Attendance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Class_ID INTEGER NOT NULL,
    Date DATE NOT NULL,
    Status TEXT CHECK(Status IN ('Present', 'Absent', 'Late', 'Excused')),
    Remarks TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE
);

-- 14. EXAM
CREATE TABLE Exam (
    Exam_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Class_ID INTEGER NOT NULL,
    Title TEXT NOT NULL, -- 'Midterm', 'Final'
    Date DATE NOT NULL,
    Max_Marks INTEGER NOT NULL,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE
);

-- 15. GRADE
CREATE TABLE Grade (
    Grade_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Exam_ID INTEGER NOT NULL,
    Marks_Obtained REAL CHECK(Marks_Obtained >= 0),
    Grade_Letter TEXT, -- 'A', 'B+'
    Comments TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID) ON DELETE CASCADE,
    UNIQUE(Student_ID, Exam_ID)
);


-- =========================================================================================
-- DATA SEEDING
-- =========================================================================================

-- Seed Staff
INSERT INTO Staff (First_Name, Last_Name, Email, Hire_Date, Role) VALUES 
('John', 'Smith', 'john.smith@school.edu', '2015-08-15', 'Teacher'),
('Maria', 'Garcia', 'maria.garcia@school.edu', '2018-01-10', 'Teacher'),
('David', 'Johnson', 'david.johnson@school.edu', '2012-05-20', 'Admin'),
('Sarah', 'Williams', 'sarah.williams@school.edu', '2020-09-01', 'Teacher');

-- Seed Departments
INSERT INTO Department (Name, HOD_Staff_ID, Office_Location) VALUES 
('Computer Science', 1, 'Building A, Room 101'),
('Mathematics', 2, 'Building B, Room 205'),
('Administration', 3, 'Main Hall, Room 1');

-- Seed Courses
INSERT INTO Course (Code, Title, Credits, Dept_ID) VALUES
('CS101', 'Intro to Programming', 4, 1),
('CS201', 'Data Structures', 4, 1),
('CS202', 'Database Systems', 4, 1),
('CS303', 'Operating Systems', 4, 1),
('CS305', 'Computer Networks', 4, 1),
('MATH101', 'Calculus I', 3, 2),
('MATH102', 'Discrete Mathematics', 3, 2),
('MATH201', 'Linear Algebra', 3, 2),
('MATH202', 'Probability and Statistics', 3, 2),
('ADM101', 'Academic Writing', 2, 3),
('ADM201', 'Communication Skills', 2, 3),
('EC101', 'Intro to Electronics', 4, 2),
('ME101', 'Thermodynamics', 4, 2),
('CV101', 'Structural Engineering Basics', 4, 2);

-- Seed Classrooms
INSERT INTO Classroom (Room_Number, Capacity, Type, Building) VALUES
('A101', 30, 'Lab', 'Building A'),
('B205', 50, 'Lecture Hall', 'Building B');

-- Seed Classes
INSERT INTO Class (Course_ID, Section, Semester, Teacher_ID) VALUES
(1, 'A', 'Spring 2026', 1), -- CS101 by John Smith
(3, 'A', 'Spring 2026', 2); -- MATH101 by Maria Garcia

-- Seed Students
INSERT INTO Student (First_Name, Last_Name, DOB, Email, Enrollment_Year, City) VALUES
('Alice', 'Brown', '2005-03-12', 'alice.b@student.edu', 2023, 'New York'),
('Bob', 'Davis', '2004-11-25', 'bob.d@student.edu', 2023, 'Los Angeles'),
('Charlie', 'Wilson', '2005-07-08', 'charlie.w@student.edu', 2024, 'Chicago'),
('Diana', 'Miller', '2006-01-30', 'diana.m@student.edu', 2024, 'New York');

-- Seed Enrollments
INSERT INTO Enrollment (Student_ID, Class_ID) VALUES
(1, 1), (2, 1), (3, 1), -- CS101
(1, 2), (4, 2);         -- MATH101
