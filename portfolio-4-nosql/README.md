# Portfolio 4: NoSQL & Advanced Data Models (Document Database)

**Course:** MIT 8103 – Advanced Database Systems  
**Student Name:** Winner Oyebanjo  
**Student ID:** 301909418  
**Institution:** Miva Open University  
**Case Study:** WinnerMIT University Student Management System (USMS)  
**Marks Weighting:** 7 Marks  

---

## 1. Overview & Objectives

Portfolio 4 explores advanced non-relational data modeling using the document paradigm (MongoDB). While Portfolios 1–3 established a fully normalized (3NF) relational database in MySQL for ACID transaction processing, Portfolio 4 models student transcripts, nested course histories, and analytical aggregations as self-contained JSON documents.

This portfolio addresses:
1. **Document Data Modeling:** Designing a denormalized, hierarchical document schema (`students_transcripts`) capturing 1:N academic history relationships.
2. **Design Trade-offs:** Detailed comparative analysis between Relational (MySQL) and Document (MongoDB) models, evaluating Embedding vs. Referencing strategies.
3. **CRUD Operations:** Implementing insert, query, update, and array manipulation operations using MongoDB Query Language (MQL).
4. **Aggregation Framework:** Developing complex multi-stage aggregation pipelines for GPA computation, course grade distributions, and departmental performance metrics.
5. **Empirical Verification:** Executing and verifying all operations against the dataset using an automated verification suite.

---

## 2. Directory Contents

| File Name | Description |
| :--- | :--- |
| [`students_transcripts.json`](./students_transcripts.json) | Standalone JSON dataset containing rich, denormalized student transcript records with nested academic terms, courses, GPA, and extracurricular activities. |
| [`Oyebanjo_Winner_Portfolio4_CRUD.js`](./Oyebanjo_Winner_Portfolio4_CRUD.js) | Production MongoDB shell (`mongosh`) script demonstrating CRUD operations, array modifications (`$push`, `$set`), and indexing. |
| [`Oyebanjo_Winner_Portfolio4_Aggregations.js`](./Oyebanjo_Winner_Portfolio4_Aggregations.js) | Advanced MongoDB aggregation pipelines (`$unwind`, `$group`, `$project`, `$sort`) for GPA calculation, grade distribution, and departmental reporting. |
| [`Oyebanjo_Winner_Portfolio4_Verification.py`](./Oyebanjo_Winner_Portfolio4_Verification.py) | Python verification engine implementing MQL-compliant aggregation logic to simulate and validate all queries without requiring external MongoDB server installation. |
| [`Oyebanjo_Winner_Portfolio4_Execution_Results.txt`](./Oyebanjo_Winner_Portfolio4_Execution_Results.txt) | Captured execution logs and empirical outputs generated from the verification suite. |
| [`Oyebanjo_Winner_Portfolio4_Report.md`](./Oyebanjo_Winner_Portfolio4_Report.md) | Comprehensive 7-mark submission report covering design rationale, schema diagrams, comparative analysis, CRUD walkthrough, aggregation pipelines, and production recommendations. |

---

## 3. How to Run & Verify

### Option A: Using the Python Verification Suite (Self-Contained)
No external MongoDB daemon or connection is required:
```bash
python3 portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Verification.py
```
Output results are written to console and saved to [`Oyebanjo_Winner_Portfolio4_Execution_Results.txt`](./Oyebanjo_Winner_Portfolio4_Execution_Results.txt).

### Option B: Using MongoDB Shell (`mongosh`)
If an active MongoDB instance is available:
```bash
# 1. Import dataset
mongoimport --db winnermit_usms_nosql --collection students_transcripts --file portfolio-4-nosql/students_transcripts.json --jsonArray

# 2. Execute CRUD operations
mongosh winnermit_usms_nosql portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_CRUD.js

# 3. Execute Aggregation pipelines
mongosh winnermit_usms_nosql portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Aggregations.js
```

---

## 4. Key Highlights & Findings

- **Atomic Transcript Retrieval:** A single MQL `find({ "student_id": "MIT-2026-001" })` query retrieves the complete student record across 5 semesters, avoiding the 6-table relational `JOIN` required in MySQL.
- **Embedded Document Architecture:** Course enrollments, grades, and semester summaries are embedded directly within academic term objects, eliminating foreign key lookups for high-frequency portal reads.
- **Aggregation Power:** Multi-stage aggregation pipelines accurately reproduce CGPA calculations ($CGPA = \frac{\sum (credits \times grade\_points)}{\sum credits}$) dynamically using pipeline stages.
- **Hybrid Architecture Recommendation:** USMS is best architected as a **polyglot persistence system**: MySQL retains core ACID transactions (tuition payment, real-time course registration), while MongoDB powers high-throughput transcript viewing, mobile student portal feeds, and historical analytics.
