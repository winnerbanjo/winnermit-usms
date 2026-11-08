# Portfolio 3: Transactions and Concurrency Control (7 Marks)
**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student:** Winner Oyebanjo (ID: 301909418)  
**Case Study:** WinnerMIT University Student Management System (USMS)  

---

## Portfolio Overview

Portfolio 3 analyzes transactional integrity (ACID properties), Multi-Version Concurrency Control (MVCC), and pessimistic row locking during student course registrations.

Testing is executed in an isolated database (`winnermit_usms_p3`) on **MySQL Community Server 26.10.0**, preserving the Portfolio 1 baseline schemas untouched.

### Contents in this Directory
1. **`Oyebanjo_Winner_Portfolio3_Setup.sql`**: Isolated schema DDL and seed data for `winnermit_usms_p3`.
2. **`Oyebanjo_Winner_Portfolio3_Transactions.sql`**: Stored procedure `sp_enrol_student` implementing atomic enrolment and pessimistic locking.
3. **`Oyebanjo_Winner_Portfolio3_SessionA.sql`**: Step-by-step instructions for Session A in multi-session concurrency testing.
4. **`Oyebanjo_Winner_Portfolio3_SessionB.sql`**: Step-by-step instructions for Session B in multi-session concurrency testing.
5. **`run_p3_classic_concurrency.py`**: Multi-session automated test harness executing dual concurrent sessions via `mysql.get_classic_session()`.
6. **`Oyebanjo_Winner_Portfolio3_Execution_Logs.txt`**: Unedited execution logs captured directly from MySQL 26.10.0.
7. **`Oyebanjo_Winner_Portfolio3_Report.md`**: Master academic technical report detailing ACID enforcement, lock timeouts, snapshot isolation, and deadlock handling.

### Key Verified Findings
* **Atomic Rollback:** Enrolment attempt on full course offering (2/2) rolled back automatically with zero data corruption.
* **Pessimistic Locking:** Verified with `MySQL Error (1205): Lock wait timeout exceeded`.
* **Repeatable Read:** Proved consistent snapshot read during concurrent updates.
* **Deadlock Recovery:** Verified engine-level circular wait detection and recovery.
