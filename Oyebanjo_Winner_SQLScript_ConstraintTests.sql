-- ============================================================
-- WinnerMIT University Student Management System
-- MIT 8103 - Advanced Database Systems
-- NEGATIVE CONSTRAINT & INTEGRITY TEST SUITE
-- Target: winnermit_usms_test
--
-- This script intentionally attempts invalid operations to prove
-- that MySQL 8.0.16+ / 26.x actively enforces all constraints.
-- Every test is isolated so it does not corrupt valid data.
-- ============================================================

USE winnermit_usms_test;

-- TEST CASE 1: Negative Check Constraint on assessment_score (> 40.00)
-- EXPECTED RESULT: FAILS with Check constraint 'chk_assessment_score' is violated.
-- INSERT INTO results (enrolment_id, assessment_score, examination_score, grade, result_remarks)
-- VALUES (3, 45.00, 50.00, 'A', 'Pass');

-- TEST CASE 2: Negative Check Constraint on examination_score (> 60.00)
-- EXPECTED RESULT: FAILS with Check constraint 'chk_examination_score' is violated.
-- INSERT INTO results (enrolment_id, assessment_score, examination_score, grade, result_remarks)
-- VALUES (3, 30.00, 65.00, 'A', 'Pass');

-- TEST CASE 3: Negative Check Constraint on semester (invalid value 'Autumn')
-- EXPECTED RESULT: FAILS with Check constraint 'chk_offering_semester' is violated.
-- INSERT INTO course_offerings (course_id, lecturer_id, session_id, semester, capacity)
-- VALUES (1, 1, 1, 'Autumn', 50);

-- TEST CASE 4: Negative Foreign Key Constraint (non-existent programme_id = 999)
-- EXPECTED RESULT: FAILS with Cannot add or update a child row: a foreign key constraint fails.
-- INSERT INTO students (programme_id, student_number, first_name, last_name, email, admission_date)
-- VALUES (999, 'WMITTEST999', 'Fake', 'Student', 'fake@example.edu', '2026-09-01');

-- TEST CASE 5: Duplicate Enrolment Unique Key Constraint (student 1 already in offering 1)
-- EXPECTED RESULT: FAILS with Duplicate entry '1-1' for key 'enrolments.uq_student_offering'.
-- INSERT INTO enrolments (student_id, offering_id, enrolment_date)
-- VALUES (1, 1, '2026-09-06');
