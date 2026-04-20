import sqlite3
import os

DB_NAME = 'school_management.db'

def populate_data():
    conn = sqlite3.connect(DB_NAME)
    
    # 1. Ensure Schema
    print("Checking schema...")
    try:
        conn.execute("ALTER TABLE Student ADD COLUMN Dept TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE Student ADD COLUMN Age INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE Enrollment ADD COLUMN Grade TEXT")
    except sqlite3.OperationalError:
        pass

    # 2. Clear Tables
    print("Clearing old data...")
    tables = ['Enrollment', 'Student', 'Class', 'Course', 'Department', 'Staff']
    for t in tables:
        conn.execute(f"DELETE FROM {t}")

    # 3. Insert Data
    print("Inserting new data...")
    
    # Insert initial Staff
    conn.execute("""
    INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Email, Hire_Date, Role) VALUES
    (1, 'John', 'Doe', 'john.doe@school.edu', '2020-01-01', 'Teacher'),
    (2, 'Jane', 'Smith', 'jane.smith@school.edu', '2020-01-01', 'Teacher'),
    (3, 'Bob', 'Jones', 'bob.jones@school.edu', '2020-01-01', 'Teacher'),
    (4, 'Alice', 'White', 'alice.white@school.edu', '2020-01-01', 'Teacher')
    """)
    
    # Add 11 more staff to reach 15
    extra_staff = []
    roles = ['Teacher', 'Admin', 'Support']
    for i in range(5, 16):
        extra_staff.append((i, f'StaffFn{i}', f'StaffLn{i}', f'staff{i}@school.edu', '2021-05-15', roles[i%3]))
    
    conn.executemany("INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Email, Hire_Date, Role) VALUES (?, ?, ?, ?, ?, ?)", extra_staff)

    sql_inserts = """
INSERT INTO Department (Dept_ID, Name, HOD_Staff_ID) VALUES
(1, 'CSE', 1), (2, 'ECE', 2), (3, 'MECH', 3), (4, 'CIVIL', 4);
INSERT INTO Course (Course_ID, Code, Title, Credits, Dept_ID) VALUES
(1, 'CS101', 'Intro to CS', 4, 1), (2, 'EC101', 'Intro to Electronics', 4, 2),
(3, 'ME101', 'Thermodynamics', 4, 3), (4, 'CV101', 'Structural Eng', 4, 4);
INSERT INTO Class (Class_ID, Course_ID, Section, Semester, Teacher_ID) VALUES
(101, 1, 'A', 'Spring 2026', 1), (102, 2, 'A', 'Spring 2026', 2),
(103, 3, 'A', 'Spring 2026', 3), (104, 4, 'A', 'Spring 2026', 4);
INSERT INTO Student (Student_ID, First_Name, Last_Name, DOB, Email, Enrollment_Year, City, Dept, Age) VALUES
(1, 'Aarav', 'Sharma', '2000-01-01', 'aarav.sharma1@example.com', 2023, 'Los Angeles', 'ECE', 22),
(2, 'Aditi', 'Verma', '2000-01-01', 'aditi.verma2@example.com', 2023, 'Chicago', 'MECH', 22),
(3, 'Akash', 'Gupta', '2000-01-01', 'akash.gupta3@example.com', 2023, 'Houston', 'CIVIL', 19),
(4, 'Ananya', 'Malhotra', '2000-01-01', 'ananya.malhotra4@example.com', 2023, 'Phoenix', 'CSE', 18),
(5, 'Arjun', 'Bhatia', '2000-01-01', 'arjun.bhatia5@example.com', 2023, 'New York', 'ECE', 21),
(6, 'Bhavya', 'Saxena', '2000-01-01', 'bhavya.saxena6@example.com', 2023, 'Los Angeles', 'MECH', 21),
(7, 'Chaitanya', 'Mehta', '2000-01-01', 'chaitanya.mehta7@example.com', 2023, 'Chicago', 'CIVIL', 21),
(8, 'Deepak', 'Chopra', '2000-01-01', 'deepak.chopra8@example.com', 2023, 'Houston', 'CSE', 18),
(9, 'Divya', 'Desai', '2000-01-01', 'divya.desai9@example.com', 2023, 'Phoenix', 'ECE', 19),
(10, 'Eshaan', 'Joshi', '2000-01-01', 'eshaan.joshi10@example.com', 2023, 'New York', 'MECH', 19),
(11, 'Faisal', 'Sharma', '2000-01-01', 'faisal.sharma11@example.com', 2023, 'Los Angeles', 'CIVIL', 22),
(12, 'Gaurav', 'Verma', '2000-01-01', 'gaurav.verma12@example.com', 2023, 'Chicago', 'CSE', 18),
(13, 'Hari', 'Gupta', '2000-01-01', 'hari.gupta13@example.com', 2023, 'Houston', 'ECE', 22),
(14, 'Isha', 'Malhotra', '2000-01-01', 'isha.malhotra14@example.com', 2023, 'Phoenix', 'MECH', 19),
(15, 'Jatin', 'Bhatia', '2000-01-01', 'jatin.bhatia15@example.com', 2023, 'New York', 'CIVIL', 20),
(16, 'Karthik', 'Saxena', '2000-01-01', 'karthik.saxena16@example.com', 2023, 'Los Angeles', 'CSE', 22),
(17, 'Kavya', 'Mehta', '2000-01-01', 'kavya.mehta17@example.com', 2023, 'Chicago', 'ECE', 20),
(18, 'Laksh', 'Chopra', '2000-01-01', 'laksh.chopra18@example.com', 2023, 'Houston', 'MECH', 18),
(19, 'Madhav', 'Desai', '2000-01-01', 'madhav.desai19@example.com', 2023, 'Phoenix', 'CIVIL', 18),
(20, 'Neha', 'Joshi', '2000-01-01', 'neha.joshi20@example.com', 2023, 'New York', 'CSE', 18),
(21, 'Omkar', 'Sharma', '2000-01-01', 'omkar.sharma21@example.com', 2023, 'Los Angeles', 'ECE', 19),
(22, 'Pooja', 'Verma', '2000-01-01', 'pooja.verma22@example.com', 2023, 'Chicago', 'MECH', 21),
(23, 'Pranav', 'Gupta', '2000-01-01', 'pranav.gupta23@example.com', 2023, 'Houston', 'CIVIL', 19),
(24, 'Rahul', 'Malhotra', '2000-01-01', 'rahul.malhotra24@example.com', 2023, 'Phoenix', 'CSE', 21),
(25, 'Riya', 'Bhatia', '2000-01-01', 'riya.bhatia25@example.com', 2023, 'New York', 'ECE', 19),
(26, 'Rohan', 'Saxena', '2000-01-01', 'rohan.saxena26@example.com', 2023, 'Los Angeles', 'MECH', 22),
(27, 'Sagar', 'Mehta', '2000-01-01', 'sagar.mehta27@example.com', 2023, 'Chicago', 'CIVIL', 20),
(28, 'Sakshi', 'Chopra', '2000-01-01', 'sakshi.chopra28@example.com', 2023, 'Houston', 'CSE', 20),
(29, 'Sameer', 'Desai', '2000-01-01', 'sameer.desai29@example.com', 2023, 'Phoenix', 'ECE', 21),
(30, 'Sanjay', 'Joshi', '2000-01-01', 'sanjay.joshi30@example.com', 2023, 'New York', 'MECH', 19),
(31, 'Shreya', 'Sharma', '2000-01-01', 'shreya.sharma31@example.com', 2023, 'Los Angeles', 'CIVIL', 22),
(32, 'Siddharth', 'Verma', '2000-01-01', 'siddharth.verma32@example.com', 2023, 'Chicago', 'CSE', 21),
(33, 'Sneha', 'Gupta', '2000-01-01', 'sneha.gupta33@example.com', 2023, 'Houston', 'ECE', 20),
(34, 'Suraj', 'Malhotra', '2000-01-01', 'suraj.malhotra34@example.com', 2023, 'Phoenix', 'MECH', 19),
(35, 'Swati', 'Bhatia', '2000-01-01', 'swati.bhatia35@example.com', 2023, 'New York', 'CIVIL', 18),
(36, 'Tarun', 'Saxena', '2000-01-01', 'tarun.saxena36@example.com', 2023, 'Los Angeles', 'CSE', 19),
(37, 'Tejas', 'Mehta', '2000-01-01', 'tejas.mehta37@example.com', 2023, 'Chicago', 'ECE', 20),
(38, 'Utkarsh', 'Chopra', '2000-01-01', 'utkarsh.chopra38@example.com', 2023, 'Houston', 'MECH', 22),
(39, 'Vaishnavi', 'Desai', '2000-01-01', 'vaishnavi.desai39@example.com', 2023, 'Phoenix', 'CIVIL', 21),
(40, 'Varun', 'Joshi', '2000-01-01', 'varun.joshi40@example.com', 2023, 'New York', 'CSE', 22),
(41, 'Vedant', 'Sharma', '2000-01-01', 'vedant.sharma41@example.com', 2023, 'Los Angeles', 'ECE', 22),
(42, 'Vidya', 'Verma', '2000-01-01', 'vidya.verma42@example.com', 2023, 'Chicago', 'MECH', 21),
(43, 'Vikas', 'Gupta', '2000-01-01', 'vikas.gupta43@example.com', 2023, 'Houston', 'CIVIL', 22),
(44, 'Vinay', 'Malhotra', '2000-01-01', 'vinay.malhotra44@example.com', 2023, 'Phoenix', 'CSE', 20),
(45, 'Yash', 'Bhatia', '2000-01-01', 'yash.bhatia45@example.com', 2023, 'New York', 'ECE', 19),
(46, 'Zara', 'Saxena', '2000-01-01', 'zara.saxena46@example.com', 2023, 'Los Angeles', 'MECH', 19),
(47, 'Abhinav', 'Mehta', '2000-01-01', 'abhinav.mehta47@example.com', 2023, 'Chicago', 'CIVIL', 19),
(48, 'Ashwin', 'Chopra', '2000-01-01', 'ashwin.chopra48@example.com', 2023, 'Houston', 'CSE', 20),
(49, 'Bharat', 'Desai', '2000-01-01', 'bharat.desai49@example.com', 2023, 'Phoenix', 'ECE', 19),
(50, 'Chetan', 'Joshi', '2000-01-01', 'chetan.joshi50@example.com', 2023, 'New York', 'MECH', 18),
(51, 'Darshan', 'Sharma', '2000-01-01', 'darshan.sharma51@example.com', 2023, 'Los Angeles', 'CIVIL', 21),
(52, 'Ekta', 'Verma', '2000-01-01', 'ekta.verma52@example.com', 2023, 'Chicago', 'CSE', 18),
(53, 'Farhan', 'Gupta', '2000-01-01', 'farhan.gupta53@example.com', 2023, 'Houston', 'ECE', 20),
(54, 'Gagan', 'Malhotra', '2000-01-01', 'gagan.malhotra54@example.com', 2023, 'Phoenix', 'MECH', 20),
(55, 'Harsh', 'Bhatia', '2000-01-01', 'harsh.bhatia55@example.com', 2023, 'New York', 'CIVIL', 22),
(56, 'Imran', 'Saxena', '2000-01-01', 'imran.saxena56@example.com', 2023, 'Los Angeles', 'CSE', 21),
(57, 'Jay', 'Mehta', '2000-01-01', 'jay.mehta57@example.com', 2023, 'Chicago', 'ECE', 22),
(58, 'Karan', 'Chopra', '2000-01-01', 'karan.chopra58@example.com', 2023, 'Houston', 'MECH', 22),
(59, 'Lalit', 'Desai', '2000-01-01', 'lalit.desai59@example.com', 2023, 'Phoenix', 'CIVIL', 19),
(60, 'Manish', 'Joshi', '2000-01-01', 'manish.joshi60@example.com', 2023, 'New York', 'CSE', 20),
(61, 'Naman', 'Sharma', '2000-01-01', 'naman.sharma61@example.com', 2023, 'Los Angeles', 'ECE', 22),
(62, 'Nitin', 'Verma', '2000-01-01', 'nitin.verma62@example.com', 2023, 'Chicago', 'MECH', 20),
(63, 'Ojas', 'Gupta', '2000-01-01', 'ojas.gupta63@example.com', 2023, 'Houston', 'CIVIL', 19),
(64, 'Pallavi', 'Malhotra', '2000-01-01', 'pallavi.malhotra64@example.com', 2023, 'Phoenix', 'CSE', 22),
(65, 'Piyush', 'Bhatia', '2000-01-01', 'piyush.bhatia65@example.com', 2023, 'New York', 'ECE', 20),
(66, 'Puneet', 'Saxena', '2000-01-01', 'puneet.saxena66@example.com', 2023, 'Los Angeles', 'MECH', 22),
(67, 'Rajat', 'Mehta', '2000-01-01', 'rajat.mehta67@example.com', 2023, 'Chicago', 'CIVIL', 19),
(68, 'Rajeev', 'Chopra', '2000-01-01', 'rajeev.chopra68@example.com', 2023, 'Houston', 'CSE', 21),
(69, 'Rakesh', 'Desai', '2000-01-01', 'rakesh.desai69@example.com', 2023, 'Phoenix', 'ECE', 22),
(70, 'Ramesh', 'Joshi', '2000-01-01', 'ramesh.joshi70@example.com', 2023, 'New York', 'MECH', 21),
(71, 'Ravi', 'Sharma', '2000-01-01', 'ravi.sharma71@example.com', 2023, 'Los Angeles', 'CIVIL', 20),
(72, 'Rishabh', 'Verma', '2000-01-01', 'rishabh.verma72@example.com', 2023, 'Chicago', 'CSE', 20),
(73, 'Rohan', 'Gupta', '2000-01-01', 'rohan.gupta73@example.com', 2023, 'Houston', 'ECE', 22),
(74, 'Rohit', 'Malhotra', '2000-01-01', 'rohit.malhotra74@example.com', 2023, 'Phoenix', 'MECH', 19),
(75, 'Sahil', 'Bhatia', '2000-01-01', 'sahil.bhatia75@example.com', 2023, 'New York', 'CIVIL', 18),
(76, 'Sandeep', 'Saxena', '2000-01-01', 'sandeep.saxena76@example.com', 2023, 'Los Angeles', 'CSE', 22),
(77, 'Saurabh', 'Mehta', '2000-01-01', 'saurabh.mehta77@example.com', 2023, 'Chicago', 'ECE', 21),
(78, 'Shivam', 'Chopra', '2000-01-01', 'shivam.chopra78@example.com', 2023, 'Houston', 'MECH', 19),
(79, 'Shubham', 'Desai', '2000-01-01', 'shubham.desai79@example.com', 2023, 'Phoenix', 'CIVIL', 18),
(80, 'Sumit', 'Joshi', '2000-01-01', 'sumit.joshi80@example.com', 2023, 'New York', 'CSE', 20),
(81, 'Sunil', 'Sharma', '2000-01-01', 'sunil.sharma81@example.com', 2023, 'Los Angeles', 'ECE', 18),
(82, 'Suresh', 'Verma', '2000-01-01', 'suresh.verma82@example.com', 2023, 'Chicago', 'MECH', 22),
(83, 'Tanmay', 'Gupta', '2000-01-01', 'tanmay.gupta83@example.com', 2023, 'Houston', 'CIVIL', 18),
(84, 'Tushar', 'Malhotra', '2000-01-01', 'tushar.malhotra84@example.com', 2023, 'Phoenix', 'CSE', 19),
(85, 'Udit', 'Bhatia', '2000-01-01', 'udit.bhatia85@example.com', 2023, 'New York', 'ECE', 18),
(86, 'Vaibhav', 'Saxena', '2000-01-01', 'vaibhav.saxena86@example.com', 2023, 'Los Angeles', 'MECH', 20),
(87, 'Varun', 'Mehta', '2000-01-01', 'varun.mehta87@example.com', 2023, 'Chicago', 'CIVIL', 18),
(88, 'Vasant', 'Chopra', '2000-01-01', 'vasant.chopra88@example.com', 2023, 'Houston', 'CSE', 19),
(89, 'Vijay', 'Desai', '2000-01-01', 'vijay.desai89@example.com', 2023, 'Phoenix', 'ECE', 19),
(90, 'Vikram', 'Joshi', '2000-01-01', 'vikram.joshi90@example.com', 2023, 'New York', 'MECH', 19),
(91, 'Vimal', 'Sharma', '2000-01-01', 'vimal.sharma91@example.com', 2023, 'Los Angeles', 'CIVIL', 22),
(92, 'Vineet', 'Verma', '2000-01-01', 'vineet.verma92@example.com', 2023, 'Chicago', 'CSE', 19),
(93, 'Vipin', 'Gupta', '2000-01-01', 'vipin.gupta93@example.com', 2023, 'Houston', 'ECE', 18),
(94, 'Vishal', 'Malhotra', '2000-01-01', 'vishal.malhotra94@example.com', 2023, 'Phoenix', 'MECH', 21),
(95, 'Vivek', 'Bhatia', '2000-01-01', 'vivek.bhatia95@example.com', 2023, 'New York', 'CIVIL', 19),
(96, 'Yash', 'Saxena', '2000-01-01', 'yash.saxena96@example.com', 2023, 'Los Angeles', 'CSE', 21),
(97, 'Yogesh', 'Mehta', '2000-01-01', 'yogesh.mehta97@example.com', 2023, 'Chicago', 'ECE', 18),
(98, 'Zaid', 'Chopra', '2000-01-01', 'zaid.chopra98@example.com', 2023, 'Houston', 'MECH', 22),
(99, 'Zane', 'Desai', '2000-01-01', 'zane.desai99@example.com', 2023, 'Phoenix', 'CIVIL', 20),
(100, 'Zoya', 'Joshi', '2000-01-01', 'zoya.joshi100@example.com', 2023, 'New York', 'CSE', 18);
INSERT INTO Enrollment (Student_ID, Class_ID, Grade) VALUES
(1, 102, 'S'),
(2, 103, 'A'),
(3, 104, 'S'),
(4, 101, 'B'),
(5, 102, 'C'),
(6, 103, 'C'),
(7, 104, 'C'),
(8, 101, 'D'),
(9, 102, 'S'),
(10, 103, 'D'),
(11, 104, 'D'),
(12, 101, 'C'),
(13, 102, 'C'),
(14, 103, 'F'),
(15, 104, 'C'),
(16, 101, 'F'),
(17, 102, 'D'),
(18, 103, 'S'),
(19, 104, 'C'),
(20, 101, 'D'),
(21, 102, 'F'),
(22, 103, 'A'),
(23, 104, 'A'),
(24, 101, 'A'),
(25, 102, 'F'),
(26, 103, 'B'),
(27, 104, 'B'),
(28, 101, 'C'),
(29, 102, 'F'),
(30, 103, 'S'),
(31, 104, 'A'),
(32, 101, 'S'),
(33, 102, 'F'),
(34, 103, 'D'),
(35, 104, 'D'),
(36, 101, 'B'),
(37, 102, 'D'),
(38, 103, 'D'),
(39, 104, 'S'),
(40, 101, 'F'),
(41, 102, 'B'),
(42, 103, 'D'),
(43, 104, 'D'),
(44, 101, 'A'),
(45, 102, 'F'),
(46, 103, 'C'),
(47, 104, 'D'),
(48, 101, 'B'),
(49, 102, 'B'),
(50, 103, 'F'),
(51, 104, 'S'),
(52, 101, 'A'),
(53, 102, 'A'),
(54, 103, 'C'),
(55, 104, 'D'),
(56, 101, 'S'),
(57, 102, 'A'),
(58, 103, 'S'),
(59, 104, 'D'),
(60, 101, 'S'),
(61, 102, 'F'),
(62, 103, 'F'),
(63, 104, 'S'),
(64, 101, 'C'),
(65, 102, 'D'),
(66, 103, 'F'),
(67, 104, 'C'),
(68, 101, 'B'),
(69, 102, 'F'),
(70, 103, 'A'),
(71, 104, 'B'),
(72, 101, 'A'),
(73, 102, 'S'),
(74, 103, 'D'),
(75, 104, 'S'),
(76, 101, 'C'),
(77, 102, 'A'),
(78, 103, 'F'),
(79, 104, 'B'),
(80, 101, 'C'),
(81, 102, 'A'),
(82, 103, 'S'),
(83, 104, 'D'),
(84, 101, 'F'),
(85, 102, 'A'),
(86, 103, 'C'),
(87, 104, 'B'),
(88, 101, 'D'),
(89, 102, 'S'),
(90, 103, 'A'),
(91, 104, 'B'),
(92, 101, 'B'),
(93, 102, 'D'),
(94, 103, 'D'),
(95, 104, 'B'),
(96, 101, 'F'),
(97, 102, 'A'),
(98, 103, 'B'),
(99, 104, 'A'),
(100, 101, 'C');
    """
    
    conn.executescript(sql_inserts)
    conn.commit()
    conn.close()
    print("Data populated for review demo.")

if __name__ == '__main__':
    populate_data()
