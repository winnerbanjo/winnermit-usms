# WinnerMIT University USMS — Portfolio 1 Evidence & Screenshot Guide

**Course:** MIT 8103 – Advanced Database Systems  
**Student Name:** Winner Oyebanjo (Student ID: 301909418)  
**Target Application:** MySQL Workbench (Connection: *WinnerMIT Local*)

This guide lists the exact screenshots you should capture from your computer for your **Continuous Assessment Portfolio 1** submission.

---

## Recommended Screenshots to Capture

### Screenshot 1: Successful Connection & Schemas Panel
* **What to Show:** MySQL Workbench connected to `WinnerMIT Local` (`127.0.0.1:3306`).
* **In the UI:** On the left **Navigator (Schemas)** panel, expand `winnermit_usms_test` (or `winnermit_usms`) to show the **Tables** folder with all nine tables:
  1. `academic_sessions`
  2. `course_offerings`
  3. `courses`
  4. `departments`
  5. `enrolments`
  6. `lecturers`
  7. `programmes`
  8. `results`
  9. `students`
* **Caption in Report:** *Figure 1: MySQL Workbench Navigator showing successful connection and all nine tables in the relational schema.*

---

### Screenshot 2: Table Row Counts & Deployment Audit
* **Query to Run:**
  ```sql
  USE winnermit_usms_test;

  SELECT 'departments' AS table_name, COUNT(*) AS total_rows FROM departments
  UNION ALL SELECT 'programmes', COUNT(*) FROM programmes
  UNION ALL SELECT 'students', COUNT(*) FROM students
  UNION ALL SELECT 'lecturers', COUNT(*) FROM lecturers
  UNION ALL SELECT 'courses', COUNT(*) FROM courses
  UNION ALL SELECT 'academic_sessions', COUNT(*) FROM academic_sessions
  UNION ALL SELECT 'course_offerings', COUNT(*) FROM course_offerings
  UNION ALL SELECT 'enrolments', COUNT(*) FROM enrolments
  UNION ALL SELECT 'results', COUNT(*) FROM results;
  ```
* **What to Show:** The query editor and the Output Result Grid displaying all nine table counts.
* **Caption in Report:** *Figure 2: Table deployment audit confirming record population across all nine entities.*

---

### Screenshot 3: Student Enrolment & Relational Roster Join
* **Query to Run:**
  ```sql
  USE winnermit_usms_test;

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
  ```
* **What to Show:** The joined result grid demonstrating referential integrity between students, programmes, offerings, courses, and lecturers (specifically showing undergraduate student Amaka Eze enrolled in `CSC2101`).
* **Caption in Report:** *Figure 3: Multi-table relational query demonstrating valid student enrolments across undergraduate and postgraduate programmes.*

---

### Screenshot 4: Academic Performance & Stored Generated Column Proof
* **Query to Run:**
  ```sql
  USE winnermit_usms_test;

  SELECT 
      s.student_number,
      CONCAT(s.first_name, ' ', s.last_name) AS student_name,
      c.course_code,
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
  ```
* **What to Show:** Result grid showing `assessment_score` + `examination_score` totaling `total_score` (83.00 and 70.00).
* **Caption in Report:** *Figure 4: Student grade sheet verifying MySQL InnoDB stored generated column calculation (total_score).*

---

### Screenshot 5: Negative Constraint Enforcement (Check Constraint Rejection)
* **Query to Run:**
  ```sql
  USE winnermit_usms_test;

  -- Test: Attempting to insert assessment score > 40
  INSERT INTO results (enrolment_id, assessment_score, examination_score, grade, result_remarks)
  VALUES (3, 45.00, 50.00, 'A', 'Pass');
  ```
* **What to Show:** The lower Action Output panel showing the red cross with error message:
  `Error Code: 3819. Check constraint 'chk_assessment_score' is violated.`
* **Caption in Report:** *Figure 5: Active enforcement of business constraints in MySQL 26.10, showing rejection of invalid assessment marks.*

---

### Screenshot 6: Foreign Key Constraint Rejection
* **Query to Run:**
  ```sql
  USE winnermit_usms_test;

  -- Test: Attempting to insert student with non-existent programme_id
  INSERT INTO students (programme_id, student_number, first_name, last_name, email, admission_date)
  VALUES (999, 'WMITTEST999', 'Fake', 'Student', 'fake@example.edu', '2026-09-01');
  ```
* **What to Show:** The lower Action Output panel showing error:
  `Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails...`
* **Caption in Report:** *Figure 6: Referential integrity test showing rejection of orphaned child records.*

---

## Summary of Files in Your Package for Submission

1. **`Oyebanjo_Winner_SQLScript.sql`** — Master MySQL 8 DDL database script.
2. **`Oyebanjo_Winner_SQLScript_SafeTest.sql`** — Non-destructive test script executed in `winnermit_usms_test`.
3. **`Oyebanjo_Winner_SQLScript_ConstraintTests.sql`** — Isolated negative constraint test suite.
4. **`Oyebanjo_Winner_Verification_Queries.sql`** — Verification and analytical queries.
5. **`Oyebanjo_Winner_ERD.md`** — Fully synchronized Mermaid ER diagram.
6. **`Oyebanjo_Winner_README.txt`** — System documentation, assumptions, and 3NF justifications.
7. **`Oyebanjo_Winner_Database_Testing_Report.md`** — Comprehensive testing and verification report.
8. **`Oyebanjo_Winner_Screenshots_Guide.md`** — Step-by-step submission evidence capture guide.
