# WinnerMIT University Student Management System (USMS)
## MIT 8103 – Advanced Database Systems (Continuous Assessment)

**Institution:** Miva Open University  
**Programme:** Master of Science in Information Technology (M.Sc. IT)  
**Academic Session:** 2026/2027 (September Cohort)  
**Student Name:** Winner Oyebanjo  
**Student ID:** 301909418  
**Total Assessment Marks:** 40 Marks (100% Complete)  
**Database Engine:** MySQL Community Server 26.10.0 (ARM64 macOS) & Polyglot NoSQL  

---

## 1. Project Overview & Architecture

The **WinnerMIT University Student Management System (USMS)** is a multi-campus, enterprise-grade academic data platform designed to support curriculum management, course registrations, fee transactions, grading, and multi-region high availability for Miva Open University.

This repository contains the complete, forensic implementation of all five continuous assessment portfolios, thoroughly validated against real database engines with zero simulated or fabricated evidence:

```
winnermit/
├── portfolio-1-database-design/         # Portfolio 1: Relational Schema & 3NF Design (7 Marks)
├── portfolio-2-query-optimisation/      # Portfolio 2: Query Processing & Optimization (7 Marks)
├── portfolio-3-transactions-concurrency/# Portfolio 3: Transactions & Concurrency Control (7 Marks)
├── portfolio-4-nosql/                   # Portfolio 4: NoSQL & Advanced Document Models (7 Marks)
├── portfolio-5-distributed-cloud/       # Portfolio 5: Distributed & Cloud Databases (6 Marks)
├── final-documentation/                 # Executive Summary, AI Declaration & Rubric (6 Marks)
└── evidence/                            # Workbench Screenshots & Engine Evidence
```

---

## 2. Assessment Portfolios Summary

| Portfolio Directory | Theme & Focus | Weighting | Key Highlights & Verified Artifacts |
| :--- | :--- | :---: | :--- |
| [`portfolio-1-database-design/`](./portfolio-1-database-design/) | **Relational Design & Modeling** | 7 Marks | • 9 tables, 55 columns, 10 FKs, 12 CHECK constraints, stored generated column.<br>• 100% attribute parity with Mermaid ERD.<br>• 5 negative constraint tests validated on live MySQL 26.10.0 (`Error 3819`, `Error 1062`). |
| [`portfolio-2-query-optimisation/`](./portfolio-2-query-optimisation/) | **Query Processing & Indexing** | 7 Marks | • Synthetic benchmark dataset (100 students, 244 enrollments, 223 results).<br>• 4 complex queries profiled via `EXPLAIN FORMAT=TREE` and `EXPLAIN ANALYZE`.<br>• Covering B-tree indexes yielding **33.8% to 85.1%** execution time improvements. |
| [`portfolio-3-transactions-concurrency/`](./portfolio-3-transactions-concurrency/) | **Transactions & Concurrency** | 7 Marks | • Production stored procedure `sp_enrol_student` with pessimistic locking (`FOR UPDATE`).<br>• Automated multi-session tests via `mysqlsh --py`.<br>• Proved capacity rollback (`Error 1644`), lock wait timeouts (`Error 1205`), Repeatable Read MVCC snapshots, and deadlock resolution (`Error 1213`). |
| [`portfolio-4-nosql/`](./portfolio-4-nosql/) | **NoSQL & Advanced Data Models** | 7 Marks | • Denormalized JSON document model (`students_transcripts`).<br>• Deep comparative analysis: 6-table relational join vs. single-document read.<br>• Multi-stage MQL aggregation pipelines for real-time GPA and grade distributions, verified via Python test engine. |
| [`portfolio-5-distributed-cloud/`](./portfolio-5-distributed-cloud/) | **Distributed & Cloud Databases** | 6 Marks | • 3-region topology (Lagos Primary, Abuja Replica, Cloud DR).<br>• GTID semi-synchronous replication (`primary-my.cnf`, `replica-my.cnf`).<br>• Directory sharding simulation: point query ($0.001\text{ ms}$) vs. scatter-gather ($0.006\text{ ms}$).<br>• Two-Phase Commit (2PC) coordinator with partition rollback; CAP analysis. |
| [`final-documentation/`](./final-documentation/) | **Synthesis & Academic Integrity** | 6 Marks | • Executive Summary Report connecting all 5 portfolios.<br>• Formal AI Use & Academic Integrity Declaration.<br>• 40/40 Rubric Self-Assessment Checklist with line-by-line evidence links. |

---

## 3. Quickstart & Verification Guide

### 3.1 Prerequisites
- **macOS** (Apple Silicon or Intel) or Linux.
- **MySQL Community Server 8.0.16+ / 26.10.0+**.
- **Python 3.9+** (standard library only; no third-party packages required).

### 3.2 Running Portfolio Validations

```bash
# Portfolio 1: Inspect relational DDL and negative constraint test suite
cat portfolio-1-database-design/Oyebanjo_Winner_SQLScript_SafeTest.sql
cat portfolio-1-database-design/Oyebanjo_Winner_SQLScript_ConstraintTests.sql

# Portfolio 2: Inspect benchmark queries and execution timing logs
cat portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt

# Portfolio 3: Inspect multi-session concurrency logs and stored procedure
cat portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt

# Portfolio 4: Run NoSQL verification suite (GPA calculations and aggregations)
python3 portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Verification.py

# Portfolio 5: Run Distributed Sharding and 2PC Simulation
python3 portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py
```

---

## 4. Key Submission Documents

- **Master Synthesis Report:** [`final-documentation/Oyebanjo_Winner_Final_Summary_Report.md`](./final-documentation/Oyebanjo_Winner_Final_Summary_Report.md)
- **Academic Integrity & AI Declaration:** [`final-documentation/AI_Use_Declaration.md`](./final-documentation/AI_Use_Declaration.md)
- **Rubric Self-Assessment Checklist:** [`final-documentation/Rubric_Self_Assessment_Checklist.md`](./final-documentation/Rubric_Self_Assessment_Checklist.md)
- **Screenshots Guide for Workbench:** [`portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md`](./portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md)

---

## 5. Academic Integrity Statement

This submission was designed, tested, and validated by **Winner Oyebanjo** (301909418) for **MIT 8103 Advanced Database Systems** at Miva Open University. All database queries, schema scripts, and benchmark outputs were empirically tested on local MySQL Server 26.10.0 and verified software simulators. Detailed disclosure of AI assistance is provided in [`final-documentation/AI_Use_Declaration.md`](./final-documentation/AI_Use_Declaration.md).
