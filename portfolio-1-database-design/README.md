# Portfolio 1: Database Design and Modelling (7 Marks)
**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student:** Winner Oyebanjo (ID: 301909418)  
**Case Study:** WinnerMIT University Student Management System (USMS)  

---

## Portfolio Overview

Portfolio 1 establishes the enterprise relational database foundation for the WinnerMIT University Student Management System (USMS). It models tertiary academic administration across nine relational entities, enforcing strict referential integrity, domain constraints, and automated grading calculations.

### Contents in this Directory
1. **`Oyebanjo_Winner_SQLScript.sql`**: Master MySQL 8/26 creation script for production database `winnermit_usms`.
2. **`Oyebanjo_Winner_SQLScript_SafeTest.sql`**: Isolated, non-destructive test script validated against `winnermit_usms_test`.
3. **`Oyebanjo_Winner_SQLScript_ConstraintTests.sql`**: Negative test suite demonstrating engine-level constraint enforcement.
4. **`Oyebanjo_Winner_Verification_Queries.sql`**: 5 multi-table analytical and validation queries.
5. **`Oyebanjo_Winner_ERD.md`**: Mermaid Entity Relationship Diagram with 100% attribute parity (55 attributes).
6. **`Oyebanjo_Winner_Database_Testing_Report.md`**: Technical verification report with live MySQL 26.10.0 execution outputs.
7. **`Oyebanjo_Winner_Screenshots_Guide.md`**: Step-by-step checklist for capturing the 6 MySQL Workbench screenshots into `evidence/`.
8. **`Oyebanjo_Winner_Portfolio1_Submission.md`**: Master academic submission document for Portfolio 1.

### Verified Architecture Highlights
* **Storage Engine:** InnoDB.
* **Character Set & Collation:** `utf8mb4` with `utf8mb4_0900_ai_ci`.
* **Foreign Keys:** 10 foreign keys with `ON UPDATE CASCADE ON DELETE RESTRICT`.
* **Check Constraints:** 12 active check constraints enforcing scores, dates, statuses, and domains.
* **Generated Column:** `total_score` calculated and stored automatically via `(assessment_score + examination_score)`.
* **3NF Justification:** Formal defence of storing Academic Board-awarded grades and remarks to preserve historical transcripts.
