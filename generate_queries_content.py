import random

def generate_queries():
    departments = ['CSE', 'ECE', 'MECH', 'CIVIL']
    class_ids = {
        'CSE': 101,
        'ECE': 102,
        'MECH': 103,
        'CIVIL': 104
    }
    
    # 1. Setup Query Construction
    setup_sql = []
    
    # Cleanup
    setup_sql.append("DELETE FROM Enrollment;")
    setup_sql.append("DELETE FROM Student;")
    setup_sql.append("DELETE FROM Class;")
    setup_sql.append("DELETE FROM Course;")
    setup_sql.append("DELETE FROM Department;")
    setup_sql.append("DELETE FROM Staff;")
    
    # Schema Updates (May fail if columns exist, but that's expected/accepted for now)
    # Using a workaround: We can't easily check existence in one script, so we append them.
    # Users will be instructed to ignore 'duplicate column' errors if they run setup twice.
    setup_sql.append("-- Note: The following ALTER statements may fail if columns already exist. This is expected.")
    setup_sql.append("ALTER TABLE Student ADD COLUMN Dept TEXT;")
    setup_sql.append("ALTER TABLE Student ADD COLUMN Age INTEGER;")
    setup_sql.append("ALTER TABLE Enrollment ADD COLUMN Grade TEXT;")

    # Staff Data
    setup_sql.append("INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Email, Hire_Date, Role) VALUES")
    setup_sql.append("(1, 'John', 'Doe', 'john.doe@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(2, 'Jane', 'Smith', 'jane.smith@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(3, 'Bob', 'Jones', 'bob.jones@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(4, 'Alice', 'White', 'alice.white@school.edu', '2020-01-01', 'Teacher');")

    # Department Data
    setup_sql.append("INSERT INTO Department (Dept_ID, Name, HOD_Staff_ID) VALUES")
    setup_sql.append("(1, 'CSE', 1), (2, 'ECE', 2), (3, 'MECH', 3), (4, 'CIVIL', 4);")

    # Course Data
    setup_sql.append("INSERT INTO Course (Course_ID, Code, Title, Credits, Dept_ID) VALUES")
    setup_sql.append("(1, 'CS101', 'Intro to CS', 4, 1), (2, 'EC101', 'Intro to Electronics', 4, 2),")
    setup_sql.append("(3, 'ME101', 'Thermodynamics', 4, 3), (4, 'CV101', 'Structural Eng', 4, 4);")

    # Class Data
    setup_sql.append("INSERT INTO Class (Class_ID, Course_ID, Section, Semester, Teacher_ID) VALUES")
    setup_sql.append("(101, 1, 'A', 'Spring 2026', 1), (102, 2, 'A', 'Spring 2026', 2),")
    setup_sql.append("(103, 3, 'A', 'Spring 2026', 3), (104, 4, 'A', 'Spring 2026', 4);")

    # Student Data
    setup_sql.append("INSERT INTO Student (Student_ID, First_Name, Last_Name, DOB, Email, Enrollment_Year, City, Dept, Age) VALUES")
    
    first_names = [
        "Aarav", "Aditi", "Akash", "Ananya", "Arjun", "Bhavya", "Chaitanya", "Deepak", "Divya", "Eshaan",
        "Faisal", "Gaurav", "Hari", "Isha", "Jatin", "Karthik", "Kavya", "Laksh", "Madhav", "Neha",
        "Omkar", "Pooja", "Pranav", "Rahul", "Riya", "Rohan", "Sagar", "Sakshi", "Sameer", "Sanjay",
        "Shreya", "Siddharth", "Sneha", "Suraj", "Swati", "Tarun", "Tejas", "Utkarsh", "Vaishnavi", "Varun",
        "Vedant", "Vidya", "Vikas", "Vinay", "Yash", "Zara", "Abhinav", "Ashwin", "Bharat", "Chetan",
        "Darshan", "Ekta", "Farhan", "Gagan", "Harsh", "Imran", "Jay", "Karan", "Lalit", "Manish",
        "Naman", "Nitin", "Ojas", "Pallavi", "Piyush", "Puneet", "Rajat", "Rajeev", "Rakesh", "Ramesh",
        "Ravi", "Rishabh", "Rohan", "Rohit", "Sahil", "Sandeep", "Saurabh", "Shivam", "Shubham", "Sumit",
        "Sunil", "Suresh", "Tanmay", "Tushar", "Udit", "Vaibhav", "Varun", "Vasant", "Vijay", "Vikram",
        "Vimal", "Vineet", "Vipin", "Vishal", "Vivek", "Yash", "Yogesh", "Zaid", "Zane", "Zoya"
    ]
    
    last_names = ["Sharma", "Verma", "Gupta", "Malhotra", "Bhatia", "Saxena", "Mehta", "Chopra", "Desai", "Joshi"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"] # Dummy cities for Main App req

    student_values = []
    enrollment_values = []
    
    # We need exactly 100 students
    # Loop 100 times. If names run out, reuse/cycle.
    for i in range(1, 101):
        sid = i
        fname = first_names[(i-1) % len(first_names)]
        lname = last_names[(i-1) % len(last_names)]
        email = f"{fname.lower()}.{lname.lower()}{i}@example.com"
        dob = "2000-01-01" # Dummy
        enrollment_year = 2023
        city = cities[i % len(cities)]
        
        # Consistent Randomness for Dept and Age based on index to be reproducible if needed, 
        # but random is fine.
        # Original data had specific ages/depts. I'll recreate randomness similar to original.
        dept = departments[i % 4] 
        age = random.randint(18, 22)
        
        student_values.append(f"({sid}, '{fname}', '{lname}', '{dob}', '{email}', {enrollment_year}, '{city}', '{dept}', {age})")
        
        # Enrollment
        cid = class_ids[dept] # Enroll in class matching Dept
        grade = random.choice(['S', 'A', 'B', 'C', 'D', 'F'])
        enrollment_values.append(f"({sid}, {cid}, '{grade}')")

    setup_sql.append(",\n".join(student_values) + ";")
    
    setup_sql.append("INSERT INTO Enrollment (Student_ID, Class_ID, Grade) VALUES")
    setup_sql.append(",\n".join(enrollment_values) + ";")
    
    setup_query = "\n".join(setup_sql)

    # 2. Other Queries (Updated for Schema)
    # Aggregates: Use Dept, Age (Demo cols). Use Student_ID for count.
    aggregates_query = "SELECT Dept, COUNT(Student_ID) as Total_Students, AVG(Age) as Avg_Age FROM Student GROUP BY Dept;"
    
    # Union: Use First_Name.
    union_query = "SELECT First_Name FROM Student WHERE Dept = 'CSE' UNION SELECT First_Name FROM Student WHERE Dept = 'ECE';"
    
    # Subquery: Use First_Name, Age.
    subquery_query = "SELECT First_Name, Age FROM Student WHERE Age = (SELECT MIN(Age) FROM Student);"
    
    # Joins: Use First_Name, Grade. Note: Enrollment table now has Grade column added.
    joins_query = "SELECT S.First_Name, E.Grade FROM Student S INNER JOIN Enrollment E ON S.Student_ID = E.Student_ID;"
    
    # Views: Use First_Name.
    create_view_query = "CREATE VIEW IF NOT EXISTS CSE_STUDENTS AS SELECT First_Name, Age FROM Student WHERE Dept = 'CSE';"
    select_view_query = "SELECT * FROM CSE_STUDENTS;"
    
    # Construct final JS object
    print("const queries = {")
    print(f"    setup: `{setup_query}`,\n")
    print(f"    aggregates: `{aggregates_query}`,\n")
    print(f"    union: `{union_query}`,\n")
    print(f"    subquery: `{subquery_query}`,\n")
    print(f"    joins: `{joins_query}`,\n")
    print(f"    create_view: `{create_view_query}`,\n")
    print(f"    select_view: `{select_view_query}`")
    print("};")

if __name__ == "__main__":
    generate_queries()
