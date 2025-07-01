Create DATABASE field_training2;
USE field_training2 ;
-- Phase 4 updated ---------------------------
-- sec 1 :  create tables of database 
-- 1.1  user table
CREATE TABLE User (
    ID INT PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL,
    Phone_No VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255)
);
-- 1.2 mentor table
CREATE TABLE Mentor (
    Mentor_ID INT PRIMARY KEY,
    Years_of_Experience INT,
    Department VARCHAR(100),
    Job_Title VARCHAR(100),
    Office_Hrs VARCHAR(100),
    Max_Assigned_Students INT CHECK (Max_Assigned_Students <= 100),
    FOREIGN KEY (Mentor_ID) REFERENCES User(ID)
);


-- 1.3 create Uni_Mentor table
CREATE TABLE Uni_Mentor (
    Uni_Mentor_ID INT PRIMARY KEY,
    Uni_Name VARCHAR(100),
    Feedback_Score DECIMAL(3,2),
    Assigned_Level VARCHAR(50),
    Years_of_Experience INT,
    Department VARCHAR(100),
    Job_Title VARCHAR(100),
    FOREIGN KEY (Uni_Mentor_ID) REFERENCES Mentor(Mentor_ID)
);
-- 1.4 create student table
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    CGPA DECIMAL(3,2),
    Application_State VARCHAR(50),
    Major VARCHAR(100),
    Academic_Level VARCHAR(50),
    Tech_Skills TEXT,
    Certification TEXT,
    LinkedIn_Profile VARCHAR(255),
    Uni_Mentor_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES User(ID),
    FOREIGN KEY (Uni_Mentor_ID) REFERENCES Uni_Mentor(Uni_Mentor_ID)
);
-- 1.5 create company table
CREATE TABLE Company (
    Company_Logo VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(100),
    Industry VARCHAR(100),
    Website VARCHAR(255),
    Student_ID INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);
-- 1.6 create company_mentor
CREATE TABLE Company_Mentor (
    Company_Mentor_ID INT PRIMARY KEY,
    Company_Name VARCHAR(100),
    Assigned_Branch VARCHAR(100),
    Evaluation_Feedback TEXT,
    Company_Logo VARCHAR(255),
    Mentor_ID INT,
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID),
    FOREIGN KEY (Company_Logo) REFERENCES Company(Company_Logo)
);
-- 1.7 create company_location 
CREATE TABLE Company_Location (
    Company_Logo VARCHAR(255),
    Locations VARCHAR(255),
    PRIMARY KEY (Company_Logo, Locations),
    FOREIGN KEY (Company_Logo) REFERENCES Company(Company_Logo)
);
-- 1.8 create Acadenic_docs table
CREATE TABLE Academic_Docs (
    Doc_ID INT PRIMARY KEY,
    Uploaded_By VARCHAR(100),
    Uni_Mentor_ID INT,
    Timestamp DATETIME,
    Transcript TEXT,
    Recommendation_Letter TEXT,
    FOREIGN KEY (Uni_Mentor_ID) REFERENCES Uni_Mentor(Uni_Mentor_ID)
);
-- 1.9 create Internship_Application
CREATE TABLE Internship_Application (
    Application_ID INT PRIMARY KEY,
    Company_Mentor_ID INT,
    Uni_Mentor_ID INT,
    Student_ID INT,
    Status VARCHAR(50),
    Applied_Date DATE,
    Decision_Date DATE,
    Doc_ID INT,
    FOREIGN KEY (Company_Mentor_ID) REFERENCES Company_Mentor(Company_Mentor_ID),
    FOREIGN KEY (Uni_Mentor_ID) REFERENCES Uni_Mentor(Uni_Mentor_ID),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Doc_ID) REFERENCES Academic_Docs(Doc_ID)
);
-- 1.10 create Has_a_Relation table
CREATE TABLE Has_a_Relation (
    Company_Logo VARCHAR(255),
    Application_ID INT,
    PRIMARY KEY (Company_Logo, Application_ID),
    FOREIGN KEY (Company_Logo) REFERENCES Company(Company_Logo),
    FOREIGN KEY (Application_ID) REFERENCES Internship_Application(Application_ID)
);
-- 1.11 create Evaluation_Report table
CREATE TABLE Evaluation_Report (
    Report_ID INT PRIMARY KEY,
    Evaluation_Date DATE,
    Company_Mentor_ID INT,
    Performance_Score DECIMAL(3,2),
    Feedback TEXT,
    FOREIGN KEY (Company_Mentor_ID) REFERENCES Company_Mentor(Company_Mentor_ID)
);
-- 1.12 create Performance_Score tavble
CREATE TABLE Performance_Score (
    Report_ID INT,
    Student_ID INT,
    Score DECIMAL(3,2),
    PRIMARY KEY (Report_ID, Student_ID),
    FOREIGN KEY (Report_ID) REFERENCES Evaluation_Report(Report_ID),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);
 -- 1.13  create Application_Company_Mentor table
CREATE TABLE Application_Company_Mentor (
    Application_ID INT,
    Company_Mentor_ID INT,
    PRIMARY KEY (Application_ID, Company_Mentor_ID),
    FOREIGN KEY (Application_ID) REFERENCES Internship_Application(Application_ID),
    FOREIGN KEY (Company_Mentor_ID) REFERENCES Company_Mentor(Company_Mentor_ID)
);

-- ----------------------------------
-- sec 2 : insert the data
-- 2.1: Insert data into User table 
INSERT INTO User (ID, Name, Phone_No, Email, Address) VALUES
(1, 'Ali Salem', '0551234567', 'ali.salem@email.com', 'Riyadh, Saudi Arabia'),
(2, 'Sara Ahmed', '0569876543', 'sara.ahmed@email.com', 'Jeddah, Saudi Arabia'),
(3, 'Omar Khalid', '0541122334', 'omar.khalid@email.com', 'Dammam, Saudi Arabia'),
(4, 'Nora Faisal', '0574455667', 'nora.faisal@email.com', 'Abha, Saudi Arabia'),
(5, 'Yousef Hamad', '0583344556', 'yousef.hamad@email.com', 'Tabuk, Saudi Arabia'),
(6, 'Lina Mohammed', '0539988776', 'lina.mohammed@email.com', 'Mecca, Saudi Arabia');

-- 2.2: Insert data into Mentor table
INSERT INTO Mentor (Mentor_ID, Years_of_Experience, Department, Job_Title, Office_Hrs, Max_Assigned_Students) VALUES
(1, 10, 'Computer Science', 'Senior Mentor', '9AM-12PM', 5),
(2, 8, 'Information Systems', 'Mentor', '1PM-4PM', 4),
(3, 12, 'Software Engineering', 'Lead Mentor', '10AM-1PM', 6) ;
INSERT INTO Mentor (Mentor_ID, Years_of_Experience, Department, Job_Title, Office_Hrs, Max_Assigned_Students) VALUES
(4, 5, 'Cybersecurity', 'Assistant Mentor', '8AM-10AM', 3),
(5, 15, 'AI & Robotics', 'Senior Lecturer', '10AM-12PM', 4),
(6, 9, 'Data Science', 'Mentor', '1PM-3PM', 5);

-- 2.3: Insert data into Uni_Mentor table
INSERT INTO Uni_Mentor (Uni_Mentor_ID, Uni_Name, Feedback_Score, Assigned_Level, Years_of_Experience, Department, Job_Title) VALUES
(1, 'King Saud University', 4.8, 'Senior', 10, 'Computer Science', 'Professor'),
(2, 'KAU', 4.6, 'Intermediate', 7, 'Information Systems', 'Associate Professor'),
(3, 'Imam University', 4.9, 'Senior', 12, 'Software Engineering', 'Department Head');
INSERT INTO Uni_Mentor (Uni_Mentor_ID, Uni_Name, Feedback_Score, Assigned_Level, Years_of_Experience, Department, Job_Title) VALUES
(4, 'PNU', 4.5, 'Junior', 6, 'Cybersecurity', 'Lecturer'),
(5, 'Taibah University', 4.7, 'Senior', 13, 'AI', 'Professor'),
(6, 'KFUPM', 4.4, 'Intermediate', 8, 'Data Science', 'Assistant Professor');

-- 2.4: Insert data into Student table
INSERT INTO Student (Student_ID, CGPA, Application_State, Major, Academic_Level, Tech_Skills, Certification, LinkedIn_Profile, Uni_Mentor_ID) VALUES
(4, 3.75, 'Pending', 'Computer Science', 'Senior', 'Java, Python', 'AWS Cloud Practitioner', 'linkedin.com/in/nora', 1),
(5, 3.90, 'Approved', 'Information Systems', 'Junior', 'SQL, Tableau', 'Google Data Analytics', 'linkedin.com/in/yousef', 2),
(6, 3.45, 'Rejected', 'Software Engineering', 'Senior', 'C++, Flutter', 'Scrum Fundamentals', 'linkedin.com/in/lina', 3);
INSERT INTO Student (Student_ID, CGPA, Application_State, Major, Academic_Level, Tech_Skills, Certification, LinkedIn_Profile, Uni_Mentor_ID) VALUES
(1, 3.60, 'Approved', 'Cybersecurity', 'Junior', 'Network Security, Python', 'CEH', 'linkedin.com/in/maha', 4),
(2, 3.82, 'Pending', 'AI', 'Senior', 'TensorFlow, ML', 'AI Expert Cert', 'linkedin.com/in/tariq', 5),
(3, 3.40, 'Approved', 'Data Science', 'Senior', 'Pandas, R', 'DataCamp Cert', 'linkedin.com/in/reem', 6);

-- 2.5: Insert data into Campony table
INSERT INTO Company (Company_Logo, Name, Industry, Website, Student_ID) VALUES
('logo1.png', 'Aramco', 'Energy', 'https://aramco.com', 4),
('logo2.png', 'STC', 'Telecom', 'https://stc.com.sa', 5),
('logo3.png', 'SAPTCO', 'Transportation', 'https://saptco.com.sa', 6);
INSERT INTO Company (Company_Logo, Name, Industry, Website, Student_ID) VALUES
('logo4.png', 'NEOM', 'Smart City', 'https://neom.com', 1),
('logo5.png', 'Mobily', 'Telecom', 'https://mobily.com.sa', 2),
('logo6.png', 'Careem', 'Tech/Transport', 'https://careem.com', 3);

-- 2.6: Insert data into Campany_Mentor table
INSERT INTO Company_Mentor (Company_Mentor_ID, Company_Name, Assigned_Branch, Evaluation_Feedback, Company_Logo, Mentor_ID) VALUES
(1, 'Aramco', 'Dhahran', 'Excellent guidance and support.', 'logo1.png', 1),
(2, 'STC', 'Riyadh', 'Very helpful and engaging.', 'logo2.png', 2),
(3, 'SAPTCO', 'Jeddah', 'Provided valuable experience.', 'logo3.png', 3),
(4, 'NEOM', 'NEOM City', 'Great support and innovation.', 'logo4.png', 4),
(5, 'Mobily', 'Riyadh', 'Highly responsive mentor.', 'logo5.png', 5),
(6, 'Careem', 'Jeddah', 'Provided diverse projects.', 'logo6.png', 6);

-- 2.7: Insert data into compony_location table 
-- company location is a multivalued attribute of the company table so we separate its table :)
INSERT INTO Company_Location (Company_Logo, Locations) VALUES
('logo1.png', 'Dhahran'),
('logo1.png', 'Riyadh'),
('logo2.png', 'Jeddah'),
('logo2.png', 'Mecca'),
('logo3.png', 'Abha'),
('logo3.png', 'Dammam')
;

-- 2.8: Insert data into Academic_Docs table
INSERT INTO Academic_Docs (Doc_ID, Uploaded_By, Uni_Mentor_ID, Timestamp, Transcript, Recommendation_Letter) VALUES
(101, 'Dr. Ali', 1, '2025-04-01 10:00:00', 'Transcript of Nora', 'Letter for Nora'),
(102, 'Dr. Sara', 2, '2025-04-01 11:00:00', 'Transcript of Yousef', 'Letter for Yousef'),
(103, 'Dr. Omar', 3, '2025-04-01 12:00:00', 'Transcript of Lina', 'Letter for Lina');
INSERT INTO Academic_Docs (Doc_ID, Uploaded_By, Uni_Mentor_ID, Timestamp, Transcript, Recommendation_Letter) VALUES
(104, 'Dr. Maha', 4, '2025-04-02 08:00:00', 'Transcript of Maha', 'Letter for Maha'),
(105, 'Dr. Tariq', 5, '2025-04-02 09:00:00', 'Transcript of Tariq', 'Letter for Tariq'),
(106, 'Dr. Reem', 6, '2025-04-02 10:00:00', 'Transcript of Reem', 'Letter for Reem');


-- 2.9: Insert data into Internship_Application table
INSERT INTO Internship_Application (Application_ID, Company_Mentor_ID, Uni_Mentor_ID, Student_ID, Status, Applied_Date, Decision_Date, Doc_ID) VALUES
(201, 1, 1, 4, 'Accepted', '2025-03-01', '2025-03-15', 101),
(202, 2, 2, 5, 'Pending', '2025-03-05', NULL, 102),
(203, 3, 3, 6, 'Rejected', '2025-03-07', '2025-03-20', 103),
(204, 4, 4, 1, 'Accepted', '2025-03-10', '2025-03-25', 104),
(205, 5, 5, 2, 'Pending', '2025-03-12', NULL, 105),
(206, 6, 6, 3, 'Accepted', '2025-03-15', '2025-03-28', 106);

-- 2.10: Insert data into Evaluation_Report table
INSERT INTO Evaluation_Report (Report_ID, Evaluation_Date, Company_Mentor_ID, Performance_Score, Feedback) VALUES
(301, '2025-04-10', 1, 4.5, 'Excellent performance by student.'),
(302, '2025-04-12', 2, 3.9, 'Good progress, needs improvement in teamwork.'),
(303, '2025-04-15', 3, 3.2, 'Average skills, needs more training.'),
(304, '2025-04-17', 4, 4.8, 'Outstanding contributions and attitude.'),
(305, '2025-04-18', 5, 4.0, 'Great learning curve observed.'),
(306, '2025-04-19', 6, 4.6, 'Well-performed in technical tasks.');

-- 2.11: Insert data into Performance_Score table
INSERT INTO Performance_Score (Report_ID, Student_ID, Score) VALUES
(301, 4, 4.5),
(302, 5, 3.9),
(303, 6, 3.2),
(304, 1, 4.8),
(305, 2, 4.0),
(306, 3, 4.6);


 -- sec 3 : RELATIONAL TABLE 
-- 3.1: Insert data into Application_Company_Mentor table(junction table)
INSERT INTO Application_Company_Mentor (Application_ID, Company_Mentor_ID) VALUES
(201, 1),
(202, 2),
(203, 3),
(204, 4),
(205, 5),
(206, 6);
-- 3.2: Insert data into Has_a_Relation table
INSERT INTO Has_a_Relation (Company_Logo, Application_ID) VALUES
('logo1.png', 201),
('logo2.png', 202),
('logo3.png', 203),
('logo4.png', 204),
('logo5.png', 205),
('logo6.png', 206);





-- sec 4 : select the tables
SELECT * FROM User;
SELECT * FROM Mentor;
SELECT * FROM Uni_Mentor;
SELECT * FROM Student;
SELECT * FROM Company;
SELECT * FROM Company_Mentor;
SELECT * FROM Company_Location;
SELECT * FROM Academic_Docs;
SELECT * FROM Internship_Application;
SELECT * FROM Has_a_Relation;
SELECT * FROM Evaluation_Report;
SELECT * FROM Performance_Score;
SELECT * FROM Application_Company_Mentor;
-- -----------------------------------------------------------------------------------
-- PHASE 5
-- -----------------------------------------------------------------------------------
-- 1)List all students registered for training along with their mentor
-- This query retrieves student information along with their university and company mentors
SELECT 
    s.Student_ID, 
    u.Name AS Student_Name, 
    um.Uni_Name AS University_Mentor,
    cm.Company_Name AS Company_Mentor
FROM Student s
JOIN User u ON s.Student_ID = u.ID
LEFT JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
LEFT JOIN Uni_Mentor um ON ia.Uni_Mentor_ID = um.Uni_Mentor_ID
LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
LEFT JOIN Company_Mentor cm ON ia.Company_Mentor_ID = cm.Company_Mentor_ID
WHERE ia.Application_ID IS NOT NULL;
    
-- 2)Which students are assigned to a particular company mentor (given a specific mentor ID)?
-- This query finds all students assigned to a specific company mentor (ID 5 in this case)
SELECT 
    s.Student_ID, 
    u.Name AS Student_Name,
    s.Major,
    s.CGPA
FROM Internship_Application ia
JOIN Student s ON ia.Student_ID = s.Student_ID
JOIN User u ON s.Student_ID = u.ID
WHERE ia.Company_Mentor_ID = 5 ;
    
-- 3)How many students are assigned to each company mentor?
-- This query counts the number of students assigned to each company mentor
SELECT cm.Company_Mentor_ID,u.Name AS Mentor_Name,cm.Company_Name,COUNT(ia.Student_ID) AS Assigned_Students
FROM Company_Mentor cm
JOIN User u ON cm.Mentor_ID = u.ID
LEFT JOIN Internship_Application ia ON cm.Company_Mentor_ID = ia.Company_Mentor_ID
GROUP BY cm.Company_Mentor_ID, u.Name, cm.Company_Name;
    
-- 4)List all trainings and the number of enrolled students
-- This query shows each company's training program and how many students are enrolled
SELECT 
    c.Name AS Company_Name,
    c.Industry,
    COUNT(DISTINCT ia.Student_ID) AS Enrolled_Students
FROM Company c
JOIN Has_a_Relation hr ON c.Company_Logo = hr.Company_Logo
JOIN Internship_Application ia ON hr.Application_ID = ia.Application_ID
GROUP BY c.Name, c.Industry;
    
-- 5)Which students have registered for training but do not have a supervisor assigned yet?
-- This query identifies students who registered but don't have a university mentor
SELECT 
    s.Student_ID,
    u.Name AS Student_Name,
    s.Major
FROM Internship_Application ia
JOIN Student s ON ia.Student_ID = s.Student_ID
JOIN User u ON s.Student_ID = u.ID
WHERE 
    ia.Status = 'Registered' 
    AND s.Uni_Mentor_ID IS NULL;
    
-- 6)List names and emails of all users who live in 'Riyadh'
-- This query finds all users with Riyadh in their address
SELECT 
    Name,
    Email
FROM 
    User
WHERE 
    Address LIKE '%Riyadh%';

    
-- 7)How many students with GPA higher than 3?
-- This query counts students with CGPA above 3.0
SELECT 
    COUNT(*) AS High_GPA_Students
FROM Student
WHERE CGPA > 3.0;
    
-- 8)How many students were approved?
-- This query counts students with approved application status
SELECT 
    COUNT(*) AS Approved_Students
FROM Student
WHERE Application_State = 'Approved';
    
-- 9)Show students with specific majors
-- This query filters students by major (Computer Science in this case)
SELECT 
    s.Student_ID,
    u.Name AS Student_Name,
    s.CGPA,
    s.Academic_Level
FROM Student s
JOIN User u ON s.Student_ID = u.ID
WHERE s.Major = 'Computer Science';
    
--  10)Show students according to the nearest addresses
-- This query lists students ordered by their address (for proximity sorting)
SELECT 
    s.Student_ID,
    u.Name AS Student_Name,
    u.Address
FROM Student s
JOIN User u ON s.Student_ID = u.ID
ORDER BY u.Address;
    
-- 11)Find Students with Highest Performance Score
-- This query identifies students with the maximum performance score in evaluations
SELECT 
    s.Student_ID,
    u.Name AS Student_Name,
    er.Performance_Score
FROM Student s
JOIN User u ON s.Student_ID = u.ID
JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
WHERE 
    er.Performance_Score = (
        SELECT MAX(Performance_Score) 
        FROM Evaluation_Report
    )
ORDER BY 
    u.Name;


-- 12)How many companies accepted students?
-- This query counts distinct companies that have accepted students

SELECT 
    COUNT(DISTINCT c.Company_Logo) AS Companies_Accepting_Students
FROM Company c
JOIN Has_a_Relation hr ON c.Company_Logo = hr.Company_Logo
JOIN Internship_Application ia ON hr.Application_ID = ia.Application_ID
WHERE ia.Status = 'Accepted';
    
-- ---------------------------------------------------------------------
-- 1. Student Dashboard View
CREATE VIEW StudentDashboard AS
SELECT 
    s.Student_ID,
    u.Name AS Student_Name,
    s.CGPA,
    s.Major,
    s.Academic_Level,
    ia.Application_ID,
    ia.Status AS Application_Status,
    c.Name AS Company_Name,
    c.Industry,
    um.Uni_Name AS University_Mentor,
    cm.Company_Name AS Company_Mentor,
    er.Performance_Score,
    er.Feedback AS Evaluation_Feedback
FROM Student s
JOIN User u ON s.Student_ID = u.ID
LEFT JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
LEFT JOIN Uni_Mentor um ON ia.Uni_Mentor_ID = um.Uni_Mentor_ID
LEFT JOIN Company_Mentor cm ON ia.Company_Mentor_ID = cm.Company_Mentor_ID
LEFT JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID;

-- View all student records with their internship applications
SELECT * FROM StudentDashboard;

-- View dashboard for a specific student by ID
SELECT * FROM StudentDashboard WHERE Student_ID = 3 ;

-- Example: Get dashboard for student with ID 2
SELECT * FROM StudentDashboard WHERE Student_ID = 2;
    
-- 2. Company Mentor View
CREATE VIEW CompanyMentorView AS
SELECT 
    cm.Company_Mentor_ID,
    u_cm.Name AS Company_Mentor_Name,
    c.Name AS Company_Name,
    c.Industry,
    ia.Application_ID,
    s.Student_ID,
    u_s.Name AS Student_Name,
    ia.Status AS Application_Status,
    ia.Applied_Date,
    ia.Decision_Date,
    er.Report_ID,
    er.Evaluation_Date,
    er.Feedback,
    ps.Score AS Performance_Score
FROM Company_Mentor cm
JOIN User u_cm ON cm.Company_Mentor_ID = u_cm.ID
JOIN Company c ON cm.Company_Logo = c.Company_Logo
LEFT JOIN Internship_Application ia ON cm.Company_Mentor_ID = ia.Company_Mentor_ID
LEFT JOIN Student s ON ia.Student_ID = s.Student_ID
LEFT JOIN User u_s ON s.Student_ID = u_s.ID
LEFT JOIN Academic_Docs ad ON ia.Doc_ID = ad.Doc_ID
LEFT JOIN Evaluation_Report er ON cm.Company_Mentor_ID = er.Company_Mentor_ID
LEFT JOIN 
    (SELECT Report_ID, Student_ID, Score 
     FROM Performance_Score) ps ON er.Report_ID = ps.Report_ID AND s.Student_ID = ps.Student_ID;
    
    -- View all records in the CompanyMentorView
SELECT * FROM CompanyMentorView;

-- View dashboard for a specific company mentor by ID
SELECT * FROM CompanyMentorView WHERE Company_Mentor_ID = 4;

    
-- 3. University Coordinator View
CREATE VIEW UniversityCoordinatorView AS
SELECT 
    um.Uni_Mentor_ID,
    u.Name AS Coordinator_Name,
    um.Uni_Name AS University,
    um.Feedback_Score,
    COUNT(DISTINCT s.Student_ID) AS Assigned_Students,
    AVG(er.Performance_Score) AS Avg_Performance_Score,
    COUNT(DISTINCT CASE WHEN ia.Status = 'Accepted' THEN s.Student_ID END) AS Placed_Students,
    COUNT(DISTINCT c.Company_Logo) AS Partner_Companies
FROM Uni_Mentor um
JOIN Mentor m ON um.Uni_Mentor_ID = m.Mentor_ID  
JOIN User u ON m.Mentor_ID = u.ID
LEFT JOIN Internship_Application ia ON um.Uni_Mentor_ID = ia.Uni_Mentor_ID
LEFT JOIN Student s ON ia.Student_ID = s.Student_ID
LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
LEFT JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
GROUP BY um.Uni_Mentor_ID, u.Name, um.Uni_Name, um.Feedback_Score;
    
SELECT * FROM UniversityCoordinatorView;

SELECT * FROM UniversityCoordinatorView 
WHERE Uni_Mentor_ID = 6 ;

-- ---------------------------------------------------
-- Stored Procedure
DELIMITER //

CREATE PROCEDURE GetStudentReport(IN student_id INT)
BEGIN
    SELECT 
        u.Name AS Student_Name,
        s.Major,
        s.Academic_Level,
        s.CGPA,
        c.Name AS Company_Name,
        c.Industry,
        ia.Status AS Application_Status,
        ia.Applied_Date,
        ia.Decision_Date,
        um.Name AS University_Mentor,
        cm.Name AS Company_Mentor,
        ps.Score AS Performance_Score,
        er.Evaluation_Date,
        er.Feedback,
        ad.Timestamp AS Document_Upload_Date,
        ad.Transcript,
        ad.Recommendation_Letter
    FROM 
        User u
    JOIN 
        Student s ON u.ID = s.Student_ID
    LEFT JOIN 
        Internship_Application ia ON s.Student_ID = ia.Student_ID
    LEFT JOIN 
        Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
    LEFT JOIN 
        Company c ON hr.Company_Logo = c.Company_Logo
    LEFT JOIN 
        Uni_Mentor umt ON ia.Uni_Mentor_ID = umt.Uni_Mentor_ID
    LEFT JOIN 
        User um ON umt.Uni_Mentor_ID = um.ID
    LEFT JOIN 
        Company_Mentor cmt ON ia.Company_Mentor_ID = cmt.Company_Mentor_ID
    LEFT JOIN 
        User cm ON cmt.Mentor_ID = cm.ID
    LEFT JOIN 
        Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
    LEFT JOIN 
        Performance_Score ps ON er.Report_ID = ps.Report_ID AND ps.Student_ID = s.Student_ID
    LEFT JOIN 
        Academic_Docs ad ON ia.Doc_ID = ad.Doc_ID AND ad.Uploaded_By = s.Student_ID
    WHERE 
        s.Student_ID = student_id;
END //

DELIMITER ;


-- Get full report for student with ID 6
CALL GetStudentReport(4);

-- Get only application status and company info
CALL GetStudentReport(8);





