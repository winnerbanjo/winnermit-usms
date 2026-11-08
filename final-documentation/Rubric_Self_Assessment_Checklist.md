# MIT 8103 Continuous Assessment Rubric Self-Assessment Checklist

**Course:** MIT 8103 – Advanced Database Systems  
**Student Name:** Winner Oyebanjo  
**Student ID:** 301909418  
**Institution:** Miva Open University  
**Academic Session:** 2026/2027  
**Total Available Marks:** 40 Marks  
**Self-Assessed Score:** 40 / 40 Marks (100%)  

---

## Portfolio Breakdown & Evidence Mapping

### 1. Portfolio 1: Database Design & Implementation (7 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **Relational Data Modeling & ERD** | 2.0 | Complete | Full 9-entity relational model matching real university operations. 100% attribute parity with Mermaid ERD: [`portfolio-1-database-design/Oyebanjo_Winner_ERD.md`](../portfolio-1-database-design/Oyebanjo_Winner_ERD.md). |
| **Normalization Rationale (3NF)** | 1.5 | Complete | Detailed third normal form analysis explaining functional dependencies and immutable grade retention in [`portfolio-1-database-design/Oyebanjo_Winner_Portfolio1_Submission.md`](../portfolio-1-database-design/Oyebanjo_Winner_Portfolio1_Submission.md#4-normalisation-explanation). |
| **SQL Schema Implementation** | 2.0 | Complete | 9 tables, 55 columns, 10 foreign keys (`CASCADE`/`RESTRICT`), 12 `CHECK` constraints, InnoDB stored generated column (`total_score`) in [`portfolio-1-database-design/Oyebanjo_Winner_SQLScript_SafeTest.sql`](../portfolio-1-database-design/Oyebanjo_Winner_SQLScript_SafeTest.sql). |
| **Empirical Constraint Testing** | 1.5 | Complete | 5 isolated negative tests executed on live MySQL 26.10.0 with confirmed error codes (`Error 3819`, `Error 1062`) documented in [`portfolio-1-database-design/Oyebanjo_Winner_Database_Testing_Report.md`](../portfolio-1-database-design/Oyebanjo_Winner_Database_Testing_Report.md). Workbench screenshot guide in [`portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md`](../portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md). |
| **Subtotal** | **7.0 / 7.0** | | |

---

### 2. Portfolio 2: Query Processing & Optimization (7 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **Benchmark Dataset & Scaling** | 1.5 | Complete | Synthetic generator script populating 100 students, 244 enrollments, 223 results in isolated schema `winnermit_usms_p2` via [`portfolio-2-query-optimisation/generate_p2_data.py`](../portfolio-2-query-optimisation/generate_p2_data.py). |
| **Complex Analytical SQL Queries** | 1.5 | Complete | 4 complex analytical queries (GPA Ranking with Window Functions, Course Demand Aggregations, At-Risk Subqueries, Faculty Workload Analysis) in [`portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Queries.sql`](../portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Queries.sql). |
| **Query Plan Analysis (`EXPLAIN ANALYZE`)** | 2.0 | Complete | Full `EXPLAIN FORMAT=TREE` and `EXPLAIN ANALYZE` captured on live MySQL 26.10.0 engine before and after indexing in [`portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt`](../portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt). |
| **Indexing Strategy & Empirical Gains** | 2.0 | Complete | Composite covering B-tree indexes yielding verified execution time speedups between **33.8% and 85.1%** documented in [`portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Report.md`](../portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Report.md). |
| **Subtotal** | **7.0 / 7.0** | | |

---

### 3. Portfolio 3: Transactions & Concurrency Control (7 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **ACID Stored Procedure Implementation** | 2.0 | Complete | Production procedure `sp_enrol_student` implementing prerequisite validation, capacity checks, and atomic state transitions using pessimistic locking (`SELECT ... FOR UPDATE`) in [`portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionA.sql`](../portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionA.sql). |
| **Capacity Rollback Enforcement** | 1.5 | Complete | Live empirical verification of capacity limits ($2/2$ seats) rejecting concurrent over-subscription with `Error 1644` in [`portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt`](../portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt). |
| **Isolation & MVCC Snapshot Verification** | 1.5 | Complete | Verified Repeatable Read MVCC consistent snapshot isolation across independent database sessions during concurrent commits in [`portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md`](../portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md#demo-3-repeatable-read-isolation-and-snapshot-consistency). |
| **Lock Contention & Deadlock Handling** | 2.0 | Complete | Induced lock wait timeout (`Error 1205`) and opposing-order circular locks triggering InnoDB automated deadlock detection and victim rollback (`Error 1213`) in [`portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md`](../portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md#demo-4-concurrent-deadlock-detection-and-engine-resolution). |
| **Subtotal** | **7.0 / 7.0** | | |

---

### 4. Portfolio 4: NoSQL & Advanced Data Models (7 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **Document Schema Design** | 2.0 | Complete | Rich, hierarchical JSON document model capturing academic terms, courses, GPA, and honours in [`portfolio-4-nosql/students_transcripts.json`](../portfolio-4-nosql/students_transcripts.json). |
| **Relational vs. Document Analysis** | 1.5 | Complete | Deep comparative analysis evaluating Embedding vs. Referencing, join overhead (6-table relational join vs. single-document read), and polyglot persistence in [`portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Report.md`](../portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Report.md#3-comparative-analysis-relational-vs-document-model). |
| **MQL CRUD Operations** | 1.5 | Complete | Complete CRUD script with complex array operators (`$push`, `$set`), projection, and multikey indexing in [`portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_CRUD.js`](../portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_CRUD.js). |
| **Aggregation Framework & Verification** | 2.0 | Complete | Advanced multi-stage pipelines (`$unwind`, `$group`, `$project`, `$sort`) for GPA computation and pass/fail distributions in [`portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Aggregations.js`](../portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Aggregations.js), verified with empirical logs in [`portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt`](../portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt). |
| **Subtotal** | **7.0 / 7.0** | | |

---

### 5. Portfolio 5: Distributed & Cloud Databases (6 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **Multi-Campus Architecture & Topology** | 1.5 | Complete | 3-region distributed topology (Lagos Primary, Abuja Replica, Cloud DR) with Mermaid architecture diagram in [`portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md`](../portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md#2-distributed-architecture-design). |
| **MySQL Replication Configuration** | 1.5 | Complete | Enterprise configurations [`portfolio-5-distributed-cloud/primary-my.cnf`](../portfolio-5-distributed-cloud/primary-my.cnf), [`portfolio-5-distributed-cloud/replica-my.cnf`](../portfolio-5-distributed-cloud/replica-my.cnf), and SQL setup/failover script [`portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Replication.sql`](../portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Replication.sql). |
| **Sharding & Query Routing** | 1.5 | Complete | Departmental directory sharding simulator benchmarked single-shard ($0.001\text{ ms}$) vs. scatter-gather ($0.006\text{ ms}$) in [`portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt`](../portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt). |
| **Distributed 2PC & CAP Analysis** | 1.5 | Complete | Two-Phase Commit coordinator simulation demonstrating success and partition rollback; detailed CAP analysis (CP for registration vs. AP for portal feeds) in [`portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md`](../portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md#5-distributed-transactions-two-phase-commit-2pc). |
| **Subtotal** | **6.0 / 6.0** | | |

---

### 6. Final Documentation, Synthesis & Academic Integrity (6 Marks)

| Assessment Criteria | Marks | Status | Primary Evidence & File Links |
| :--- | :---: | :---: | :--- |
| **Executive Synthesis & Case Study Reflection** | 2.5 | Complete | High-level synthesis connecting all 5 portfolios, comparative paradigm matrix, and academic reflections in [`final-documentation/Oyebanjo_Winner_Final_Summary_Report.md`](./Oyebanjo_Winner_Final_Summary_Report.md). |
| **Academic Integrity & AI Use Declaration** | 1.5 | Complete | Transparent disclosure of AI assistance and student empirical verification in [`final-documentation/AI_Use_Declaration.md`](./AI_Use_Declaration.md). |
| **Rubric Compliance & Project Organization** | 2.0 | Complete | Modular repository layout with per-portfolio README files, empirical test evidence, and self-assessment checklist in [`final-documentation/Rubric_Self_Assessment_Checklist.md`](./Rubric_Self_Assessment_Checklist.md) and [`README.md`](../README.md). |
| **Subtotal** | **6.0 / 6.0** | | |

---

### Final Continuous Assessment Summary

$$\mathbf{Total\ Marks:\ 7.0 + 7.0 + 7.0 + 7.0 + 6.0 + 6.0 = 40.0\ /\ 40.0\ (100\%)}$$
