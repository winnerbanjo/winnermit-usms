#!/usr/bin/env python3
"""
MIVA MIT 8103 - OFFICIAL SUBMISSION STAGING AND PACKAGING SUITE
Author: Winner Oyebanjo (Student ID: 301909418)
Packages clean submission directory Oyebanjo_Winner_301909418 and builds Oyebanjo_Winner_301909418.zip
"""

import os
import shutil
import zipfile

WORKSPACE = "/Users/oyekunle/Downloads/winnermit"
STAGING_ROOT = os.path.join(WORKSPACE, "staging_submission")
TARGET_DIR = os.path.join(STAGING_ROOT, "Oyebanjo_Winner_301909418")
FINAL_ZIP = os.path.join(WORKSPACE, "Oyebanjo_Winner_301909418.zip")

# Ensure clean staging directory
if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)
os.makedirs(TARGET_DIR, exist_ok=True)

# File mapping: (source_relative_path, target_relative_path)
FILE_MAP = [
    # Top-Level Root Documents
    ("Oyebanjo_Winner_README.txt", "Oyebanjo_Winner_README.txt"),
    ("README.md", "Oyebanjo_Winner_Master_README.md"),

    # Portfolio 1: Database Design & Modeling
    ("portfolio-1-database-design/README.md", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Portfolio1_README.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Portfolio1_Submission.md", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Portfolio1_Submission.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript.sql", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_SQLScript.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript_SafeTest.sql", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_SQLScript_SafeTest.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript_ConstraintTests.sql", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_SQLScript_ConstraintTests.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_ERD.md", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_ERD.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Database_Testing_Report.md", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Database_Testing_Report.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Verification_Queries.sql", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Verification_Queries.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md", "Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Screenshots_Guide.md"),

    # Portfolio 2: Query Processing & Index Optimization
    ("portfolio-2-query-optimisation/README.md", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_README.md"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Report.md", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Report.md"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Setup.sql", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Setup.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Data.sql", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Data.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Queries.sql", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Queries.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt"),
    ("portfolio-2-query-optimisation/generate_p2_data.py", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Data_Generator.py"),
    ("portfolio-2-query-optimisation/run_p2_benchmarks.py", "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Benchmark_Runner.py"),

    # Portfolio 3: Transactions & Concurrency Control
    ("portfolio-3-transactions-concurrency/README.md", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_README.md"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Report.md"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Setup.sql", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Setup.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Transactions.sql", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Transactions.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionA.sql", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_SessionA.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionB.sql", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_SessionB.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt"),
    ("portfolio-3-transactions-concurrency/run_p3_classic_concurrency.py", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Concurrency_Runner.py"),
    ("portfolio-3-transactions-concurrency/run_p3_transactions.py", "Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Transaction_Runner.py"),

    # Portfolio 4: NoSQL & Advanced Data Models
    ("portfolio-4-nosql/README.md", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_README.md"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Report.md", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Report.md"),
    ("portfolio-4-nosql/students_transcripts.json", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Transcripts.json"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_CRUD.js", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_CRUD.js"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Aggregations.js", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Aggregations.js"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Verification.py", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Verification.py"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt", "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Execution_Results.txt"),

    # Portfolio 5: Distributed & Cloud Databases
    ("portfolio-5-distributed-cloud/README.md", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_README.md"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Report.md"),
    ("portfolio-5-distributed-cloud/primary-my.cnf", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Primary.cnf"),
    ("portfolio-5-distributed-cloud/replica-my.cnf", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Replica.cnf"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Replication.sql", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Replication.sql"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt", "Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt"),

    # Final Documentation & Synthesis
    ("final-documentation/Oyebanjo_Winner_Final_Summary_Report.md", "Oyebanjo_Winner_FinalDocumentation/Oyebanjo_Winner_Final_Summary_Report.md"),
    ("final-documentation/AI_Use_Declaration.md", "Oyebanjo_Winner_FinalDocumentation/Oyebanjo_Winner_AI_Use_Declaration.md"),
    ("final-documentation/Rubric_Self_Assessment_Checklist.md", "Oyebanjo_Winner_FinalDocumentation/Oyebanjo_Winner_Rubric_Checklist.md"),
]

print("Staging files into clean structure...")
for src_rel, dst_rel in FILE_MAP:
    src_path = os.path.join(WORKSPACE, src_rel)
    dst_path = os.path.join(TARGET_DIR, dst_rel)
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Missing source file: {src_path}")
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"  [COPIED] {src_rel} -> {dst_rel}")

# Fix relative file references in staged scripts so they run portably
staged_p4_verif = os.path.join(TARGET_DIR, "Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Verification.py")
with open(staged_p4_verif, "r", encoding="utf-8") as f:
    p4_code = f.read()

# Make path relative to script directory
p4_code = p4_code.replace(
    'DATA_FILE = "/Users/oyekunle/Downloads/winnermit/portfolio-4-nosql/students_transcripts.json"',
    'import os\nSCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))\nDATA_FILE = os.path.join(SCRIPT_DIR, "Oyebanjo_Winner_Portfolio4_Transcripts.json")\nif not os.path.exists(DATA_FILE):\n    DATA_FILE = os.path.join(SCRIPT_DIR, "students_transcripts.json")'
)
p4_code = p4_code.replace(
    'OUTPUT_FILE = "/Users/oyekunle/Downloads/winnermit/portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt"',
    'OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Oyebanjo_Winner_Portfolio4_Execution_Results.txt")'
)
with open(staged_p4_verif, "w", encoding="utf-8") as f:
    f.write(p4_code)
print("  [PATCHED] Portfolio 4 Verification paths relative in staged copy.")

staged_p2_gen = os.path.join(TARGET_DIR, "Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Data_Generator.py")
with open(staged_p2_gen, "r", encoding="utf-8") as f:
    p2_code = f.read()
p2_code = p2_code.replace(
    "with open('/Users/oyekunle/Downloads/winnermit/portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Data.sql', 'w') as f:",
    "import os\n    script_dir = os.path.dirname(os.path.abspath(__file__))\n    with open(os.path.join(script_dir, 'Oyebanjo_Winner_Portfolio2_Data.sql'), 'w') as f:"
)
with open(staged_p2_gen, "w", encoding="utf-8") as f:
    f.write(p2_code)
print("  [PATCHED] Portfolio 2 Data Generator paths relative in staged copy.")

# Create Evidence Log and Screenshots Status in Oyebanjo_Winner_Evidence/
evidence_dir = os.path.join(TARGET_DIR, "Oyebanjo_Winner_Evidence")
os.makedirs(evidence_dir, exist_ok=True)

evidence_log = os.path.join(evidence_dir, "Oyebanjo_Winner_Evidence_Log.txt")
with open(evidence_log, "w", encoding="utf-8") as f:
    f.write("""================================================================================
WINNERMIT USMS: EVIDENCE LOG & BENCHMARK AUDIT TRAIL
Student: Winner Oyebanjo (301909418) | MIT 8103 Advanced Database Systems
================================================================================

This directory records empirical verification evidence across all 5 portfolios:

1. Portfolio 1: Relational Schema & Negative Constraints
   - Engine: MySQL Community Server 26.10.0 (ARM64 macOS)
   - Tested Database: winnermit_usms_test
   - Constraint Errors Verified: Error 3819 (Score > 100), Error 1062 (Duplicate PK)
   - Detailed Log: Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Database_Testing_Report.md
   - Screenshot Guide: Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Screenshots_Guide.md
   - Screenshots Audit Status: See Oyebanjo_Winner_Screenshots_Status_Report.md

2. Portfolio 2: Query Optimization Benchmarks
   - Scaled Dataset: winnermit_usms_p2 (100 students, 244 enrolments, 223 results)
   - Cost Models & Latency: EXPLAIN FORMAT=TREE and EXPLAIN ANALYZE
   - Speedups Verified: 33.8% to 85.1% latency reduction
   - Raw Query Plans: Oyebanjo_Winner_Portfolio2/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt

3. Portfolio 3: Transactions & Concurrency Control
   - Multi-Session Engine: mysqlsh --py (mysql.get_classic_session)
   - Scenarios Tested: Capacity rollback (Error 1644), Lock wait timeout (Error 1205),
     Repeatable Read MVCC consistent snapshot, Deadlock victim rollback (Error 1213)
   - Raw Session Telemetry: Oyebanjo_Winner_Portfolio3/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt

4. Portfolio 4: NoSQL Document Aggregations
   - Dataset: 8 rich multi-term student transcript documents
   - Verified Aggregations: Dynamic GPA calculation, grade distributions, pass rates
   - Execution Log: Oyebanjo_Winner_Portfolio4/Oyebanjo_Winner_Portfolio4_Execution_Results.txt
   - Environment Note: Verified using Python aggregation engine against JSON dataset.

5. Portfolio 5: Distributed Sharding & 2PC Simulation
   - Router Latency: Point query (0.001 ms) vs. Scatter-gather (0.006 ms)
   - Two-Phase Commit: Verified commit atomicity and simulated partition rollback
   - Execution Log: Oyebanjo_Winner_Portfolio5/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt
   - Environment Note: Multi-campus GTID configuration and failover SQL verified via 2PC simulator.

================================================================================
""")
print("  [CREATED] Oyebanjo_Winner_Evidence/Oyebanjo_Winner_Evidence_Log.txt")

screenshots_report = os.path.join(evidence_dir, "Oyebanjo_Winner_Screenshots_Status_Report.md")
with open(screenshots_report, "w", encoding="utf-8") as f:
    f.write("""# Portfolio 1: MySQL Workbench Screenshots Audit & Verification Status

**Student Name:** Winner Oyebanjo (Student ID: 301909418)  
**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  

---

## 1. Screenshot Audit Status

In accordance with academic integrity guidelines, automated GUI screen capture tools were not utilized to synthesize or simulate graphical evidence. The required 6 figures should be captured directly by the candidate from MySQL Workbench connected to `winnermit_usms_test`:

| Screenshot Figure | Target View / SQL Query in MySQL Workbench | Status | Primary Supplementary Text Evidence |
| :--- | :--- | :---: | :--- |
| **figure1_schemas_overview.png** | Schemas navigator panel showing `winnermit_usms_test` and all 9 tables. | *Manual Capture Required* | Documented in `Oyebanjo_Winner_Portfolio1/Oyebanjo_Winner_Database_Testing_Report.md` (Section 3). |
| **figure2_table_row_counts.png** | Query: `SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.tables WHERE table_schema='winnermit_usms_test';` | *Manual Capture Required* | Server output confirmed and recorded in `Oyebanjo_Winner_Database_Testing_Report.md` (Table Deployment Matrix). |
| **figure3_student_roster_join.png** | Query: `SELECT s.student_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name, p.programme_code FROM students s JOIN programmes p ON s.programme_id = p.programme_id;` | *Manual Capture Required* | Server output confirmed in `Oyebanjo_Winner_Verification_Queries.sql`. |
| **figure4_student_grade_sheet.png** | Query: `SELECT * FROM results LIMIT 10;` showing generated `total_score` and `grade`. | *Manual Capture Required* | Verified in `Oyebanjo_Winner_Database_Testing_Report.md` (Section 4). |
| **figure5_capacity_utilization.png** | Query: `SELECT co.offering_id, c.course_code, co.capacity, COUNT(e.enrolment_id) AS enrolled FROM course_offerings co LEFT JOIN enrolments e ON co.offering_id = e.offering_id GROUP BY co.offering_id, c.course_code, co.capacity;` | *Manual Capture Required* | Verified in `Oyebanjo_Winner_Portfolio2_Execution_Plans.txt` and `Oyebanjo_Winner_Database_Testing_Report.md`. |
| **figure6_negative_constraint_rejection.png** | Workbench query editor showing `Error 3819: Check constraint 'chk_results_exam' is violated.` | *Manual Capture Required* | Verified with live error output in `Oyebanjo_Winner_Database_Testing_Report.md` (Negative Test 1). |

---

## 2. Technical Recommendation
All underlying SQL queries and constraint triggers execute cleanly on MySQL Server 26.10.0. The candidate may capture the above 6 images from MySQL Workbench and save them into `Oyebanjo_Winner_Evidence/` if required by the course grader.
""")
print("  [CREATED] Oyebanjo_Winner_Evidence/Oyebanjo_Winner_Screenshots_Status_Report.md")

# Verify all staged filenames satisfy the naming convention: Oyebanjo_Winner_DocumentType.extension
print("\nVerifying naming conventions in staged directory...")
invalid_names = []
for root, dirs, files in os.walk(TARGET_DIR):
    for f in files:
        if not f.startswith("Oyebanjo_Winner_"):
            invalid_names.append(os.path.join(root, f))
    for d in dirs:
        if not d.startswith("Oyebanjo_Winner_"):
            invalid_names.append(os.path.join(root, d))

if invalid_names:
    print("ERROR: Found files or folders not matching 'Oyebanjo_Winner_' prefix:")
    for bad in invalid_names:
        print("  - ", bad)
    raise ValueError("Naming convention check failed!")
else:
    print("SUCCESS: 100% of files and folders in staging directory satisfy 'Oyebanjo_Winner_*' naming rule.")

# Package into ZIP archive
print(f"\nBuilding final submission ZIP: {FINAL_ZIP}...")
if os.path.exists(FINAL_ZIP):
    os.remove(FINAL_ZIP)

with zipfile.ZipFile(FINAL_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(STAGING_ROOT):
        for file in files:
            full_path = os.path.join(root, file)
            # relative path inside zip starting with Oyebanjo_Winner_301909418/
            rel_path = os.path.relpath(full_path, STAGING_ROOT)
            zipf.write(full_path, rel_path)

zip_size_mb = os.path.getsize(FINAL_ZIP) / (1024 * 1024)
print(f"Archive successfully created: {FINAL_ZIP}")
print(f"Total ZIP size: {zip_size_mb:.2f} MB (Must be < 100 MB: {'PASS' if zip_size_mb < 100 else 'FAIL'})")

# Inspect ZIP root structure
print("\nVerifying ZIP top-level folder structure...")
with zipfile.ZipFile(FINAL_ZIP, "r") as zipf:
    top_levels = set()
    file_count = 0
    for name in zipf.namelist():
        file_count += 1
        parts = name.split("/")
        if parts:
            top_levels.add(parts[0])

print(f"Total files in archive: {file_count}")
print(f"Top-level directories in archive: {top_levels}")
if top_levels == {"Oyebanjo_Winner_301909418"}:
    print("SUCCESS: ZIP strictly contains single top-level folder 'Oyebanjo_Winner_301909418'.")
else:
    print("WARNING: Top-level folder mismatch:", top_levels)
