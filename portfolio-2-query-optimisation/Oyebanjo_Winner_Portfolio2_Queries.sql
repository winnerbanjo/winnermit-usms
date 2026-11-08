-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 2: Query Processing and Optimisation
-- MASTER ANALYTICAL QUERY SUITE
-- Target: winnermit_usms_p2
-- Student: Winner Oyebanjo (ID: 301909418)
-- ============================================================

USE winnermit_usms_p2;

-- Query 1: Student Academic Performance & GPA Analysis
SELECT 
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    p.programme_code,
    d.department_code,
    COUNT(e.enrolment_id) AS courses_passed,
    ROUND(AVG(r.total_score), 2) AS average_score,
    SUM(c.credit_units) AS total_credits_earned
FROM students s
JOIN programmes p ON s.programme_id = p.programme_id
JOIN departments d ON p.department_id = d.department_id
JOIN enrolments e ON s.student_id = e.student_id
JOIN course_offerings co ON e.offering_id = co.offering_id
JOIN courses c ON co.course_id = c.course_id
JOIN results r ON e.enrolment_id = r.enrolment_id
WHERE d.department_code = 'SCT'
  AND r.result_remarks = 'Pass'
GROUP BY s.student_id, s.student_number, s.first_name, s.last_name, p.programme_code, d.department_code
HAVING average_score >= 60.00
ORDER BY average_score DESC;

-- Query 2: Course Enrolment Demand & Utilization
SELECT 
    c.course_code,
    c.course_title,
    sess.session_name,
    co.semester,
    co.capacity,
    COUNT(e.enrolment_id) AS enrolled_count,
    ROUND(AVG(r.examination_score), 2) AS avg_exam_score
FROM course_offerings co
JOIN courses c ON co.course_id = c.course_id
JOIN academic_sessions sess ON co.session_id = sess.session_id
JOIN enrolments e ON co.offering_id = e.offering_id
LEFT JOIN results r ON e.enrolment_id = r.enrolment_id
WHERE sess.session_name = '2026/2027'
GROUP BY co.offering_id, c.course_code, c.course_title, sess.session_name, co.semester, co.capacity
HAVING enrolled_count >= 5
ORDER BY enrolled_count DESC;

-- Query 3: At-Risk Student Early Warning Subquery
SELECT 
    s.student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    p.programme_name,
    (SELECT ROUND(AVG(r2.total_score), 2)
     FROM enrolments e2
     JOIN results r2 ON e2.enrolment_id = r2.enrolment_id
     WHERE e2.student_id = s.student_id) AS overall_avg
FROM students s
JOIN programmes p ON s.programme_id = p.programme_id
WHERE s.student_id IN (
    SELECT DISTINCT e.student_id
    FROM enrolments e
    JOIN results r ON e.enrolment_id = r.enrolment_id
    WHERE r.grade = 'F'
)
ORDER BY overall_avg ASC;

-- Query 4: Departmental Teaching Workload & Distinction Rate
SELECT 
    d.department_code,
    d.department_name,
    CONCAT(l.first_name, ' ', l.last_name) AS lecturer_name,
    COUNT(DISTINCT co.offering_id) AS offerings_taught,
    COUNT(e.enrolment_id) AS total_students_evaluated,
    SUM(CASE WHEN r.grade = 'A' THEN 1 ELSE 0 END) AS distinctions_awarded,
    ROUND((SUM(CASE WHEN r.grade = 'A' THEN 1 ELSE 0 END) / COUNT(e.enrolment_id)) * 100, 1) AS distinction_percentage
FROM departments d
JOIN lecturers l ON d.department_id = l.department_id
JOIN course_offerings co ON l.lecturer_id = co.lecturer_id
JOIN enrolments e ON co.offering_id = e.offering_id
JOIN results r ON e.enrolment_id = r.enrolment_id
GROUP BY d.department_code, d.department_name, l.lecturer_id, l.first_name, l.last_name
ORDER BY d.department_code, distinction_percentage DESC;
