
def apply_changes():
    # Read the generated queries content
    # I'll rely on generating it again within this script to be self-contained and accurate
    # copying the logic from generate_queries_content.py but returning string instead of printing
    import random
    
    departments = ['CSE', 'ECE', 'MECH', 'CIVIL']
    class_ids = {'CSE': 101, 'ECE': 102, 'MECH': 103, 'CIVIL': 104}
    
    setup_sql = []
    setup_sql.append("DELETE FROM Enrollment;")
    setup_sql.append("DELETE FROM Student;")
    setup_sql.append("DELETE FROM Class;")
    setup_sql.append("DELETE FROM Course;")
    setup_sql.append("DELETE FROM Department;")
    setup_sql.append("DELETE FROM Staff;")
    setup_sql.append("-- Note: The following ALTER statements may fail if columns already exist. This is expected.")
    setup_sql.append("ALTER TABLE Student ADD COLUMN Dept TEXT;")
    setup_sql.append("ALTER TABLE Student ADD COLUMN Age INTEGER;")
    setup_sql.append("ALTER TABLE Enrollment ADD COLUMN Grade TEXT;")
    
    setup_sql.append("INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Email, Hire_Date, Role) VALUES")
    setup_sql.append("(1, 'John', 'Doe', 'john.doe@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(2, 'Jane', 'Smith', 'jane.smith@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(3, 'Bob', 'Jones', 'bob.jones@school.edu', '2020-01-01', 'Teacher'),")
    setup_sql.append("(4, 'Alice', 'White', 'alice.white@school.edu', '2020-01-01', 'Teacher');")
    
    setup_sql.append("INSERT INTO Department (Dept_ID, Name, HOD_Staff_ID) VALUES")
    setup_sql.append("(1, 'CSE', 1), (2, 'ECE', 2), (3, 'MECH', 3), (4, 'CIVIL', 4);")
    
    setup_sql.append("INSERT INTO Course (Course_ID, Code, Title, Credits, Dept_ID) VALUES")
    setup_sql.append("(1, 'CS101', 'Intro to CS', 4, 1), (2, 'EC101', 'Intro to Electronics', 4, 2),")
    setup_sql.append("(3, 'ME101', 'Thermodynamics', 4, 3), (4, 'CV101', 'Structural Eng', 4, 4);")
    
    setup_sql.append("INSERT INTO Class (Class_ID, Course_ID, Section, Semester, Teacher_ID) VALUES")
    setup_sql.append("(101, 1, 'A', 'Spring 2026', 1), (102, 2, 'A', 'Spring 2026', 2),")
    setup_sql.append("(103, 3, 'A', 'Spring 2026', 3), (104, 4, 'A', 'Spring 2026', 4);")
    
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
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]

    student_values = []
    enrollment_values = []
    
    for i in range(1, 101):
        sid = i
        fname = first_names[(i-1) % len(first_names)]
        lname = last_names[(i-1) % len(last_names)]
        email = f"{fname.lower()}.{lname.lower()}{i}@example.com"
        dob = "2000-01-01"
        enrollment_year = 2023
        city = cities[i % len(cities)]
        dept = departments[i % 4] 
        age = random.randint(18, 22)
        
        student_values.append(f"({sid}, '{fname}', '{lname}', '{dob}', '{email}', {enrollment_year}, '{city}', '{dept}', {age})")
        cid = class_ids[dept]
        grade = random.choice(['S', 'A', 'B', 'C', 'D', 'F'])
        enrollment_values.append(f"({sid}, {cid}, '{grade}')")

    setup_sql.append(",\n".join(student_values) + ";")
    setup_sql.append("INSERT INTO Enrollment (Student_ID, Class_ID, Grade) VALUES")
    setup_sql.append(",\n".join(enrollment_values) + ";")
    
    setup_query = "\n".join(setup_sql)

    aggregates_query = "SELECT Dept, COUNT(Student_ID) as Total_Students, AVG(Age) as Avg_Age FROM Student GROUP BY Dept;"
    union_query = "SELECT First_Name FROM Student WHERE Dept = 'CSE' UNION SELECT First_Name FROM Student WHERE Dept = 'ECE';"
    subquery_query = "SELECT First_Name, Age FROM Student WHERE Age = (SELECT MIN(Age) FROM Student);"
    joins_query = "SELECT S.First_Name, E.Grade FROM Student S INNER JOIN Enrollment E ON S.Student_ID = E.Student_ID;"
    create_view_query = "CREATE VIEW IF NOT EXISTS CSE_STUDENTS AS SELECT First_Name, Age FROM Student WHERE Dept = 'CSE';"
    select_view_query = "SELECT * FROM CSE_STUDENTS;"

    # Construct the new queries block
    new_queries_block = "        const queries = {\n"
    new_queries_block += f"            setup: `{setup_query}`,\n"
    new_queries_block += f"            aggregates: `{aggregates_query}`,\n"
    new_queries_block += f"            union: `{union_query}`,\n"
    new_queries_block += f"            subquery: `{subquery_query}`,\n"
    new_queries_block += f"            joins: `{joins_query}`,\n"
    new_queries_block += f"            create_view: `{create_view_query}`,\n"
    new_queries_block += f"            select_view: `{select_view_query}`\n"
    new_queries_block += "        };"

    # Read the file
    file_path = r'c:\Users\zanya\SQL\templates\db_review.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex or String find to replace
    # We look for "const queries = {" and the matching "};"
    import re
    # Match const queries = { ... }; non-greedy dot
    # Be careful with nested braces if any, but our object is simple string properties
    pattern = re.compile(r'const queries = \{.*?\};', re.DOTALL)
    
    # Check if we find it
    match = pattern.search(content)
    if match:
        # We need to make sure indentation is correct for the replacement
        # The new_queries_block has 8 spaces indent
        # The match in the file might have '        const queries = ...'
        # We should replace the whole matched string.
        # But 'match' result includes the text.
        
        # Verify if the indent in file matches what we expect
        start_idx = match.start()
        # Look backwards to see indentation? No need, we dictate indentation in new block.
        # Just replace the match.
        
        new_content = content[:start_idx] + new_queries_block.strip() + content[match.end():]
        # Note: .strip() on new_queries_block means we lose leading indentation if not careful.
        # But new_queries_block starts with spaces. .strip() would remove them.
        # We should NOT strip, or we should handle it.
        # Let's adjust new_queries_block to not have leading newline if any.
        
        # Wait, the regex `const queries = \{` will match starting at `const`.
        # It won't match the whitespace before it.
        # So `content[:start_idx]` will end with whitespace (e.g. `    `).
        # If `new_queries_block` also has whitespace, we duplicate it.
        # In the file:
        # `    <script>`
        # `        const queries = {`
        # If regex matches `const queries...`, then `content[:start_idx]` ends with `        `.
        # So `new_queries_block` should NOT have indentation on the first line.
        
        # Le's fix `new_queries_block`.
        new_queries_block_fixed = "const queries = {\n"
        new_queries_block_fixed += f"            setup: `{setup_query}`,\n"
        new_queries_block_fixed += f"            aggregates: `{aggregates_query}`,\n"
        new_queries_block_fixed += f"            union: `{union_query}`,\n"
        new_queries_block_fixed += f"            subquery: `{subquery_query}`,\n"
        new_queries_block_fixed += f"            joins: `{joins_query}`,\n"
        new_queries_block_fixed += f"            create_view: `{create_view_query}`,\n"
        new_queries_block_fixed += f"            select_view: `{select_view_query}`\n"
        new_queries_block_fixed += "        };"
        
        new_content = content[:start_idx] + new_queries_block_fixed + content[match.end():]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated db_review.html")
    else:
        print("Could not find queries block in db_review.html")

if __name__ == "__main__":
    apply_changes()
