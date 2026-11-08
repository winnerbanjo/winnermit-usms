-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 2: Query Processing and Optimisation
-- ISOLATED BENCHMARK DATABASE SETUP (winnermit_usms_p2)
-- Student: Winner Oyebanjo (ID: 301909418)
-- ============================================================

CREATE DATABASE IF NOT EXISTS winnermit_usms_p2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE winnermit_usms_p2;

-- 1. Departments
CREATE TABLE IF NOT EXISTS departments (
    department_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_code VARCHAR(10) NOT NULL UNIQUE,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    office_location VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Programmes
CREATE TABLE IF NOT EXISTS programmes (
    programme_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    programme_code VARCHAR(15) NOT NULL UNIQUE,
    programme_name VARCHAR(120) NOT NULL,
    award_level VARCHAR(40) NOT NULL,
    duration_years TINYINT UNSIGNED NOT NULL,
    CONSTRAINT chk_p2_prog_dur CHECK (duration_years BETWEEN 1 AND 8),
    CONSTRAINT fk_p2_prog_dept FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 3. Students
CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    programme_id INT UNSIGNED NOT NULL,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(25),
    admission_date DATE NOT NULL,
    student_status VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT chk_p2_stud_stat CHECK (student_status IN ('Active', 'Suspended', 'Graduated', 'Withdrawn')),
    CONSTRAINT fk_p2_stud_prog FOREIGN KEY (programme_id) REFERENCES programmes(programme_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 4. Lecturers
CREATE TABLE IF NOT EXISTS lecturers (
    lecturer_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    staff_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT chk_p2_lect_stat CHECK (employment_status IN ('Active', 'On Leave', 'Inactive')),
    CONSTRAINT fk_p2_lect_dept FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 5. Courses
CREATE TABLE IF NOT EXISTS courses (
    course_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED NOT NULL,
    course_code VARCHAR(15) NOT NULL UNIQUE,
    course_title VARCHAR(150) NOT NULL,
    credit_units TINYINT UNSIGNED NOT NULL,
    course_description TEXT,
    CONSTRAINT chk_p2_crs_cu CHECK (credit_units BETWEEN 1 AND 6),
    CONSTRAINT fk_p2_crs_dept FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 6. Academic sessions
CREATE TABLE IF NOT EXISTS academic_sessions (
    session_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_name VARCHAR(20) NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT chk_p2_sess_dates CHECK (end_date > start_date)
) ENGINE=InnoDB;

-- 7. Course offerings
CREATE TABLE IF NOT EXISTS course_offerings (
    offering_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id INT UNSIGNED NOT NULL,
    lecturer_id INT UNSIGNED NOT NULL,
    session_id INT UNSIGNED NOT NULL,
    semester VARCHAR(20) NOT NULL,
    capacity SMALLINT UNSIGNED NOT NULL DEFAULT 100,
    CONSTRAINT chk_p2_off_sem CHECK (semester IN ('First', 'Second', 'Summer')),
    CONSTRAINT chk_p2_off_cap CHECK (capacity > 0),
    CONSTRAINT uq_p2_crs_offering UNIQUE (course_id, session_id, semester),
    CONSTRAINT fk_p2_off_crs FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_p2_off_lect FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_p2_off_sess FOREIGN KEY (session_id) REFERENCES academic_sessions(session_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 8. Enrolments
CREATE TABLE IF NOT EXISTS enrolments (
    enrolment_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED NOT NULL,
    offering_id INT UNSIGNED NOT NULL,
    enrolment_date DATE NOT NULL,
    enrolment_status VARCHAR(20) NOT NULL DEFAULT 'Enrolled',
    CONSTRAINT chk_p2_enr_stat CHECK (enrolment_status IN ('Enrolled', 'Dropped', 'Completed')),
    CONSTRAINT uq_p2_stud_offering UNIQUE (student_id, offering_id),
    CONSTRAINT fk_p2_enr_stud FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_p2_enr_off FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 9. Results
CREATE TABLE IF NOT EXISTS results (
    result_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    enrolment_id INT UNSIGNED NOT NULL UNIQUE,
    assessment_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    examination_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    total_score DECIMAL(5,2) GENERATED ALWAYS AS (assessment_score + examination_score) STORED,
    grade VARCHAR(2),
    result_remarks VARCHAR(30) DEFAULT 'Pending',
    CONSTRAINT chk_p2_res_ass CHECK (assessment_score BETWEEN 0 AND 40),
    CONSTRAINT chk_p2_res_exam CHECK (examination_score BETWEEN 0 AND 60),
    CONSTRAINT chk_p2_res_grd CHECK (grade IS NULL OR grade IN ('A', 'B', 'C', 'D', 'E', 'F')),
    CONSTRAINT chk_p2_res_rem CHECK (result_remarks IN ('Pending', 'Pass', 'Fail')),
    CONSTRAINT fk_p2_res_enr FOREIGN KEY (enrolment_id) REFERENCES enrolments(enrolment_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;
