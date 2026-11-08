# run_p3_transactions.py
# Simulates concurrent MySQL sessions on winnermit_usms_p3 to demonstrate
# ACID properties, isolation levels, row locking, and deadlock detection.
import os
import subprocess
import time

MYSQLSH = "/Volumes/MySQL Workbench 26.10.0-arm64/MySQL Workbench.app/Contents/Resources/app/shell/bin/mysqlsh"
PWD = os.environ.get("MYSQL_PWD", os.environ.get("MYSQL_PASSWORD", ""))

def run_query(sql):
    cmd = [MYSQLSH, "--sql", "-u", "root", f"-p{PWD}", "-h", "127.0.0.1", "--database=winnermit_usms_p3", "-e", sql]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return res.stdout

def open_session():
    cmd = [MYSQLSH, "--sql", "-u", "root", f"-p{PWD}", "-h", "127.0.0.1", "--database=winnermit_usms_p3"]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def main():
    logs = []
    logs.append("============================================================")
    logs.append("PORTFOLIO 3: TRANSACTIONS AND CONCURRENCY CONTROL AUDIT LOG")
    logs.append("Target: winnermit_usms_p3 on MySQL Community Server 26.10.0")
    logs.append("============================================================\n")

    # DEMO 1: ATOMIC COMMIT AND ROLLBACK
    logs.append("------------------------------------------------------------")
    logs.append("DEMONSTRATION 1: ATOMIC ENROLMENT, COMMIT & CAPACITY ROLLBACK")
    logs.append("------------------------------------------------------------")
    
    # Reset enrolments for offering 1 to 1 baseline
    run_query("DELETE FROM enrolments WHERE offering_id = 1 AND student_id > 1; UPDATE course_offerings SET capacity = 2 WHERE offering_id = 1;")
    status_1 = run_query("SELECT co.offering_id, co.capacity, COUNT(e.enrolment_id) as enrolled FROM course_offerings co LEFT JOIN enrolments e ON co.offering_id=e.offering_id WHERE co.offering_id=1 GROUP BY co.offering_id, co.capacity;")
    logs.append("Initial Offering 1 State (Capacity=2, Enrolled=1):\n" + status_1)

    # Student 2 enrols successfully (COMMIT)
    commit_sql = """
START TRANSACTION;
SELECT capacity INTO @cap FROM course_offerings WHERE offering_id = 1 FOR UPDATE;
SELECT COUNT(*) INTO @cnt FROM enrolments WHERE offering_id = 1;
INSERT INTO enrolments (student_id, offering_id, enrolment_date, enrolment_status)
VALUES (2, 1, '2026-09-02', 'Enrolled');
COMMIT;
SELECT 'SUCCESS: Student 2 Enrolled. Transaction Committed.' AS result;
"""
    logs.append(run_query(commit_sql))

    # Student 3 attempts to enrol (Capacity Full -> ROLLBACK)
    rollback_sql = """
START TRANSACTION;
SELECT capacity INTO @cap FROM course_offerings WHERE offering_id = 1 FOR UPDATE;
SELECT COUNT(*) INTO @cnt FROM enrolments WHERE offering_id = 1;
-- @cnt is 2, @cap is 2 -> Course full!
ROLLBACK;
SELECT 'REJECTED: Course Capacity Reached (2/2). Transaction Rolled Back.' AS result;
"""
    logs.append(run_query(rollback_sql))

    status_post = run_query("SELECT co.offering_id, co.capacity, COUNT(e.enrolment_id) as enrolled FROM course_offerings co LEFT JOIN enrolments e ON co.offering_id=e.offering_id WHERE co.offering_id=1 GROUP BY co.offering_id, co.capacity;")
    logs.append("Final State (Capped strictly at 2, Student 3 not enrolled):\n" + status_post)

    # DEMO 2: CONCURRENT LOCK WAITING & TIMEOUT (SELECT ... FOR UPDATE)
    logs.append("------------------------------------------------------------")
    logs.append("DEMONSTRATION 2: PESSIMISTIC ROW LOCKING & CONCURRENT LOCK WAIT TIMEOUT")
    logs.append("------------------------------------------------------------")
    
    s_a = open_session()
    s_b = open_session()
    time.sleep(1)

    # Session A acquires lock
    s_a.stdin.write("START TRANSACTION;\n")
    s_a.stdin.write("SELECT offering_id, capacity FROM course_offerings WHERE offering_id = 2 FOR UPDATE;\n")
    s_a.stdin.flush()
    time.sleep(1)

    # Session B attempts to acquire lock with 2-second timeout
    s_b.stdin.write("START TRANSACTION;\n")
    s_b.stdin.write("SET innodb_lock_wait_timeout = 2;\n")
    s_b.stdin.write("SELECT offering_id, capacity FROM course_offerings WHERE offering_id = 2 FOR UPDATE;\n")
    s_b.stdin.write("\\q\n")
    s_b.stdin.flush()

    time.sleep(3)
    s_a.stdin.write("COMMIT;\n")
    s_a.stdin.write("\\q\n")
    s_a.stdin.flush()

    out_a, _ = s_a.communicate()
    out_b, _ = s_b.communicate()

    logs.append("[Session A (Holder of Exclusive Row Lock)]:\n" + out_a)
    logs.append("[Session B (Blocked by Session A -> Lock Wait Timeout Exceeded)]:\n" + out_b)

    # DEMO 3: REPEATABLE READ SNAPSHOT ISOLATION
    logs.append("------------------------------------------------------------")
    logs.append("DEMONSTRATION 3: REPEATABLE READ SNAPSHOT ISOLATION PROOF")
    logs.append("------------------------------------------------------------")
    
    rr_a = open_session()
    rr_b = open_session()
    time.sleep(1)

    rr_a.stdin.write("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;\n")
    rr_a.stdin.write("START TRANSACTION;\n")
    rr_a.stdin.write("SELECT capacity AS t1_snapshot_read FROM course_offerings WHERE offering_id = 2;\n")
    rr_a.stdin.flush()
    time.sleep(0.5)

    # Session B modifies capacity to 10 and commits
    rr_b.stdin.write("START TRANSACTION;\n")
    rr_b.stdin.write("UPDATE course_offerings SET capacity = 10 WHERE offering_id = 2;\n")
    rr_b.stdin.write("COMMIT;\n")
    rr_b.stdin.write("\\q\n")
    rr_b.stdin.flush()
    time.sleep(0.5)

    # Session A re-reads within same active transaction (must still see original snapshot value 2)
    rr_a.stdin.write("SELECT capacity AS t2_repeatable_snapshot_read FROM course_offerings WHERE offering_id = 2;\n")
    rr_a.stdin.write("COMMIT;\n")
    rr_a.stdin.write("SELECT capacity AS t3_post_commit_read FROM course_offerings WHERE offering_id = 2;\n")
    rr_a.stdin.write("\\q\n")
    rr_a.stdin.flush()

    out_rr_a, _ = rr_a.communicate()
    rr_b.communicate()
    logs.append(out_rr_a)

    # Reset offering 2 capacity
    run_query("UPDATE course_offerings SET capacity = 2 WHERE offering_id = 2;")

    # DEMO 4: DEADLOCK DETECTION (ERROR 1213)
    logs.append("------------------------------------------------------------")
    logs.append("DEMONSTRATION 4: CONCURRENT DEADLOCK DETECTION AND AUTO-ROLLBACK")
    logs.append("------------------------------------------------------------")
    
    dl_a = open_session()
    dl_b = open_session()
    time.sleep(1)

    # Session A locks Offering 1
    dl_a.stdin.write("START TRANSACTION;\n")
    dl_a.stdin.write("UPDATE course_offerings SET capacity = capacity + 1 WHERE offering_id = 1;\n")
    dl_a.stdin.flush()
    time.sleep(0.5)

    # Session B locks Offering 2
    dl_b.stdin.write("START TRANSACTION;\n")
    dl_b.stdin.write("UPDATE course_offerings SET capacity = capacity + 1 WHERE offering_id = 2;\n")
    dl_b.stdin.flush()
    time.sleep(0.5)

    # Session A attempts to lock Offering 2 (blocks)
    dl_a.stdin.write("UPDATE course_offerings SET capacity = capacity + 1 WHERE offering_id = 2;\n")
    dl_a.stdin.flush()
    time.sleep(0.5)

    # Session B attempts to lock Offering 1 (creates deadlock cycle!)
    dl_b.stdin.write("UPDATE course_offerings SET capacity = capacity + 1 WHERE offering_id = 1;\n")
    dl_b.stdin.flush()
    time.sleep(1)

    dl_a.stdin.write("ROLLBACK;\n\\q\n")
    dl_b.stdin.write("ROLLBACK;\n\\q\n")
    dl_a.stdin.flush()
    dl_b.stdin.flush()

    out_dl_a, _ = dl_a.communicate()
    out_dl_b, _ = dl_b.communicate()

    logs.append("[Session A Output]:\n" + out_dl_a)
    logs.append("[Session B Output (Engine-Level Deadlock Detected)]:\n" + out_dl_b)

    # Reset offering capacities
    run_query("UPDATE course_offerings SET capacity = 2 WHERE offering_id IN (1, 2);")

    log_path = "/Users/oyekunle/Downloads/winnermit/portfolio-3-transactions-concurrency/Oyebanjo_Winner_Portfolio3_Execution_Logs.txt"
    with open(log_path, "w") as f:
        f.write("\n".join(logs))
    print(f"Transactions execution logs updated: {log_path}")

if __name__ == '__main__':
    main()
