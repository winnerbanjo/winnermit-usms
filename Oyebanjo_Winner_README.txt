================================================================================
MIVA OPEN UNIVERSITY | FACULTY OF COMPUTING & APPLIED SCIENCES
MIT 8103: ADVANCED DATABASE SYSTEMS (CONTINUOUS ASSESSMENT)
ACADEMIC SESSION: 2026/2027 (SEPTEMBER COHORT) | TOTAL MARKS: 40
================================================================================

STUDENT INFORMATION:
- Student Name:   Winner Oyebanjo
- Student ID:     301909418
- Programme:      Master of Science in Information Technology (M.Sc. IT)
- Course:         MIT 8103 – Advanced Database Systems
- Target Degree:  Miva Open University
- Submission Date: November 2026
- Case Study:     WinnerMIT University Student Management System (USMS)
- Primary Database: MySQL Community Server 26.10.0 / 8.0.16+ (InnoDB Engine)
- GitHub Repo:    https://github.com/winnerbanjo/winnermit-usms (Private)
- Assessor Access: GitHub User 'winnerbanjo' | Email: winnerbanjochannel@gmail.com

================================================================================
TABLE OF CONTENTS
================================================================================
1. Case Study Overview (WinnerMIT USMS)
2. Submission Structure & Mandatory Naming Conventions
3. Portfolio 1: Database Design & Relational Modeling (7 Marks)
4. Portfolio 2: Query Processing & Index Optimization (7 Marks)
5. Portfolio 3: Transactions & Concurrency Control (7 Marks)
6. Portfolio 4: NoSQL & Advanced Document Models (7 Marks)
7. Portfolio 5: Distributed & Cloud Databases (6 Marks)
8. Final Synthesis & Executive Summary (6 Marks)
9. Step-by-Step Instructions to Reproduce Practical Demonstrations
10. Testing, Verification & Empirical Evidence Summary
11. Academic References
12. Formal Academic Integrity & AI-Use Declaration

================================================================================
1. CASE STUDY OVERVIEW (WINNERMIT USMS)
================================================================================
The WinnerMIT University Student Management System (USMS) is an enterprise 
academic data platform engineered to manage student admissions, degree 
programmes, academic departments, faculty appointments, semester curriculum 
offerings, course registrations, examination results, and multi-campus 
distribution (Lagos Main Campus, Abuja Northern Campus, and Global Online Learning).

The system addresses the dual needs of:
a) Strict relational ACID integrity for billing, enrollment caps, and certified 
   transcripts.
b) High-throughput read scaling and polyglot persistence (NoSQL/Distributed) 
   for real-time student portal dashboards and analytics.

================================================================================
2. SUBMISSION STRUCTURE & MANDATORY NAMING CONVENTIONS
================================================================================
Per the official Miva MIT 8103 continuous assessment instructions:
- Top-Level Archive: Oyebanjo_Winner_301909418.zip
- Main Directory inside ZIP: Oyebanjo_Winner_301909418/
- Standalone Readme: Oyebanjo_Winner_README.txt
- Every assignment file follows the format: Oyebanjo_Winner_DocumentType.extension

DIRECTORY & FILE INVENTORY:
Oyebanjo_Winner_301909418/
│
├── Oyebanjo_Winner_README.txt                        (Master Assignment Overview)
├── Oyebanjo_Winner_Master_README.md                   (Markdown Portal Document)
│
├── Portfolio_1_Database_Design/                      (7 Marks)
│   ├── Oyebanjo_Winner_Portfolio1_README.md          (Module Guide)
│   ├── Oyebanjo_Winner_Portfolio1_Submission.md      (Academic Design Document)
│   ├── Oyebanjo_Winner_SQLScript.sql                 (Master DDL & DML Schema)
│   ├── Oyebanjo_Winner_SQLScript_SafeTest.sql        (Isolated Verification DDL)
│   ├── Oyebanjo_Winner_SQLScript_ConstraintTests.sql (5 Negative Tests)
│   ├── Oyebanjo_Winner_ERD.md                        (Mermaid ERD Diagram)
│   ├── Oyebanjo_Winner_Database_Testing_Report.md    (Empirical Test Logs)
│   ├── Oyebanjo_Winner_Verification_Queries.sql      (Analytical Reporting SQL)
│   └── Oyebanjo_Winner_Screenshots_Guide.md          (Workbench Capture Checklist)
│
├── Portfolio_2_Query_Optimisation/                   (7 Marks)
│   ├── Oyebanjo_Winner_Portfolio2_README.md          (Module Guide)
│   ├── Oyebanjo_Winner_Portfolio2_Report.md          (Optimization Benchmark Report)
│   ├── Oyebanjo_Winner_Portfolio2_Setup.sql          (Benchmark Schema DDL)
│   ├── Oyebanjo_Winner_Portfolio2_Data.sql           (Synthetic Scaled Dataset)
│   ├── Oyebanjo_Winner_Portfolio2_Queries.sql        (4 Analytical Queries)
│   ├── Oyebanjo_Winner_Portfolio2_Execution_Plans.txt (EXPLAIN ANALYZE Logs)
│   ├── Oyebanjo_Winner_Portfolio2_Data_Generator.py  (Data Synthesis Engine)
│   └── Oyebanjo_Winner_Portfolio2_Benchmark_Runner.py (Automated Profiler)
│
├── Portfolio_3_Transactions_Concurrency/             (7 Marks)
│   ├── Oyebanjo_Winner_Portfolio3_README.md          (Module Guide)
│   ├── Oyebanjo_Winner_Portfolio3_Report.md          (Concurrency & Locking Report)
│   ├── Oyebanjo_Winner_Portfolio3_Setup.sql          (Concurrency Test Schema)
│   ├── Oyebanjo_Winner_Portfolio3_Transactions.sql   (ACID sp_enrol_student)
│   ├── Oyebanjo_Winner_Portfolio3_SessionA.sql       (Dual-Session Client A Script)
│   ├── Oyebanjo_Winner_Portfolio3_SessionB.sql       (Dual-Session Client B Script)
│   ├── Oyebanjo_Winner_Portfolio3_Execution_Logs.txt (Live Session Telemetry)
│   ├── Oyebanjo_Winner_Portfolio3_Concurrency_Runner.py (Classic Multi-Session Harness)
│   └── Oyebanjo_Winner_Portfolio3_Transaction_Runner.py (X-Protocol Driver)
│
├── Portfolio_4_NoSQL_Advanced_Data_Models/           (7 Marks)
│   ├── Oyebanjo_Winner_Portfolio4_README.md          (Module Guide)
│   ├── Oyebanjo_Winner_Portfolio4_Report.md          (Comparative Paradigm Report)
│   ├── Oyebanjo_Winner_Portfolio4_Transcripts.json   (Denormalized JSON Dataset)
│   ├── Oyebanjo_Winner_Portfolio4_CRUD.js            (MongoDB Shell CRUD Operations)
│   ├── Oyebanjo_Winner_Portfolio4_Aggregations.js    (MQL Multi-Stage Pipelines)
│   ├── Oyebanjo_Winner_Portfolio4_Verification.py    (Python Verification Engine)
│   └── Oyebanjo_Winner_Portfolio4_Execution_Results.txt (Verified Output Logs)
│
├── Portfolio_5_Distributed_Cloud_Databases/          (6 Marks)
│   ├── Oyebanjo_Winner_Portfolio5_README.md          (Module Guide)
│   ├── Oyebanjo_Winner_Portfolio5_Report.md          (Distributed Topology Report)
│   ├── Oyebanjo_Winner_Portfolio5_Primary.cnf        (Lagos Primary MySQL Config)
│   ├── Oyebanjo_Winner_Portfolio5_Replica.cnf        (Abuja Replica MySQL Config)
│   ├── Oyebanjo_Winner_Portfolio5_Replication.sql    (GTID & Failover Script)
│   ├── Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py (2PC & Sharding Simulator)
│   └── Oyebanjo_Winner_Portfolio5_Execution_Logs.txt (Simulation Verification Logs)
│
├── Final_Documentation/                              (6 Marks)
│   ├── Oyebanjo_Winner_Final_Summary_Report.md       (2-3 Page Executive Synthesis)
│   ├── Oyebanjo_Winner_AI_Use_Declaration.md         (Academic Integrity Disclosure)
│   └── Oyebanjo_Winner_Rubric_Checklist.md           (40/40 Evidence Matrix)
│
└── Evidence/                                         (Screenshots & Logs)
    └── Oyebanjo_Winner_Evidence_Log.txt              (Audit Trail & Capture Notes)

================================================================================
3. PORTFOLIO 1: DATABASE DESIGN & RELATIONAL MODELING (7 MARKS)
================================================================================
- Relational Schema: 9 core entities (departments, programmes, lecturers, 
  students, courses, course_prerequisites, course_offerings, enrolments, results).
- Total Attributes: 55 attributes, 10 foreign keys with referential actions 
  (ON DELETE RESTRICT / CASCADE), 12 CHECK constraints, and 1 stored generated 
  column (total_score = continuous_assessment + examination).
- Third Normal Form (3NF) Justification: Complete decomposition avoiding transitive 
  dependencies. The stored grade and remarks in 'results' preserve historical 
  integrity against future grading scale changes, adhering strictly to 3NF.
- Constraint Verification: 5 negative tests executed on live MySQL 26.10.0:
  1. Score > 100 rejected by chk_results_exam (Error 3819).
  2. Duplicate student_id rejected by PRIMARY KEY (Error 1062).
  3. Invalid email format rejected by chk_students_email (Error 3819).
  4. End date before start date rejected by chk_offerings_dates (Error 3819).
  5. Enrolling without course prerequisite rejected by FK integrity (Error 1452).

================================================================================
4. PORTFOLIO 2: QUERY PROCESSING & INDEX OPTIMIZATION (7 MARKS)
================================================================================
- Scaled Dataset: Isolated database 'winnermit_usms_p2' with 100 students, 
  244 enrollments, and 223 grade results.
- 4 Complex Analytical Queries Profiled with EXPLAIN FORMAT=TREE & EXPLAIN ANALYZE:
  • Query 1 (GPA Ranking & Window Functions):
    - Optimization: Added composite index idx_results_student_total(student_id, total_score, offering_id).
    - Gain: Execution time dropped from 7.08 ms to 3.30 ms (53.4% faster).
  • Query 2 (Course Demand & Enrollment Utilization):
    - Optimization: Added composite index idx_offerings_course_semester.
    - Gain: Execution time dropped from 1.42 ms to 0.94 ms (33.8% faster).
  • Query 3 (At-Risk Academic Warning Subquery):
    - Optimization: Added covering index idx_results_student_offering.
    - Gain: Execution time dropped from 0.195 ms to 0.029 ms (85.1% faster).
  • Query 4 (Faculty Workload Analysis across Departments):
    - Optimization: Added composite index idx_lecturers_dept_status.
    - Gain: Execution time dropped from 7.90 ms to 1.87 ms (76.3% faster).

================================================================================
5. PORTFOLIO 3: TRANSACTIONS & CONCURRENCY CONTROL (7 MARKS)
================================================================================
- Stored Procedure: 'sp_enrol_student' in 'winnermit_usms_p3' implementing 
  pessimistic row-level locking (SELECT ... FOR UPDATE) and atomic state checks.
- Dual-Session Empirical Demonstrations:
  • Demo 1 (Atomic Capacity Rollback): Course capacity of 2/2 seats strictly 
    enforced. Session B rejected with Error 1644: 'Course offering is at maximum capacity'.
  • Demo 2 (Lock Contention & Timeout): Exclusive lock held by Session A caused 
    Session B to block and safely abort with Error 1205: 'Lock wait timeout exceeded'.
  • Demo 3 (Repeatable Read MVCC Snapshot): Session A observed consistent 
    enrollment counts under Repeatable Read isolation regardless of concurrent 
    commits in Session B.
  • Demo 4 (Deadlock Handling): Opposing-sequence updates induced InnoDB graph 
    cycle detection and victim transaction rollback (Error 1213).

================================================================================
6. PORTFOLIO 4: NOSQL & ADVANCED DATA MODELS (7 MARKS)
================================================================================
- Document Schema: Denormalized JSON model ('students_transcripts') capturing 
  nested terms, courses, grades, credits, GPA, and academic honors.
- Relational vs. Document Paradigm Analysis: Proved that retrieving a complete 
  student transcript requires a 6-table JOIN in MySQL, whereas MongoDB resolves 
  the query in a single disk read (O(1)) via find({ "student_id": "MIT-2026-001" }).
- Aggregations: Developed MQL aggregation pipelines ($unwind, $group, $project, $sort) 
  calculating semester GPA, cumulative CGPA, course pass/fail rates, and 
  departmental performance metrics.
- Verification: Validated through automated test suite with verified output logs.

================================================================================
7. PORTFOLIO 5: DISTRIBUTED & CLOUD DATABASES (6 MARKS)
================================================================================
- Multi-Campus Architecture: 3-region topology comprising Lagos Main Campus 
  (Primary Source), Abuja Northern Campus (Semi-Sync Replica), and Cloud 
  Managed Infrastructure (Disaster Recovery).
- MySQL GTID Semi-Synchronous Replication: Configured primary-my.cnf and 
  replica-my.cnf with GTID auto-positioning, ROW binary logging, and semi-sync 
  acknowledgement guaranteeing Zero Data Loss (RPO = 0).
- Sharding & Two-Phase Commit (2PC): Implemented directory-based departmental 
  sharding. Single-shard point query latency measured at 0.001 ms vs. 0.006 ms 
  for multi-shard scatter-gather. Simulated 2PC coordinator ensuring complete 
  rollback when a participating shard is partitioned/offline.
- CAP Theorem Strategic Trade-off: CP chosen for course registration (consistency 
  prevents seat over-allocation); AP chosen for student portal reads (availability 
  ensures 100% portal uptime during network partitions).

================================================================================
8. FINAL SYNTHESIS & EXECUTIVE SUMMARY (6 MARKS)
================================================================================
- 2-3 page executive summary synthesizing Portfolios 1-5, case study findings, 
  architectural comparisons, and engineering reflections.
- Formal AI use disclosure and academic integrity compliance.
- 40/40 rubric self-assessment matrix linking every grading criterion to specific 
  code lines and execution evidence.

================================================================================
9. STEP-BY-STEP INSTRUCTIONS TO REPRODUCE PRACTICAL DEMONSTRATIONS
================================================================================

PREREQUISITES:
- Operating System: macOS (Apple Silicon/Intel), Linux, or Windows.
- MySQL Community Server: Version 8.0.16 or later (Tested on MySQL 26.10.0).
- Python: Version 3.9 or higher (standard library).

REPRODUCTION STEPS:

1. Portfolio 1 (Database Creation & Negative Constraint Tests):
   $ mysql -u root -p < Portfolio_1_Database_Design/Oyebanjo_Winner_SQLScript_SafeTest.sql
   $ mysql -u root -p < Portfolio_1_Database_Design/Oyebanjo_Winner_SQLScript_ConstraintTests.sql

2. Portfolio 2 (Query Optimization Benchmarking):
   $ python3 Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Benchmark_Runner.py
   (Examine EXPLAIN ANALYZE plans in Oyebanjo_Winner_Portfolio2_Execution_Plans.txt)

3. Portfolio 3 (Transactions & Concurrency Multi-Session Testing):
   $ python3 Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Concurrency_Runner.py
   (Inspect transaction isolation and lock timeouts in Oyebanjo_Winner_Portfolio3_Execution_Logs.txt)

4. Portfolio 4 (NoSQL Document Aggregations Verification):
   $ python3 Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Verification.py
   (Inspect GPA and distribution results in Oyebanjo_Winner_Portfolio4_Execution_Results.txt)

5. Portfolio 5 (Distributed Sharding, 2PC & CAP Simulation):
   $ python3 Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py
   (Inspect routing and 2PC logs in Oyebanjo_Winner_Portfolio5_Execution_Logs.txt)

================================================================================
10. TESTING, VERIFICATION & EMPIRICAL EVIDENCE SUMMARY
================================================================================
All practical work was executed against active MySQL 26.10.0 database instances 
and verified simulation software. No outputs or query plans were simulated:
- Portfolio 1: 9 tables verified, 5 negative constraints tested with actual errors.
- Portfolio 2: 4 queries profiled on 100 students/244 enrolments; speedups 33.8% to 85.1%.
- Portfolio 3: Real multi-session concurrency tested (Errors 1644, 1205, 1213 verified).
- Portfolio 4: MQL aggregation pipeline verified on 8 multi-semester transcript documents.
- Portfolio 5: GTID replication configs and 2PC failure rollback verified.

================================================================================
11. ACADEMIC REFERENCES
================================================================================
1. Date, C. J. (2019). Database Design and Relational Theory: Normal Forms and 
   All That Jazz. 2nd Edition. O'Reilly Media.
2. Elmasri, R., & Navathe, S. B. (2021). Fundamentals of Database Systems. 
   7th Edition. Pearson Education.
3. Kleppmann, M. (2017). Designing Data-Intensive Applications: The Big Ideas 
   Behind Reliable, Scalable, and Maintainable Systems. O'Reilly Media.
4. MySQL AB. (2026). MySQL 8.0 Reference Manual: InnoDB Storage Engine, 
   Replication, and Optimization. Oracle Corporation.
5. MongoDB Inc. (2026). The MongoDB Aggregation Framework and Data Modeling 
   Guide. MongoDB Documentation.

================================================================================
12. FORMAL ACADEMIC INTEGRITY & AI-USE DECLARATION
================================================================================
I, Winner Oyebanjo (Student ID: 301909418), declare that this submission is my 
original work for MIT 8103 Advanced Database Systems at Miva Open University.

Generative AI tools (Google DeepMind Antigravity and OpenAI ChatGPT) were utilized 
for syntax scaffolding, script generation, and documentation drafting. All 
underlying architecture decisions, database queries, constraint tests, execution 
plans, and concurrency harnesses were reviewed, executed, and verified by me 
on live database engines. Full disclosure is provided in 
Final_Documentation/Oyebanjo_Winner_AI_Use_Declaration.md.

Student: Winner Oyebanjo (301909418)
Miva Open University | Faculty of Computing & Applied Sciences
================================================================================
