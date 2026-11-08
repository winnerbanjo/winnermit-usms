-- ============================================================
-- WinnerMIT University Student Management System
-- MIT 8103 - Advanced Database Systems
-- Verification & Analytical Query Suite
-- Target Database: winnermit_usms_test (or winnermit_usms)
-- ============================================================

USE winnermit_usms_test;

-- 1. Table Row Counts Audit
SELECT 'departments' AS table_name, COUNT(*) AS total_rows FROM departments
UNION ALL SELECT 'programmes', COUNT(*) FROM programmes
UNION ALL SELECT 'students', COUNT(*) FROM students
UNION ALL SELECT 'lecturers', COUNT(*) FROM lecturers
UNION ALL SELECT 'courses', COUNT(*) FROM courses
UNION ALL SELECT 'academic_sessions', COUNT(*) FROM academic_sessions
UNION ALL SELECT 'course_offerings', COUNT(*) FROM course_offerings
UNION ALL SELECT 'enrolments', COUNT(*) FROM enrolments
UNION ALL SELECT 'results', COUNT(*) FROM results;

-- 2. Student Enrolment and Programme Roster
SELECT 
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    p.programme_code,
    p.award_level,
    c.course_code,
    c.course_title,
    c.credit_units,
    co.semester,
    sess.session_name,
    CONCAT(l.first_name, ' ', l.last_name) AS lecturer_name
FROM enrolments e
JOIN students s ON e.student_id = s.student_id
JOIN programmes p ON s.programme_id = p.programme_id
JOIN course_offerings co ON e.offering_id = co.offering_id
JOIN courses c ON co.course_id = c.course_id
JOIN academic_sessions sess ON co.session_id = sess.session_id
JOIN lecturers l ON co.lecturer_id = l.lecturer_id
ORDER BY p.award_level DESC, s.student_number;

-- 3. Student Academic Performance & Grade Sheet
SELECT 
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.course_code,
    c.course_title,
    r.assessment_score,
    r.examination_score,
    r.total_score,
    r.grade,
    r.result_remarks
FROM results r
JOIN enrolments e ON r.enrolment_id = e.enrolment_id
JOIN students s ON e.student_id = s.student_id
JOIN course_offerings co ON e.offering_id = co.offering_id
JOIN courses c ON co.course_id = c.course_id;

-- 4. Course Enrolment Capacity & Class Utilization Report
SELECT 
    c.course_code,
    c.course_title,
    co.semester,
    sess.session_name,
    co.capacity AS max_capacity,
    COUNT(e.enrolment_id) AS enrolled_students,
    (co.capacity - COUNT(e.enrolment_id)) AS remaining_seats
FROM course_offerings co
JOIN courses c ON co.course_id = c.course_id
JOIN academic_sessions sess ON co.session_id = sess.session_id
LEFT JOIN enrolments e ON co.offering_id = e.offering_id
GROUP BY co.offering_id, c.course_code, c.course_title, co.semester, sess.session_name, co.capacity;

-- 5. Departmental Academic Staff & Course Offerings Distribution
SELECT 
    d.department_code,
    d.department_name,
    CONCAT(l.first_name, ' ', l.last_name) AS lecturer_name,
    l.staff_number,
    COUNT(co.offering_id) AS assigned_offerings
FROM departments d
JOIN lecturers l ON d.department_id = l.department_id
LEFT JOIN course_offerings co ON l.lecturer_id = co.lecturer_id
GROUP BY d.department_code, d.department_name, l.lecturer_id, l.first_name, l.last_name, l.staff_number
ORDER BY d.department_code, lecturer_name;
