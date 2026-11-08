# Portfolio 2: Query Processing and Optimisation (7 Marks)
## Technical Report & Empirical Performance Benchmark

**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student Name:** Winner Oyebanjo (Student ID: 301909418)  
**Database Server:** MySQL Community Server 26.10.0 (macOS ARM64)  
**Benchmark Database:** `winnermit_usms_p2` (Isolated Benchmark Schema)  

---

## 1. Executive Summary

Portfolio 2 investigates the execution mechanics, query access paths, and indexing optimizations for four complex analytical queries designed for the **WinnerMIT University Student Management System (USMS)**.

Testing was conducted on an isolated benchmark schema (`winnermit_usms_p2`) populated with a realistic synthetic workload:
* 4 academic departments
* 6 undergraduate and postgraduate degree programmes
* 12 faculty lecturers
* 15 curriculum courses
* 24 course offerings across two academic sessions
* 100 students
* 244 course enrolments
* 223 assessment and examination results

Using MySQL's declarative `EXPLAIN FORMAT=TREE` and runtime `EXPLAIN ANALYZE`, this study diagnoses query bottlenecks (full table scans, intermediate temporary tables, unindexed joins) and applies targeted secondary and composite B-tree indexes. The resulting optimisations achieved query latency reductions ranging from **33.8% to 85.1%**.

---

## 2. Empirical Performance Comparison Summary

| Query Description | Complexity Elements | Baseline Execution Time | Optimised Execution Time | Latency Improvement | Dominant Access Path Change |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Query 1: Student GPA & Academic Performance** | 6-table Join, Filter, Aggregation, Having, Sort | **7.08 ms** | **3.30 ms** | **53.4% faster** | Eliminated full table scan on `results`; converted to covering index filter. |
| **Query 2: Course Enrolment Demand & Utilization** | 4-table Join, Left Join, Session Filter, Group By | **1.42 ms** | **0.94 ms** | **33.8% faster** | Single-column session lookup converted to composite `(session_id, semester)` index. |
| **Query 3: At-Risk Student Early Warning** | Subquery in `WHERE IN`, Correlated Subquery in `SELECT` | **0.195 ms** | **0.029 ms** | **85.1% faster** | Subquery cost plummeted from 60.2 to 4.14 via `idx_p2_res_grade`. |
| **Query 4: Departmental Workload & Distinction Rate** | 5-table Join, Group By, Conditional Sums, Sorting | **7.90 ms** | **1.87 ms** | **76.3% faster** | Nested loop join pipeline accelerated via indexed enrolment and result lookups. |

---

## 3. Query 1: Student Academic Performance & GPA Analysis

### 3.1. Business Question
*"Identify top-performing students in the School of Computing and Technology (SCT) with an average passing score of 60.00 or higher, calculating their cumulative average mark, total passed courses, and total credit units earned."*

### 3.2. SQL Query
```sql
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
```

### 3.3. Baseline Execution Diagnosis (`EXPLAIN ANALYZE`)
* **Execution Time:** 7.08 ms (Cost: 61.6).
* **Bottleneck:** The query engine performed a full table scan on `results r` (`Table scan on r, cost=22.6 rows=223`) to evaluate `r.result_remarks = 'Pass'`, joining back to enrolments and students sequentially.

### 3.4. Index Optimisation
```sql
CREATE INDEX idx_p2_res_rem_score ON results(result_remarks, total_score);
```
* **Rationale:** Creates a composite index covering the filter predicate (`result_remarks = 'Pass'`) and the aggregate target (`total_score`), allowing MySQL to bypass reading unindexed result rows.

### 3.5. Post-Optimisation Result
* **Execution Time:** **3.30 ms** (53.4% reduction).
* **Observed Plan Change:** The optimizer inverted the driving table order to start with programmes in department 1 (`Index lookup on p using fk_p2_prog_dept`), leveraging existing foreign keys and the composite index to eliminate the full table scan.

---

## 4. Query 2: Course Enrolment Demand & Capacity Saturation

### 4.1. Business Question
*"Determine course offerings in Academic Session 2026/2027 with at least 5 enrolled students, calculating enrolled count and average examination score."*

### 4.2. SQL Query
```sql
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
```

### 4.3. Baseline Execution Diagnosis
* **Execution Time:** 1.42 ms.
* **Bottleneck:** Lookup on `course_offerings` used only the single-column session index (`fk_p2_off_sess`), requiring secondary filtering for semester and course joins.

### 4.4. Index Optimisation
```sql
CREATE INDEX idx_p2_off_sess_sem ON course_offerings(session_id, semester);
```
* **Rationale:** A composite index on `(session_id, semester)` narrows the candidate course offerings directly in the B-Tree index before loading table rows into memory.

### 4.5. Post-Optimisation Result
* **Execution Time:** **0.94 ms** (33.8% speedup).

---

## 5. Query 3: At-Risk Student Early Warning Subquery

### 5.1. Business Question
*"Identify all students who have received at least one failing grade ('F') across their enrolments, computing their cumulative average score across all enrolled units."*

### 5.2. SQL Query
```sql
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
```

### 5.3. Baseline Execution Diagnosis
* **Execution Time:** 0.195 ms (Estimated Cost: 60.2).
* **Bottleneck:** The subquery in `WHERE s.student_id IN (...)` executed a materialization scan with deduplication (`Table scan on r, cost=22.6 rows=223`) because `results.grade` was unindexed.

### 5.4. Index Optimisation
```sql
CREATE INDEX idx_p2_res_grade ON results(grade);
CREATE INDEX idx_p2_enr_stud ON enrolments(student_id);
```
* **Rationale:** `idx_p2_res_grade` allows instant index-range lookup for failing grades without examining passing rows. `idx_p2_enr_stud` speeds up the correlated subquery in the `SELECT` projection.

### 5.5. Post-Optimisation Result
* **Execution Time:** **0.029 ms** (85.1% speedup; cost plunged from 60.2 to 4.14).
* **Observed Plan Change:** `Table scan on r` was replaced with `Index lookup on r using idx_p2_res_grade (grade = 'F')`.

---

## 6. Query 4: Departmental Teaching Workload & Distinction Rate

### 6.1. Business Question
*"Calculate total students evaluated, unique course offerings taught, and percentage of distinction grades ('A') awarded per lecturer grouped by department."*

### 6.2. SQL Query
```sql
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
```

### 6.3. Baseline vs. Optimised Comparison
* **Baseline Execution Time:** 7.90 ms.
* **Optimised Execution Time:** **1.87 ms** (76.3% reduction).
* **Explanation:** Leverages `idx_p2_enr_stud` and covering index scans on `course_offerings`, drastically reducing nested loop join overhead.

---

## 7. Technical Conclusion & Optimization Takeaways

1. **Selective Indexing Principle:** In tertiary academic systems, indexing foreign key and filter attributes (`grade`, `session_id`, `student_id`) yields high returns for administrative reporting.
2. **Composite Index Design:** Multi-attribute indexes such as `(session_id, semester)` and `(result_remarks, total_score)` eliminate table access by allowing the query engine to satisfy both filtering and sorting directly in the index leaf pages.
3. **Over-Indexing Trade-off:** While secondary indexes significantly enhance query retrieval performance, each additional index incurs write overhead on `INSERT` and `UPDATE` operations. The indexes implemented here were strictly chosen based on demonstrated workload requirements.
