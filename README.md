#  School Management System (DBMS Project)

A robust, normalized relational database system designed to manage the complex data requirements of an educational institution. This project demonstrates the implementation of a schema handling students, staff, curriculum, attendance, and grading.

##  Database Architecture

The project features a well-structured SQLite database with **3NF/BCNF normalization** ensuring data integrity and minimal redundancy.

### Key Entities & Relationships
1.  **Staff & Departments**: 
    - Handles teaching and non-teaching staff.
    - Manages department hierarchies and Head of Department (HOD) assignments (1:1 relationships).
    - Tracks staff qualifications as a multi-valued attribute.
2.  **Student Information System**:
    - Stores comprehensive student profiles.
    - Manages multi-valued attributes like phone numbers.
    - **Weak Entity Implementation**: Guardian information is linked strictly to students.
3.  **Academic Structure**:
    - **Courses**: The catalog of subjects offered.
    - **Classes**: Specific instances of courses for a given term/semester.
    - **Enrollments**: Many-to-Many relationship between Students and Classes.
4.  **Logistics**:
    - **Classrooms**: Manages room capacity and types (Lab, Lecture Hall).
    - **Timetabling**: Allocation of classes to rooms at specific times (scheduling).
5.  **Assessment**:
    - **Exams**: Linked to specific classes.
    - **Grades**: Tracks student performance in exams.
    - **Attendance**: Daily tracking with status constraints.

##  Getting Started

### Prerequisites
*   Python 3.x
*   SQLite3

### Installation

1.  **Clone the repository:**
    \\\ash
    git clone https://github.com/zanyanbu/DBMS-project.git
    cd DBMS-project
    \\\

2.  **Initialize the Database:**
    Run the initialization script to build the schema and populate initial data.
    \\\ash
    python init_db.py
    \\\

### Usage

**1. Verification:**
Check the contents of the database tables to ensure data is loaded correctly.
\\\ash
python check_contents.py
\\\

**2. Run Custom SQL Queries:**
Execute your own SQL commands defined in \custom_query.sql\.
\\\ash
python run_custom.py
\\\

**3. Interactive Shell:**
Open a direct SQL shell to query the database in real-time.
\\\ash
python interactive_shell.py
\\\
*Example shell command:*
\\\sql
SELECT * FROM Student WHERE Enrollment_Year = 2024;
\\\

**4. Generate Reports:**
Run pre-defined complex queries (joins, aggregations) to see the system in action.
\\\ash
python run_queries.py
\\\

##  Project Structure

*   \school_management.sql\: The core DDL/DML script defining the schema and relationships.
*   \init_db.py\: Python script to bootstrap the SQLite database.
*   \check_contents.py\: Utility to inspect table data.
*   \interactive_shell.py\: A CLI interface for executing raw SQL.
*   \un_queries.py\: Collection of analytical queries (e.g., student schedules, grade reports).

##  Tech Stack
*   **Database Engine**: SQLite
*   **Language**: SQL, Python
*   **Concepts**: Relational Theory, Normalization, Foreign Keys, Constraints, Joins
