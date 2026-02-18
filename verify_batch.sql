SELECT 
    'Student' as Table_Name, COUNT(*) as Count FROM Student
UNION ALL SELECT 'Teacher', COUNT(*) FROM Teacher
UNION ALL SELECT 'Class', COUNT(*) FROM Class
UNION ALL SELECT 'Department', COUNT(*) FROM Department
UNION ALL SELECT 'Enrollment', COUNT(*) FROM Enrollment
UNION ALL
SELECT 
    'Tamil Students', COUNT(*) 
FROM Student 
WHERE Name IN ('Karthik Raja', 'Priya Raman', 'Saravanan Velu');