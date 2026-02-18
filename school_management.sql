-- PLACEHOLDER - THIS FILE NEEDS TO BE REGENERATED
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

-- 12. ENROLLMENT (M:N Relationship)
CREATE TABLE Enrollment (
    Enrollment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Student_ID INTEGER NOT NULL,
    Class_ID INTEGER NOT NULL,
    Date_Enrolled DATE DEFAULT CURRENT_DATE,
    Status TEXT CHECK(Status IN ('Enrolled', 'Completed', 'Dropped', 'Withdrawn')) DEFAULT 'Enrolled',
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE,
    UNIQUE(Student_ID, Class_ID)
);

-- 13. EXAM
CREATE TABLE Exam (
    Exam_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Class_ID INTEGER NOT NULL,
    Title TEXT NOT NULL, -- 'Midterm', 'Final', 'Quiz 1'
    Total_Marks INTEGER NOT NULL,
    Weightage_Percent INTEGER,
    Exam_Date DATE NOT NULL,
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE
);

-- 14. GRADE
CREATE TABLE Grade (
    Grade_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Exam_ID INTEGER NOT NULL,
    Student_ID INTEGER NOT NULL,
    Marks_Obtained REAL CHECK(Marks_Obtained >= 0),
    Comments TEXT,
    FOREIGN KEY (Exam_ID) REFERENCES Exam(Exam_ID) ON DELETE CASCADE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    UNIQUE(Exam_ID, Student_ID)
);

-- 15. ATTENDANCE
CREATE TABLE Attendance (
    Attendance_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Class_ID INTEGER NOT NULL,
    Student_ID INTEGER NOT NULL,
    Date DATE NOT NULL,
    Status TEXT CHECK(Status IN ('Present', 'Absent', 'Late', 'Excused')),
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) ON DELETE CASCADE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE
);

-- =========================================================================================
-- [PART 2] ROBUST DATA INSERTION
-- =========================================================================================

-- 1. INSERT STAFF (Hierarchy: Principal -> HOD -> Teacher)
INSERT INTO Staff (First_Name, Last_Name, Email, Designation, Hire_Date, Street_Address, City, Zip_Code) VALUES
('Albus', 'Dumbledore', 'head@school.edu', 'Principal', '1990-01-01', '1 Main St', 'London', 'SW1A'),
('Minerva', 'McGonagall', 'deputy@school.edu', 'Vice Principal', '1995-08-15', '2 Tower Ln', 'Edinburgh', 'EH1'),
('Severus', 'Snape', 'snape@school.edu', 'HOD', '2000-09-01', 'Spinners End', 'Cokeworth', 'CK1'),
('Pomona', 'Sprout', 'sprout@school.edu', 'HOD', '1998-05-20', 'Greenhouse 3', 'Hogsmeade', 'HM3'),
('Filius', 'Flitwick', 'flit@school.edu', 'HOD', '1999-02-14', 'Ravenclaw Tower', 'Hogsmeade', 'HM4'),
('Remus', 'Lupin', 'lupin@school.edu', 'Teacher', '2010-09-01', 'Grimmauld Place', 'London', 'N1'),
('Rubeus', 'Hagrid', 'hagrid@school.edu', 'Lab Assistant', '1985-06-30', 'The Hut', 'Grounds', 'GR1'),
('Sybil', 'Trelawney', 'sybil@school.edu', 'Teacher', '2005-01-10', 'North Tower', 'Hogsmeade', 'HM5'),
('Gilderoy', 'Lockhart', 'lockhart@school.edu', 'Teacher', '2012-09-01', 'Bookstore Ln', 'Diagon Alley', 'DA1'),
('Horace', 'Slughorn', 'slug@school.edu', 'Teacher', '2015-09-01', 'Manor House', 'Wiltshire', 'WL1');

-- 2. STAFF PHONES (Multi-valued)
INSERT INTO Staff_Phone (Staff_ID, Phone_Number, Type) VALUES
(1, '555-0001', 'Work'), (1, '555-9999', 'Mobile'),
(3, '555-0003', 'Mobile'),
(6, '555-1234', 'Mobile'), (6, '555-5678', 'Home');

-- 3. STAFF QUALIFICATIONS (Multi-valued)
INSERT INTO Staff_Qualification (Staff_ID, Degree, Institution, Year_Obtained) VALUES
(1, 'PhD Magic', 'Oxford', 1980), (1, 'MSc Alchemy', 'Cambridge', 1975),
(3, 'MSc Potions', 'Hogwarts', 1995),
(6, 'BEd Defense', 'Hogwarts', 2005);

-- 4. DEPARTMENTS
INSERT INTO Department (Name, HOD_Staff_ID, Office_Location) VALUES
('Potions', 3, 'Dungeon 5'),
('Herbology', 4, 'Greenhouse 1'),
('Charms', 5, 'West Tower 3'),
('Defense Against Dark Arts', 2, 'Classroom 3C');

-- 5. STUDENTS (Generating diverse data)
INSERT INTO Student (First_Name, Last_Name, DOB, Email, Street_Address, City, Zip_Code, Enrollment_Year) VALUES
('Harry', 'Potter', '2005-07-31', 'harry@std.edu', '4 Privet Dr', 'Little Whinging', 'LW1', 2023),
('Hermione', 'Granger', '2005-09-19', 'hermione@std.edu', '8 Heathgate', 'London', 'NW11', 2023),
('Ron', 'Weasley', '2005-03-01', 'ron@std.edu', 'The Burrow', 'Ottery', 'OT1', 2023),
('Draco', 'Malfoy', '2005-06-05', 'draco@std.edu', 'Malfoy Manor', 'Wiltshire', 'WL2', 2023),
('Luna', 'Lovegood', '2006-02-13', 'luna@std.edu', 'The Rookery', 'Ottery', 'OT2', 2024),
('Neville', 'Longbottom', '2005-07-30', 'neville@std.edu', 'Gran Home', 'Liverpool', 'LV1', 2023),
('Ginny', 'Weasley', '2006-08-11', 'ginny@std.edu', 'The Burrow', 'Ottery', 'OT1', 2024),
('Fred', 'Weasley', '2003-04-01', 'fred@std.edu', 'Diagon Alley', 'London', 'DA2', 2021),
('George', 'Weasley', '2003-04-01', 'george@std.edu', 'Diagon Alley', 'London', 'DA2', 2021),
('Cho', 'Chang', '2004-10-15', 'cho@std.edu', 'High St', 'London', 'LD1', 2022),
('Cedric', 'Diggory', '2003-09-20', 'cedric@std.edu', 'Badger Ln', 'Hufflepuff', 'HF1', 2021),
('Pansy', 'Parkinson', '2005-11-10', 'pansy@std.edu', 'Slytherin House', 'Hogwarts', 'HG1', 2023),
('Dean', 'Thomas', '2005-12-05', 'dean@std.edu', 'West Ham', 'London', 'WH1', 2023),
('Seamus', 'Finnigan', '2005-01-25', 'seamus@std.edu', 'Kenmare', 'Ireland', 'IR1', 2023),
('Lavender', 'Brown', '2005-05-02', 'lavender@std.edu', 'East End', 'London', 'E1', 2023),
('Padma', 'Patil', '2005-08-10', 'padma@std.edu', 'Brick Ln', 'London', 'E2', 2023),
('Parvati', 'Patil', '2005-08-10', 'parvati@std.edu', 'Brick Ln', 'London', 'E2', 2023),
('Colin', 'Creevey', '2006-06-01', 'colin@std.edu', 'Milkman Row', 'London', 'MR1', 2024),
('Gregory', 'Goyle', '2005-04-20', 'goyle@std.edu', 'Dark Alley', 'Knockturn', 'KT1', 2023),
('Vincent', 'Crabbe', '2005-05-25', 'crabbe@std.edu', 'Dark Alley', 'Knockturn', 'KT1', 2023);

-- 6. STUDENT GUARDIANS (Weak Entity)
INSERT INTO Guardian (Student_ID, First_Name, Last_Name, Relationship, Phone_Number, Email) VALUES
(1, 'Vernon', 'Dursley', 'Guardian', '555-4444', 'vernon@drill.com'),
(2, 'Monica', 'Granger', 'Mother', '555-5555', 'monica@dental.com'),
(3, 'Molly', 'Weasley', 'Mother', '555-6666', 'molly@home.com'),
(4, 'Lucius', 'Malfoy', 'Father', '555-7777', 'lucius@ministry.com');

-- 7. CLASSROOMS
INSERT INTO Classroom (Room_Number, Capacity, Type, Building) VALUES
('DUN-001', 40, 'Lab', 'Dungeons'),
('GRN-001', 30, 'Lab', 'Greenhouses'),
('TWR-101', 50, 'Lecture Hall', 'West Tower'),
('DAT-303', 40, 'Seminar Room', 'Main Castle');

-- 8. COURSES
INSERT INTO Course (Code, Title, Credits, Dept_ID) VALUES
('POT101', 'Intro to Potions', 4, 1),
('POT201', 'Advanced Brewing', 4, 1),
('HER101', 'Basic Herbology', 3, 2),
('CHM101', 'Charms Theory', 3, 3),
('DAD101', 'Defense Basics', 4, 4);

-- 9. CLASSES (Scheduled Instances)
INSERT INTO Class (Course_ID, Section, Semester, Teacher_ID) VALUES
(1, 'A', 'Fall 2025', 3), -- Potions A (Snape)
(1, 'B', 'Fall 2025', 10), -- Potions B (Slughorn)
(2, 'A', 'Fall 2025', 3), -- Adv Potions
(3, 'A', 'Fall 2025', 4), -- Herbology
(5, 'A', 'Fall 2025', 6); -- Defense (Lupin)

-- 10. ENROLLMENTS
-- Harry, Ron, Hermione take Potions A, Herbology, Defense
INSERT INTO Enrollment (Student_ID, Class_ID) VALUES 
(1, 1), (1, 4), (1, 5),
(2, 1), (2, 4), (2, 5),
(3, 1), (3, 4), (3, 5);

-- Draco takes Potions A and Defense
INSERT INTO Enrollment (Student_ID, Class_ID) VALUES (4, 1), (4, 5);

-- Luna and Ginny take Herbology
INSERT INTO Enrollment (Student_ID, Class_ID) VALUES (5, 4), (7, 4);

-- 11. SCHEDULE
INSERT INTO Class_Schedule (Class_ID, Room_ID, Day_of_Week, Start_Time, End_Time) VALUES
(1, 1, 'Mon', '09:00', '10:30'), -- Potions A Mon
(1, 1, 'Wed', '09:00', '10:30'), -- Potions A Wed
(5, 4, 'Tue', '14:00', '15:30'), -- Defense Tue
(4, 2, 'Fri', '10:00', '11:30'); -- Herbology Fri

-- 12. EXAMS & GRADES
INSERT INTO Exam (Class_ID, Title, Total_Marks, Weightage_Percent, Exam_Date) VALUES
(1, 'Potion Making Practical', 100, 30, '2025-10-31'),
(5, 'Boggart Banishing', 50, 20, '2025-11-15');

-- Grades for Potion Practical
INSERT INTO Grade (Exam_ID, Student_ID, Marks_Obtained, Comments) VALUES
(1, 1, 85.5, 'Good texture, slightly runny.'),
(1, 2, 100.0, 'Perfect execution.'),
(1, 3, 70.0, 'Cauldron melted.'),
(1, 4, 90.0, 'Excellent color.');

-- 13. ATTENDANCE (Batch Insert)
INSERT INTO Attendance (Class_ID, Student_ID, Date, Status) VALUES
(1, 1, '2025-09-01', 'Present'),
(1, 2, '2025-09-01', 'Present'),
(1, 3, '2025-09-01', 'Late'), -- Ron was late
(1, 4, '2025-09-01', 'Present');

-- =========================================================================================
-- END OF ROBUST SCRIPT
-- =========================================================================================