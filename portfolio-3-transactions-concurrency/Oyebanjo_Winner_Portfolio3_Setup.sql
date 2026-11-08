-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 3: Transactions and Concurrency Control
-- ISOLATED TEST SCHEMA SETUP (winnermit_usms_p3)
-- Student: Winner Oyebanjo (ID: 301909418)
-- ============================================================

CREATE DATABASE IF NOT EXISTS winnermit_usms_p3
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE winnermit_usms_p3;

-- 1. Departments
CREATE TABLE IF NOT EXISTS departments (
    department_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_code VARCHAR(10) NOT NULL UNIQUE,
    department_name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 2. Programmes
CREATE TABLE IF NOT EXISTS programmes (
    programme_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    programme_code VARCHAR(15) NOT NULL UNIQUE,
    programme_name VARCHAR(120) NOT NULL
) ENGINE=InnoDB;

-- 3. Students
CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    programme_id INT UNSIGNED NOT NULL,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 4. Courses
CREATE TABLE IF NOT EXISTS courses (
    course_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    course_code VARCHAR(15) NOT NULL UNIQUE,
    course_title VARCHAR(150) NOT NULL,
    credit_units TINYINT UNSIGNED NOT NULL
) ENGINE=InnoDB;

-- 5. Academic sessions
CREATE TABLE IF NOT EXISTS academic_sessions (
    session_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 6. Course offerings (Critical for concurrency & capacity locking)
CREATE TABLE IF NOT EXISTS course_offerings (
    offering_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id INT UNSIGNED NOT NULL,
    session_id INT UNSIGNED NOT NULL,
    semester VARCHAR(20) NOT NULL,
    capacity SMALLINT UNSIGNED NOT NULL DEFAULT 2, -- Low capacity to test race conditions & saturation
    CONSTRAINT uq_p3_offering UNIQUE (course_id, session_id, semester)
) ENGINE=InnoDB;

-- 7. Enrolments
CREATE TABLE IF NOT EXISTS enrolments (
    enrolment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    offering_id INT UNSIGNED NOT NULL,
    enrolment_date DATE NOT NULL,
    enrolment_status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    CONSTRAINT uq_p3_stud_off UNIQUE (student_id, offering_id)
) ENGINE=InnoDB;

-- Baseline Seed Data
INSERT IGNORE INTO departments VALUES (1, 'SCT', 'School of Computing and Technology');
INSERT IGNORE INTO programmes VALUES (1, 1, 'MIT', 'Master of Information Technology');
INSERT IGNORE INTO students VALUES 
(1, 1, 'WMIT001', 'Ada', 'Okafor', 'ada@example.edu'),
(2, 1, 'WMIT002', 'Tunde', 'Bello', 'tunde@example.edu'),
(3, 1, 'WMIT003', 'Amaka', 'Eze', 'amaka@example.edu'),
(4, 1, 'WMIT004', 'Chinedu', 'Adewale', 'chinedu@example.edu');

INSERT IGNORE INTO courses VALUES (1, 1, 'MIT8103', 'Advanced Database Systems', 3);
INSERT IGNORE INTO courses VALUES (2, 1, 'MIT8105', 'Network Architecture and Protocols', 3);
INSERT IGNORE INTO academic_sessions VALUES (1, '2026/2027');

-- Offering 1 has a strictly limited capacity of 2 seats
INSERT IGNORE INTO course_offerings VALUES (1, 1, 1, 'First', 2);
-- Offering 2 has capacity of 2 seats
INSERT IGNORE INTO course_offerings VALUES (2, 2, 1, 'First', 2);

-- Pre-enrol Student 1 into Offering 1 (1 seat remaining)
INSERT IGNORE INTO enrolments VALUES (1, 1, 1, '2026-09-01', 'Enrolled');
