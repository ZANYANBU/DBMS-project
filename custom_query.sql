-- 1. Create Exams for the missing subjects
INSERT INTO Exam (Title, Max_Marks, Date, Class_ID) VALUES
('Python Final Project', 100, '2024-05-20', 9),   -- Intro to Python
('Web Dev Portfolio', 50, '2024-05-22', 11),       -- Web Dev
('Shakespeare Essay', 100, '2024-04-10', 13),      -- Shakespeare
('Organic Chem Lab', 50, '2024-03-15', 7),         -- Chemistry I
('Oil Painting Final', 100, '2024-06-01', 18),     -- Painting
('100m Dash Time Trial', 10, '2024-05-05', 20);    -- Athletics

-- 2. Populate Grades for 'Intro to Python' (Students 21-40)
INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID) VALUES
(88, 'B+', 21, 3), (92, 'A', 22, 3), (75, 'C', 23, 3), (60, 'D', 24, 3), (95, 'A', 25, 3),
(82, 'B', 26, 3), (91, 'A', 27, 3), (79, 'C+', 28, 3), (65, 'D', 29, 3), (98, 'A+', 30, 3),
(55, 'F', 31, 3), (89, 'B+', 32, 3), (77, 'C+', 33, 3), (62, 'D', 34, 3), (93, 'A', 35, 3),
(85, 'B', 36, 3), (90, 'A-', 37, 3), (74, 'C', 38, 3), (68, 'D+', 39, 3), (99, 'A+', 40, 3);

-- 3. Populate Grades for 'Shakespeare' (Students 61-80)
INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID) VALUES
(78, 'C+', 61, 5), (85, 'B', 62, 5), (92, 'A-', 63, 5), (88, 'B+', 64, 5), (70, 'C-', 65, 5),
(95, 'A', 66, 5), (81, 'B-', 67, 5), (76, 'C', 68, 5), (84, 'B', 69, 5), (90, 'A-', 70, 5),
(65, 'D', 71, 5), (98, 'A+', 72, 5), (72, 'C-', 73, 5), (83, 'B', 74, 5), (79, 'C+', 75, 5),
(88, 'B+', 76, 5), (91, 'A', 77, 5), (60, 'D-', 78, 5), (85, 'B', 79, 5), (94, 'A', 80, 5);

-- 4. Populate Grades for 'Chemistry I' (Students 1-20)
-- Note: These students already have Physics grades, now they get Chem grades too!
INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID) VALUES
(45, 'A', 1, 6), (42, 'B', 2, 6), (38, 'C', 3, 6), (48, 'A+', 4, 6), (40, 'B', 5, 6),
(35, 'C', 6, 6), (49, 'A+', 7, 6), (44, 'A', 8, 6), (30, 'D', 9, 6), (46, 'A', 10, 6),
(41, 'B', 11, 6), (39, 'C+', 12, 6), (47, 'A', 13, 6), (43, 'B+', 14, 6), (33, 'D', 15, 6),
(50, 'A+', 16, 6), (25, 'F', 17, 6), (40, 'B', 18, 6), (37, 'C', 19, 6), (45, 'A', 20, 6);

-- 5. Populate Attendance for a full week (Batch Insert)
INSERT INTO Attendance (Date, Status, Student_ID, Class_ID) VALUES
('2024-03-05', 'Present', 21, 9), ('2024-03-05', 'Present', 22, 9), ('2024-03-05', 'Absent', 23, 9),
('2024-03-05', 'Present', 61, 13), ('2024-03-05', 'Late', 62, 13), ('2024-03-05', 'Present', 63, 13),
('2024-03-06', 'Present', 1, 7), ('2024-03-06', 'Present', 2, 7), ('2024-03-06', 'Excused', 3, 7);

-- =========================================================================================
--  BATCH 6: TAMIL STUDENTS DATA INJECTION
-- =========================================================================================

-- 1. Insert Tamil Students
INSERT INTO Student (Name, Email, DOB, Address) VALUES
('Karthik Raja', 'karthik.r@std.edu', '2006-05-12', '10 Adyar, Chennai'),
('Priya Raman', 'priya.r@std.edu', '2006-08-22', '15 Mylapore, Chennai'),
('Saravanan Velu', 'sara.v@std.edu', '2005-11-05', '22 Anna Nagar, Madurai'),
('Meenakshi Sundaram', 'meena.s@std.edu', '2006-01-30', '45 TVS Road, Trichy'),
('Arun Kumar', 'arun.k@std.edu', '2005-07-14', '12 Gandhipuram, Coimbatore'),
('Divya Bharathi', 'divya.b@std.edu', '2006-03-18', '88 Salem Main Rd, Salem'),
('Balaji Krishnan', 'balaji.k@std.edu', '2005-09-09', '34 West Masi St, Madurai'),
('Anitha Lakshmi', 'anitha.l@std.edu', '2006-12-01', '56 Beach Rd, Pondicherry'),
('Muthu Vel', 'muthu.v@std.edu', '2005-04-25', '77 North St, Tirunelveli'),
('Sangeetha Ravi', 'sangeetha.r@std.edu', '2006-06-10', '90 Bypass Rd, Vellore');

-- 2. Enroll them in "Advanced Tamil Literature" (New Class)
-- First, let's create a Tamil Department and Class if they don't exist
INSERT INTO Department (Name) VALUES ('Tamil Literature');

-- Add a Teacher for Tamil
INSERT INTO Teacher (Name, Email, Specialization, Dept_ID) VALUES
('Dr. Abdul Kalam', 'kalam@school.edu', 'Tamil Poetry', (SELECT Dept_ID FROM Department WHERE Name = 'Tamil Literature'));

-- Create the Class
INSERT INTO Class (Name, Section, Academic_Year, Teacher_ID, Dept_ID) VALUES
('Tamil Classics', 'A', '2024', 
 (SELECT Teacher_ID FROM Teacher WHERE Name = 'Dr. Abdul Kalam'), 
 (SELECT Dept_ID FROM Department WHERE Name = 'Tamil Literature'));

-- 3. Enroll the new Tamil students into this class
-- (Using a subquery to find the students we just added based on email to avoid ID errors)
INSERT INTO Enrollment (Student_ID, Class_ID)
SELECT Student_ID, (SELECT Class_ID FROM Class WHERE Name = 'Tamil Classics')
FROM Student 
WHERE Email IN (
    'karthik.r@std.edu', 'priya.r@std.edu', 'sara.v@std.edu', 'meena.s@std.edu', 
    'arun.k@std.edu', 'divya.b@std.edu', 'balaji.k@std.edu', 'anitha.l@std.edu', 
    'muthu.v@std.edu', 'sangeetha.r@std.edu'
);

-- 4. Create an Exam for Tamil Class
INSERT INTO Exam (Title, Max_Marks, Date, Class_ID) VALUES
('Thirukkural Recitation', 100, '2024-07-15', (SELECT Class_ID FROM Class WHERE Name = 'Tamil Classics'));

-- 5. Give them Grades
INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID)
SELECT 95, 'A', Student_ID, (SELECT Exam_ID FROM Exam WHERE Title = 'Thirukkural Recitation') FROM Student WHERE Email = 'karthik.r@std.edu';

INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID)
SELECT 98, 'A+', Student_ID, (SELECT Exam_ID FROM Exam WHERE Title = 'Thirukkural Recitation') FROM Student WHERE Email = 'priya.r@std.edu';

INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID)
SELECT 88, 'B+', Student_ID, (SELECT Exam_ID FROM Exam WHERE Title = 'Thirukkural Recitation') FROM Student WHERE Email = 'sara.v@std.edu';

INSERT INTO Grade (Marks_Obtained, Grade_Letter, Student_ID, Exam_ID)
SELECT 92, 'A', Student_ID, (SELECT Exam_ID FROM Exam WHERE Title = 'Thirukkural Recitation') FROM Student WHERE Email = 'meena.s@std.edu';