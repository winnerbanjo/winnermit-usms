WINNER OYEBANJO
Student ID: 301909418
Course: MIT 8103 - Advanced Database Systems
Assessment: Continuous Assessment - September Cohort 2026
Portfolio: Portfolio 1 - Database Design and Modelling
Case Study: WinnerMIT University Student Management System

CONTENTS
1. Oyebanjo_Winner_SQLScript.sql
   Master MySQL 8/26 database creation script. It creates the WinnerMIT University
   Student Management System database, nine relational tables, keys,
   constraints, indexes and fictional sample records.

2. Oyebanjo_Winner_SQLScript_SafeTest.sql
   Non-destructive, isolated verification script targeting winnermit_usms_test.

3. Oyebanjo_Winner_SQLScript_ConstraintTests.sql
   Negative constraint test suite demonstrating engine-level enforcement.

4. Oyebanjo_Winner_Verification_Queries.sql
   Analytical queries, student rosters, transcripts and utilization reports.

5. Oyebanjo_Winner_ERD.md
   Entity Relationship Diagram (Mermaid format) and relationship explanations.

6. Oyebanjo_Winner_Database_Testing_Report.md
   Comprehensive testing report containing live execution logs and evidence.

7. Oyebanjo_Winner_Screenshots_Guide.md
   Step-by-step checklist of evidence screenshots to capture for submission.

8. Oyebanjo_Winner_Portfolio1_Submission.md
   Master academic submission report synthesizing design, normalisation,
   real MySQL test evidence, query demonstrations, and technical reflections.

HOW TO RUN THE SQL SCRIPT
1. Install and open MySQL Server and MySQL Workbench.
2. Connect to your local MySQL Server.
3. Open Oyebanjo_Winner_SQLScript.sql in MySQL Workbench.
4. Read the warning at the top of the script before executing it.
5. Execute the script, then refresh the Schemas panel.
6. Confirm that the winnermit_usms database and its nine tables exist.
7. Run the SELECT verification statements at the bottom of the script.
8. Capture your own screenshots showing successful execution and results.

IMPORTANT
The SQL script contains a DROP DATABASE statement for winnermit_usms.
Run it only in a development environment where you do not need to preserve
existing data. The sample records are fictional. This package is a prepared
starting implementation; it must be executed and checked on your computer.
Keep your screenshots and evidence of your own testing for the submission.

DESIGN ASSUMPTIONS
- Each student belongs to one programme in this simplified model.
- Each course offering has one assigned lecturer.
- A course is offered at most once per semester in a given academic session.
- A student can enrol in a given course offering only once.
- Each enrolment can have at most one result.
- Assessment is out of 40 and examination is out of 60.
- Grading and Normalisation Assumption:
  total_score is implemented as a stored generated column calculated from
  (assessment_score + examination_score). The grade and result_remarks
  attributes are intentionally stored rather than purely derived. This design
  decision reflects real-world university regulations where final letter grades
  and pass/fail remarks represent official academic board/senate determinations.
  Storing them preserves historical audit trails (protecting historical records
  against subsequent changes to grading scales or moderation adjustments) and
  permits discretionary grading overrides (e.g. aegrotat passes or special
  consideration) without violating 3NF, as documented under institutional business rules.

ACADEMIC INTEGRITY
Review, test and understand the submitted work. Acknowledge any external
sources and any AI assistance in accordance with Miva's instructions.
