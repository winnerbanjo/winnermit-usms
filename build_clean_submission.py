#!/usr/bin/env python3
"""
Staging and Packaging Script for Miva University MIT 8103 Continuous Assessment
Packages clean submission directory Oyebanjo_Winner_301909418 and creates Oyebanjo_Winner_301909418.zip
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
    # Root Files
    ("Oyebanjo_Winner_README.txt", "Oyebanjo_Winner_README.txt"),
    ("README.md", "Oyebanjo_Winner_Master_README.md"),

    # Portfolio 1
    ("portfolio-1-database-design/README.md", "Portfolio_1_Database_Design/Oyebanjo_Winner_Portfolio1_README.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Portfolio1_Submission.md", "Portfolio_1_Database_Design/Oyebanjo_Winner_Portfolio1_Submission.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript.sql", "Portfolio_1_Database_Design/Oyebanjo_Winner_SQLScript.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript_SafeTest.sql", "Portfolio_1_Database_Design/Oyebanjo_Winner_SQLScript_SafeTest.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_SQLScript_ConstraintTests.sql", "Portfolio_1_Database_Design/Oyebanjo_Winner_SQLScript_ConstraintTests.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_ERD.md", "Portfolio_1_Database_Design/Oyebanjo_Winner_ERD.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Database_Testing_Report.md", "Portfolio_1_Database_Design/Oyebanjo_Winner_Database_Testing_Report.md"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Verification_Queries.sql", "Portfolio_1_Database_Design/Oyebanjo_Winner_Verification_Queries.sql"),
    ("portfolio-1-database-design/Oyebanjo_Winner_Screenshots_Guide.md", "Portfolio_1_Database_Design/Oyebanjo_Winner_Screenshots_Guide.md"),

    # Portfolio 2
    ("portfolio-2-query-optimisation/README.md", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_README.md"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Report.md", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Report.md"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Setup.sql", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Setup.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Data.sql", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Data.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Queries.sql", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Queries.sql"),
    ("portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt"),
    ("portfolio-2-query-optimisation/generate_p2_data.py", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Data_Generator.py"),
    ("portfolio-2-query-optimisation/run_p2_benchmarks.py", "Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Benchmark_Runner.py"),

    # Portfolio 3
    ("portfolio-3-transactions-concurrency/README.md", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_README.md"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Report.md", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Report.md"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Setup.sql", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Setup.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Transactions.sql", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Transactions.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionA.sql", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_SessionA.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_SessionB.sql", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_SessionB.sql"),
    ("portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt"),
    ("portfolio-3-transactions-concurrency/run_p3_classic_concurrency.py", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Concurrency_Runner.py"),
    ("portfolio-3-transactions-concurrency/run_p3_transactions.py", "Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Transaction_Runner.py"),

    # Portfolio 4
    ("portfolio-4-nosql/README.md", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_README.md"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Report.md", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Report.md"),
    ("portfolio-4-nosql/students_transcripts.json", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Transcripts.json"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_CRUD.js", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_CRUD.js"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Aggregations.js", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Aggregations.js"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Verification.py", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Verification.py"),
    ("portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt", "Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Execution_Results.txt"),

    # Portfolio 5
    ("portfolio-5-distributed-cloud/README.md", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_README.md"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Report.md", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Report.md"),
    ("portfolio-5-distributed-cloud/primary-my.cnf", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Primary.cnf"),
    ("portfolio-5-distributed-cloud/replica-my.cnf", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Replica.cnf"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Replication.sql", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Replication.sql"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py"),
    ("portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt", "Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt"),

    # Final Documentation
    ("final-documentation/Oyebanjo_Winner_Final_Summary_Report.md", "Final_Documentation/Oyebanjo_Winner_Final_Summary_Report.md"),
    ("final-documentation/AI_Use_Declaration.md", "Final_Documentation/Oyebanjo_Winner_AI_Use_Declaration.md"),
    ("final-documentation/Rubric_Self_Assessment_Checklist.md", "Final_Documentation/Oyebanjo_Winner_Rubric_Checklist.md"),
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

# Create Evidence Log
evidence_dir = os.path.join(TARGET_DIR, "Evidence")
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
   - Detailed Log: Portfolio_1_Database_Design/Oyebanjo_Winner_Database_Testing_Report.md
   - Screenshot Guide: Portfolio_1_Database_Design/Oyebanjo_Winner_Screenshots_Guide.md

2. Portfolio 2: Query Optimization Benchmarks
   - Scaled Dataset: winnermit_usms_p2 (100 students, 244 enrolments, 223 results)
   - Cost Models & Latency: EXPLAIN FORMAT=TREE and EXPLAIN ANALYZE
   - Speedups Verified: 33.8% to 85.1% latency reduction
   - Raw Query Plans: Portfolio_2_Query_Optimisation/Oyebanjo_Winner_Portfolio2_Execution_Plans.txt

3. Portfolio 3: Transactions & Concurrency Control
   - Multi-Session Engine: mysqlsh --py (mysql.get_classic_session)
   - Scenarios Tested: Capacity rollback (Error 1644), Lock wait timeout (Error 1205),
     Repeatable Read MVCC consistent snapshot, Deadlock victim rollback (Error 1213)
   - Raw Session Telemetry: Portfolio_3_Transactions_Concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt

4. Portfolio 4: NoSQL Document Aggregations
   - Dataset: 8 rich multi-term student transcript documents
   - Verified Aggregations: Dynamic GPA calculation, grade distributions, pass rates
   - Execution Log: Portfolio_4_NoSQL_Advanced_Data_Models/Oyebanjo_Winner_Portfolio4_Execution_Results.txt

5. Portfolio 5: Distributed Sharding & 2PC Simulation
   - Router Latency: Point query (0.001 ms) vs. Scatter-gather (0.006 ms)
   - Two-Phase Commit: Verified commit atomicity and simulated partition rollback
   - Execution Log: Portfolio_5_Distributed_Cloud_Databases/Oyebanjo_Winner_Portfolio5_Execution_Logs.txt

================================================================================
""")
print("  [CREATED] Evidence/Oyebanjo_Winner_Evidence_Log.txt")

# Verify all staged filenames satisfy the naming convention: Oyebanjo_Winner_DocumentType.extension
print("\nVerifying naming conventions in staged directory...")
invalid_names = []
for root, dirs, files in os.walk(TARGET_DIR):
    for f in files:
        if not f.startswith("Oyebanjo_Winner_"):
            invalid_names.append(os.path.join(root, f))

if invalid_names:
    print("ERROR: Found files not matching 'Oyebanjo_Winner_' prefix:")
    for bad in invalid_names:
        print("  - ", bad)
    raise ValueError("Naming convention check failed!")
else:
    print("SUCCESS: 100% of files in staging directory satisfy 'Oyebanjo_Winner_*.extension' naming rule.")

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
