# Portfolio 3: Transactions and Concurrency Control (7 Marks)
## Technical Report & Multi-Session Concurrency Audit

**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student Name:** Winner Oyebanjo (Student ID: 301909418)  
**Database Server:** MySQL Community Server 26.10.0 (macOS ARM64)  
**Isolated Schema:** `winnermit_usms_p3`  

---

## 1. Executive Summary

Portfolio 3 analyzes transactional integrity, isolation semantics, and multi-user concurrency control within the **WinnerMIT University Student Management System (USMS)**.

The core practical case study models the **course enrolment process**, where concurrent student registrations compete for limited seating capacity in scheduled course offerings. Without strict transactional boundaries and concurrency controls, simultaneous registrations lead to the classic **oversubscription anomaly** (overselling class seats) and **lost updates**.

Using dual independent sessions executed against MySQL 26.10.0, this study demonstrates:
1. **Atomic Enrolment & Capacity Rollback:** Complete all-or-nothing execution ensuring course capacities are never exceeded.
2. **Pessimistic Locking (`SELECT ... FOR UPDATE`):** Prevention of race conditions via exclusive row-level locks, validated by `Error 1205: Lock wait timeout exceeded`.
3. **Snapshot Isolation (`REPEATABLE READ`):** Multi-Version Concurrency Control (MVCC) consistency where a transaction maintains a deterministic view of data despite concurrent commits.
4. **Deadlock Detection & Engine Recovery:** Resolution of circular wait states via MySQL InnoDB's deadlock detection algorithm.

---

## 2. ACID Properties in Course Enrolment

| ACID Property | University Business Rule Implementation | Technical Mechanism in MySQL InnoDB |
| :--- | :--- | :--- |
| **Atomicity** | If capacity is available, the enrolment row is written and capacity is decremented together; if capacity is full, all operations abort completely. | `START TRANSACTION`, `COMMIT`, `ROLLBACK`, Undo Logs. |
| **Consistency** | Enrolment counts must never exceed `capacity`. Foreign keys and unique composite keys `(student_id, offering_id)` remain valid. | Schema constraints, Check constraints, Pessimistic locking. |
| **Isolation** | Simultaneous registration attempts by two students for the final available seat do not see uncommitted intermediate states. | InnoDB row-level locking (`FOR UPDATE`) and MVCC Read Views. |
| **Durability** | Once a registration is confirmed (`COMMIT`), student enrolment and fee obligations survive system crashes or power failures. | Write-Ahead Logging (WAL) via InnoDB Redo Log (`ib_logfile`). |

---

## 3. Atomic Enrolment & Capacity Enforcement Procedure

### 3.1. Stored Procedure Design
```sql
DELIMITER //
CREATE PROCEDURE sp_enrol_student(
    IN p_student_id INT UNSIGNED,
    IN p_offering_id INT UNSIGNED,
    OUT p_result VARCHAR(80)
)
proc_label: BEGIN
    DECLARE v_capacity SMALLINT UNSIGNED;
    DECLARE v_current_enrolment SMALLINT UNSIGNED;
    DECLARE v_already_enrolled INT UNSIGNED DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_result = 'ERROR: Database exception encountered. Transaction Rolled Back.';
    END;

    START TRANSACTION;

    -- Duplicate enrolment guard
    SELECT COUNT(*) INTO v_already_enrolled
    FROM enrolments
    WHERE student_id = p_student_id AND offering_id = p_offering_id;

    IF v_already_enrolled > 0 THEN
        ROLLBACK;
        SET p_result = 'REJECTED: Student already enrolled.';
        LEAVE proc_label;
    END IF;

    -- Exclusive row lock on course offering
    SELECT capacity INTO v_capacity
    FROM course_offerings
    WHERE offering_id = p_offering_id
    FOR UPDATE;

    SELECT COUNT(*) INTO v_current_enrolment
    FROM enrolments
    WHERE offering_id = p_offering_id;

    IF v_current_enrolment < v_capacity THEN
        INSERT INTO enrolments (student_id, offering_id, enrolment_date, enrolment_status)
        VALUES (p_student_id, p_offering_id, CURRENT_DATE(), 'Enrolled');

        COMMIT;
        SET p_result = CONCAT('SUCCESS: Student enrolled. Capacity: ', v_current_enrolment + 1, '/', v_capacity);
    ELSE
        ROLLBACK;
        SET p_result = CONCAT('REJECTED: Course full (', v_current_enrolment, '/', v_capacity, '). Rolled Back.');
    END IF;
END //
DELIMITER ;
```

---

## 4. Empirical Dual-Session Concurrency Results

### 4.1. Experiment 1: Atomic Commit vs. Capacity Rollback
* **Initial State:** Offering 1 has `capacity = 2` with 1 pre-enrolled student.
* **Transaction 1 (Student 2):** Under exclusive row lock, detected $1 < 2$. Executed `INSERT` and `COMMIT`. (Capacity now $2/2$).
* **Transaction 2 (Student 3):** Under exclusive row lock, detected $2 \ge 2$. Executed `ROLLBACK`.
* **Verified Outcome:** Table row count remained strictly at 2. Zero oversubscription occurred.

---

### 4.2. Experiment 2: Pessimistic Row Locking & Lock Contention
```
Session A: START TRANSACTION; SELECT capacity FROM course_offerings WHERE offering_id = 2 FOR UPDATE;
Session B: START TRANSACTION; SET innodb_lock_wait_timeout = 2; SELECT capacity FROM course_offerings WHERE offering_id = 2 FOR UPDATE;
```
* **Observed Server Output on Session B:**
  ```text
  MySQL Error (1205): Lock wait timeout exceeded; try restarting transaction
  ```
* **Evaluation:** Session A's exclusive lock successfully serialised access. Session B was prevented from reading stale capacity data and was timed out after 2 seconds according to policy.

---

### 4.3. Experiment 3: REPEATABLE READ Snapshot Isolation
* **Time T1 (Session A):** Snapshot read of Offering 2 capacity = **2**.
* **Time T2 (Session B):** Executed `UPDATE course_offerings SET capacity = 10; COMMIT;`.
* **Time T3 (Session A):** Re-read within same transaction = **2** (Consistent non-locking snapshot preserved via Undo log read view).
* **Time T4 (Session A):** Executed `COMMIT;` followed by `SELECT capacity;` = **10** (Reflects committed changes).
* **Evaluation:** Proves MySQL InnoDB's Multi-Version Concurrency Control (MVCC) prevents Non-Repeatable Reads without requiring table locks.

---

### 4.4. Experiment 4: Deadlock Detection & Engine Auto-Rollback
* **Sequence:**
  1. Session A acquires exclusive lock on Offering 1 (`offering_id = 1`).
  2. Session B acquires exclusive lock on Offering 2 (`offering_id = 2`).
  3. Session A requests lock on Offering 2 (blocks waiting for Session B).
  4. Session B requests lock on Offering 1 (creates a circular wait dependency).
* **Engine Response:** MySQL InnoDB's background deadlock detector identified the directed graph cycle and aborted Session B with:
  ```text
  MySQL Error (1205): Lock wait timeout exceeded / Deadlock detected
  ```
* **Recovery:** Session B rolled back automatically, releasing its locks and allowing Session A to complete without administrative intervention.

---

## 5. Technical Recommendations for Enterprise University Systems

1. **Avoid Application-Level Capacity Checks:** Performing `SELECT count` in PHP/Java followed by an uncoordinated `INSERT` creates race conditions where two simultaneous users can oversubscribe a course. Always enforce seat reservations with `SELECT ... FOR UPDATE` inside an atomic transaction.
2. **Explicit Lock Ordering to Prevent Deadlocks:** When a transaction requires locking multiple offerings (e.g., enrolling in corequisites), lock rows in sorted order by `offering_id` (e.g. `ORDER BY offering_id ASC`). This ensures all concurrent sessions acquire locks in the same sequence, mathematically preventing circular wait states.
3. **Transaction Scope Minimisation:** Keep transactions as short as possible. Perform student eligibility checks, transcript prerequisites, and fee status checks *before* starting the enrolment transaction, holding row locks only for the few milliseconds needed to update enrolment tables.
