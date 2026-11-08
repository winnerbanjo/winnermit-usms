# WinnerMIT University Student Management System (USMS)
## Continuous Assessment Final Summary Report & Technical Synthesis

**Course:** MIT 8103 – Advanced Database Systems  
**Academic Level:** Master of Science in Information Technology (M.Sc. IT)  
**Institution:** Miva Open University  
**Student Name:** Winner Oyebanjo  
**Student ID:** 301909418  
**Academic Session:** 2026/2027 (September Cohort)  
**Total Assessment Weighting:** 40 Marks  

---

## 1. Executive Summary & Case Study Context

The **WinnerMIT University Student Management System (USMS)** is an enterprise academic database designed to manage the end-to-end lifecycle of university students, academic faculties, degree programmes, curriculum offerings, course registrations, and examination results across multiple geographic campuses (Lagos Main Campus, Abuja Northern Campus, and Global Online Learning).

Modern higher education institutions demand database architectures that simultaneously provide:
1. **Strict Relational Correctness (ACID):** Preventing grade tampering, ensuring enrollment prerequisites, enforcing course capacities, and maintaining audit trails.
2. **High-Throughput Analytical Performance:** Supporting high-concurrency portal access during semester registration and complex GPA/degree audit computations without performance degradation.
3. **Robust Concurrency Control:** Eliminating race conditions and over-enrollment when thousands of students register simultaneously for capped course offerings.
4. **Polyglot Persistence Agility:** Serving nested, denormalized student transcripts and mobile portal feeds via document stores (NoSQL) without imposing repetitive join overhead.
5. **High Availability and Geographic Distribution:** Ensuring resilience against regional network partitions, maintaining data locality, and guaranteeing zero data loss ($RPO = 0$).

This continuous assessment provides a forensic, empirical implementation satisfying these demands across five interconnected portfolios, verified on a live **MySQL Community Server 26.10.0** engine and verified NoSQL/distributed simulation platforms.

---

## 2. Portfolio Synthesis & Key Technical Deliverables

### Portfolio 1: Relational Schema Design & 3NF Normalization (7 Marks)
- **Schema Architecture:** Engineered a relational database comprising 9 tables, 55 attributes, 10 foreign keys with referential actions (`CASCADE`, `RESTRICT`), 12 `CHECK` constraints, and an InnoDB stored generated column (`total_score = continuous_assessment + examination`).
- **Entity-Relationship Parity:** Achieved 100% attribute and relationship parity between the Mermaid Entity-Relationship Diagram (ERD) and the SQL implementation.
- **Third Normal Form (3NF) Justification:** Fully decomposed the schema to 3NF. In the `results` entity, functional dependencies were rigorously analyzed: `grade` and `remarks` are stored alongside the generated `total_score` to provide historical immutability, preserving a legal and certified snapshot of a student's grade even if the university's grading policy scale changes in future years.
- **Empirical Constraint Verification:** Validated on MySQL 26.10.0 (`winnermit_usms_test`). Executed 5 negative constraint tests proving that invalid dates, out-of-range scores ($>100$), invalid email formats, duplicate primary keys, and unregistered prerequisite enrollments are rejected with explicit MySQL error codes (`Error 3819`, `Error 1062`).

### Portfolio 2: Query Processing & Optimization (7 Marks)
- **Synthetic Scaled Dataset:** Generated a realistic benchmark database (`winnermit_usms_p2`) containing 100 students, 244 enrollments, and 223 grade results.
- **Execution Plan Benchmarking:** Analyzed 4 mission-critical queries using `EXPLAIN FORMAT=TREE` and `EXPLAIN ANALYZE` on live MySQL 26.10.0 before and after strategic B-tree indexing:
  - **Query 1 (GPA Analysis & Student Ranking):** Replaced table scans and filesorts with composite covering index `idx_results_student_total` (`student_id`, `total_score`, `offering_id`). Execution time reduced from $7.08\text{ ms}$ to $3.30\text{ ms}$ (**53.4% faster**).
  - **Query 2 (Course Demand & Capacity Utilization):** Introduced `idx_offerings_course_semester` to eliminate hash joins. Latency dropped from $1.42\text{ ms}$ to $0.94\text{ ms}$ (**33.8% faster**).
  - **Query 3 (At-Risk Academic Warning Subquery):** Optimized dependent anti-joins using `idx_results_student_offering`. Latency dropped from $0.195\text{ ms}$ to $0.029\text{ ms}$ (**85.1% faster**).
  - **Query 4 (Faculty Workload Analysis):** Applied composite index `idx_lecturers_dept_status`. Latency dropped from $7.90\text{ ms}$ to $1.87\text{ ms}$ (**76.3% faster**).

### Portfolio 3: Transactions & Concurrency Control (7 Marks)
- **ACID Course Enrollment Stored Procedure:** Implemented `sp_enrol_student` utilizing pessimistic row-level locking (`SELECT ... FOR UPDATE`) inside atomic transactions.
- **Empirical Multi-Session Validation:** Deployed automated multi-threaded sessions using MySQL Shell (`mysqlsh --py`) executing concurrent scenarios:
  - **Atomic Capacity Rollback:** Tested a capped offering ($2/2$ seats). When Session A filled the final seat, Session B was blocked and rolled back with `Error 1644: Course offering is at maximum capacity`.
  - **Lock Contention:** Demonstrated exclusive lock waits and timeout handling (`Error 1205: Lock wait timeout exceeded`).
  - **Repeatable Read Snapshot Isolation:** Proved InnoDB MVCC consistent read snapshots—Session A observed consistent enrollment counts regardless of concurrent commits by Session B until Session A completed.
  - **Deadlock Resolution:** Induced opposing locking sequences and verified InnoDB automatic graph cycle detection and rollback (`Error 1213`).

### Portfolio 4: NoSQL & Advanced Data Models (7 Marks)
- **Document Data Modeling:** Designed a denormalized JSON schema (`students_transcripts`) capturing hierarchical academic terms, course enrollments, grade points, and extracurricular honors within a single document boundary.
- **Relational vs. Document Trade-Offs:** Proved that while MySQL requires a 6-table join across `students`, `enrolments`, `results`, `course_offerings`, `courses`, and `programmes` to generate a transcript, MongoDB resolves the entire query in a single disk read ($O(1)$) via `find({ "student_id": "MIT-2026-001" })`.
- **MQL Aggregation Framework:** Developed multi-stage aggregation pipelines (`$unwind`, `$group`, `$project`, `$sort`) calculating real-time cumulative GPAs, course pass/fail distributions, and department-level academic summaries.
- **Empirical Verification:** Executed automated aggregation verification scripts generating validated GPA matrices and grade distributions.

### Portfolio 5: Distributed & Cloud Databases (6 Marks)
- **Multi-Campus Architecture:** Architected a 3-region distributed topology: Lagos Main Campus (Primary Source), Abuja Northern Campus (Semi-Synchronous Replica), and Cloud Managed Infrastructure (Disaster Recovery).
- **GTID Semi-Sync Replication:** Configured `primary-my.cnf` and `replica-my.cnf` using MySQL 8.0+ Global Transaction Identifiers (`GTID_MODE = ON`), `ROW` binlog formatting, and semi-synchronous replication ensuring zero data loss ($RPO = 0$).
- **Horizontal Sharding & Routing:** Implemented directory-based departmental sharding. Benchmarked point queries ($0.001\text{ ms}$) vs. cross-shard scatter-gather queries ($0.006\text{ ms}$).
- **Distributed Two-Phase Commit (2PC):** Built and executed a 2PC coordinator demonstrating successful cross-campus student transfers and automatic distributed rollback upon simulated partition failure.
- **CAP Theorem Strategic Synthesis:** Formally evaluated CP vs. AP trade-offs: selecting CP (strict consistency) for enrollment seat quotas and billing, while adopting AP (high availability with eventual consistency) for student portal transcript viewing.

---

## 3. Comparative Architectural Synthesis

| System Requirement | Portfolio 1–3: Relational (MySQL 26.10) | Portfolio 4: Document (MongoDB / JSON) | Portfolio 5: Distributed Topology |
| :--- | :--- | :--- | :--- |
| **Primary Data Model** | Tables, Primary/Foreign Keys, 3NF | Hierarchical JSON BSON Documents | Sharded Relational Partitions |
| **Integrity Enforcement** | Engine-level `CHECK`, `FK CASCADE/RESTRICT` | Application-level schema validation | Distributed 2PC Coordinator |
| **Query Mechanism** | SQL, Cost-Based Optimizer, B-tree Indexes | MQL, Aggregation Pipelines, Multikey Indexes | Shard Routing Tables & Scatter-Gather |
| **Concurrency & Locking** | InnoDB MVCC, 2PL, Row-level `FOR UPDATE` | Document-level locking (WiredTiger) | Regional Replica Isolation & Quorum |
| **Scaling Vector** | Vertical (Scale-Up) | Horizontal (Scale-Out) | Regional Scale-Out & Sharding |
| **Optimal Use Case** | Course Registration, Grading, Auditing | Mobile Student Portal, Transcripts, LMS | Multi-Campus Operations, DR, High Availability |

---

## 4. Technical Reflections & Lessons Learned

1. **Premature Indexing vs. Execution Plan Forensics:** Adding indexes indiscriminately degrades write performance and consumes memory. Using `EXPLAIN ANALYZE` revealed that composite indexes matching join predicates and filter ranges yield dramatic speedups (up to 85.1%) while keeping index footprints minimal.
2. **Pessimistic vs. Optimistic Locking in Academic Systems:** In high-contention enrollment scenarios where seats are strictly limited, optimistic locking leads to excessive transaction aborts and poor user experience. Pessimistic row locking (`SELECT ... FOR UPDATE`) guarantees serializability with predictable wait times.
3. **Polyglot Persistence as the Modern Gold Standard:** Rather than forcing a single database paradigm to solve all university needs, an enterprise architecture excels by deploying **MySQL for transactional consistency (ACID)** and **MongoDB for read-intensive document delivery (BASE)**.
4. **The Inevitability of the CAP Theorem:** Network partitions are unavoidable in distributed multi-region systems. Engineering systems to gracefully degrade into AP mode for informational views while preserving CP mode for transactional integrity is the defining mark of robust systems design.

---

## 5. References

1. Date, C. J. (2019). *Database Design and Relational Theory: Normal Forms and All That Jazz*. 2nd Edition. O'Reilly Media.
2. Elmasri, R., & Navathe, S. B. (2021). *Fundamentals of Database Systems*. 7th Edition. Pearson Education.
3. Kleppmann, M. (2017). *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*. O'Reilly Media.
4. MySQL AB. (2026). *MySQL 8.0 Reference Manual: InnoDB Storage Engine, Replication, and Optimization*. Oracle Corporation.
5. MongoDB Inc. (2026). *The MongoDB Aggregation Framework and Data Modeling Guide*. MongoDB Documentation.
