-- ============================================================
-- WinnerMIT University Student Management System
-- MIT 8103 - Advanced Database Systems
-- Portfolio 1: Database Design and Modelling
-- Target: MySQL 8.0.16+ (InnoDB)
--
-- IMPORTANT:
-- 1. Run this script in a development database, not a live system.
-- 2. The DROP DATABASE statement below deletes an existing database
--    named winnermit_usms. Remove/comment it if you already have data.
-- 3. The sample records are fictional demonstration data.
-- ============================================================

DROP DATABASE IF EXISTS winnermit_usms;
CREATE DATABASE winnermit_usms
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE winnermit_usms;

-- 1. Departments
CREATE TABLE departments (
    department_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_code VARCHAR(10) NOT NULL UNIQUE,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    office_location VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Programmes
CREATE TABLE programmes (
    programme_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    programme_code VARCHAR(15) NOT NULL UNIQUE,
    programme_name VARCHAR(120) NOT NULL,
    award_level VARCHAR(40) NOT NULL,
    duration_years TINYINT UNSIGNED NOT NULL,
    CONSTRAINT chk_programme_duration CHECK (duration_years BETWEEN 1 AND 8),
    CONSTRAINT fk_programmes_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 3. Students
CREATE TABLE students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    programme_id INT UNSIGNED NOT NULL,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(25),
    admission_date DATE NOT NULL,
    student_status VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT chk_student_status
        CHECK (student_status IN ('Active', 'Suspended', 'Graduated', 'Withdrawn')),
    CONSTRAINT fk_students_programme
        FOREIGN KEY (programme_id) REFERENCES programmes(programme_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_students_name (last_name, first_name)
) ENGINE=InnoDB;

-- 4. Lecturers
CREATE TABLE lecturers (
    lecturer_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    staff_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT chk_lecturer_status
        CHECK (employment_status IN ('Active', 'On Leave', 'Inactive')),
    CONSTRAINT fk_lecturers_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 5. Courses
CREATE TABLE courses (
    course_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    course_code VARCHAR(15) NOT NULL UNIQUE,
    course_title VARCHAR(150) NOT NULL,
    credit_units TINYINT UNSIGNED NOT NULL,
    course_description TEXT,
    CONSTRAINT chk_course_credit_units CHECK (credit_units BETWEEN 1 AND 6),
    CONSTRAINT fk_courses_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 6. Academic sessions
CREATE TABLE academic_sessions (
    session_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(20) NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT chk_session_dates CHECK (end_date > start_date)
) ENGINE=InnoDB;

-- 7. Course offerings
-- A course offering is a specific course taught by a lecturer
-- in a particular academic session and semester.
CREATE TABLE course_offerings (
    offering_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id INT UNSIGNED NOT NULL,
    lecturer_id INT UNSIGNED NOT NULL,
    session_id INT UNSIGNED NOT NULL,
    semester VARCHAR(20) NOT NULL,
    capacity SMALLINT UNSIGNED NOT NULL DEFAULT 100,
    CONSTRAINT chk_offering_semester
        CHECK (semester IN ('First', 'Second', 'Summer')),
    CONSTRAINT chk_offering_capacity CHECK (capacity > 0),
    CONSTRAINT uq_course_offering
        UNIQUE (course_id, session_id, semester),
    CONSTRAINT fk_offerings_course
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_offerings_lecturer
        FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_offerings_session
        FOREIGN KEY (session_id) REFERENCES academic_sessions(session_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_offerings_lecturer (lecturer_id),
    INDEX idx_offerings_session (session_id)
) ENGINE=InnoDB;

-- 8. Enrolments
-- This resolves the many-to-many relationship between students
-- and course offerings.
CREATE TABLE enrolments (
    enrolment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    offering_id INT UNSIGNED NOT NULL,
    enrolment_date DATE NOT NULL,
    enrolment_status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    CONSTRAINT chk_enrolment_status
        CHECK (enrolment_status IN ('Enrolled', 'Dropped', 'Completed')),
    CONSTRAINT uq_student_offering UNIQUE (student_id, offering_id),
    CONSTRAINT fk_enrolments_student
        FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_enrolments_offering
        FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_enrolments_offering (offering_id)
) ENGINE=InnoDB;

-- 9. Results
-- One result record is permitted for each enrolment.
CREATE TABLE results (
    result_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    enrolment_id INT UNSIGNED NOT NULL UNIQUE,
    assessment_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    examination_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    total_score DECIMAL(5,2)
        GENERATED ALWAYS AS (assessment_score + examination_score) STORED,
    grade VARCHAR(2),
    result_remarks VARCHAR(30) DEFAULT 'Pending',
    CONSTRAINT chk_assessment_score
        CHECK (assessment_score BETWEEN 0 AND 40),
    CONSTRAINT chk_examination_score
        CHECK (examination_score BETWEEN 0 AND 60),
    CONSTRAINT chk_result_grade
        CHECK (grade IS NULL OR grade IN ('A', 'B', 'C', 'D', 'E', 'F')),
    CONSTRAINT chk_result_remarks
        CHECK (result_remarks IN ('Pending', 'Pass', 'Fail')),
    CONSTRAINT fk_results_enrolment
        FOREIGN KEY (enrolment_id) REFERENCES enrolments(enrolment_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
-- FICTIONAL SAMPLE DATA FOR TESTING THE DESIGN
-- ============================================================

INSERT INTO departments (department_code, department_name, office_location) VALUES
('SCT', 'School of Computing and Technology', 'Block A'),
('SBS', 'School of Business Studies', 'Block B');

INSERT INTO programmes
(department_id, programme_code, programme_name, award_level, duration_years) VALUES
(1, 'MIT', 'Master of Information Technology', 'Masters', 2),
(1, 'BSC-CS', 'BSc Computer Science', 'Undergraduate', 4),
(2, 'MBA', 'Master of Business Administration', 'Masters', 2);

INSERT INTO students
(programme_id, student_number, first_name, last_name, email, phone, admission_date, student_status) VALUES
(1, 'WMIT2026001', 'Ada', 'Okafor', 'ada.okafor@example.edu', '+2348000000001', '2026-09-01', 'Active'),
(1, 'WMIT2026002', 'Tunde', 'Bello', 'tunde.bello@example.edu', '+2348000000002', '2026-09-01', 'Active'),
(2, 'WCS2026001', 'Amaka', 'Eze', 'amaka.eze@example.edu', '+2348000000003', '2026-09-01', 'Active');

INSERT INTO lecturers
(department_id, staff_number, first_name, last_name, email, employment_status) VALUES
(1, 'WML001', 'Chika', 'Nwosu', 'chika.nwosu@example.edu', 'Active'),
(1, 'WML002', 'Ibrahim', 'Yusuf', 'ibrahim.yusuf@example.edu', 'Active'),
(2, 'WML003', 'Grace', 'Adeyemi', 'grace.adeyemi@example.edu', 'Active');

INSERT INTO courses
(department_id, course_code, course_title, credit_units, course_description) VALUES
(1, 'MIT8103', 'Advanced Database Systems', 3, 'Relational, NoSQL and distributed database concepts.'),
(1, 'MIT8105', 'Network Architecture and Protocols', 3, 'Network models, protocols and architecture.'),
(2, 'MBA8101', 'Strategic Management', 3, 'Strategy formulation and organisational performance.'),
(1, 'CSC2101', 'Database Systems Foundations', 3, 'Relational model, SQL querying, and database normalization.');

INSERT INTO academic_sessions (session_name, start_date, end_date) VALUES
('2026/2027', '2026-09-01', '2027-08-31');

INSERT INTO course_offerings
(course_id, lecturer_id, session_id, semester, capacity) VALUES
(1, 1, 1, 'First', 80),
(2, 2, 1, 'First', 80),
(3, 3, 1, 'First', 60),
(4, 1, 1, 'First', 100);

INSERT INTO enrolments
(student_id, offering_id, enrolment_date, enrolment_status) VALUES
(1, 1, '2026-09-05', 'Enrolled'),
(2, 1, '2026-09-05', 'Enrolled'),
(1, 2, '2026-09-05', 'Enrolled'),
(3, 4, '2026-09-05', 'Enrolled');

INSERT INTO results
(enrolment_id, assessment_score, examination_score, grade, result_remarks) VALUES
(1, 32.00, 51.00, 'A', 'Pass'),
(2, 28.00, 42.00, 'B', 'Pass');

-- Quick verification queries
SELECT * FROM departments;
SELECT * FROM programmes;
SELECT * FROM students;
SELECT * FROM lecturers;
SELECT * FROM courses;
SELECT * FROM academic_sessions;
SELECT * FROM course_offerings;
SELECT * FROM enrolments;
SELECT * FROM results;
