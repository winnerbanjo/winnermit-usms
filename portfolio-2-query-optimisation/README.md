# Portfolio 2: Query Processing and Optimisation (7 Marks)
**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student:** Winner Oyebanjo (ID: 301909418)  
**Case Study:** WinnerMIT University Student Management System (USMS)  

---

## Portfolio Overview

Portfolio 2 demonstrates practical query performance diagnosis, execution plan evaluation, and secondary index optimisation using MySQL's native `EXPLAIN FORMAT=TREE` and `EXPLAIN ANALYZE`.

Testing is carried out in an isolated benchmark schema (`winnermit_usms_p2`), leaving the Portfolio 1 reference schema (`winnermit_usms_test`) completely unaltered.

### Contents in this Directory
1. **`Oyebanjo_Winner_Portfolio2_Setup.sql`**: Isolated schema DDL for `winnermit_usms_p2`.
2. **`Oyebanjo_Winner_Portfolio2_Data.sql`**: Scaled synthetic dataset (4 depts, 6 programmes, 12 lecturers, 15 courses, 24 offerings, 100 students, 244 enrolments, 223 results).
3. **`generate_p2_data.py`**: Python script used to generate the synthetic benchmark data.
4. **`Oyebanjo_Winner_Portfolio2_Queries.sql`**: The 4 university analytical SQL queries.
5. **`run_p2_benchmarks.py`**: Automated runner executing `EXPLAIN` and `EXPLAIN ANALYZE` before and after indexing on MySQL 26.10.0.
6. **`Oyebanjo_Winner_Portfolio2_Execution_Plans.txt`**: Raw, unedited execution plans and timing logs captured directly from MySQL 26.10.0.
7. **`Oyebanjo_Winner_Portfolio2_Report.md`**: Master academic technical report detailing access path diagnoses, index rationale, and performance comparison tables.

### Key Performance Findings
* **Query 1 (GPA Ranking):** 7.08 ms $\rightarrow$ 3.30 ms (**53.4% faster**).
* **Query 2 (Course Demand):** 1.42 ms $\rightarrow$ 0.94 ms (**33.8% faster**).
* **Query 3 (At-Risk Subquery):** 0.195 ms $\rightarrow$ 0.029 ms (**85.1% faster**).
* **Query 4 (Staff Workload):** 7.90 ms $\rightarrow$ 1.87 ms (**76.3% faster**).
