-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 3: Transactions and Concurrency Control
-- SESSION A INSTRUCTIONS (Run in Terminal 1 or Workbench Tab 1)
-- Target: winnermit_usms_p3
-- ============================================================

USE winnermit_usms_p3;

-- STEP 1: Demonstrate Exclusive Lock (FOR UPDATE)
START TRANSACTION;
SELECT offering_id, capacity 
FROM course_offerings 
WHERE offering_id = 2 
FOR UPDATE;

-- (Keep this transaction open while executing Session B Step 1)
-- Once Session B has blocked and timed out:
COMMIT;

-- STEP 2: Demonstrate REPEATABLE READ Snapshot Isolation
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;

-- Initial Snapshot Read
SELECT capacity AS session_a_t1_snapshot 
FROM course_offerings 
WHERE offering_id = 2;

-- (Wait for Session B to execute its UPDATE and COMMIT)

-- Re-reading within the same transaction (Snapshot must remain unchanged!)
SELECT capacity AS session_a_t2_repeatable_read 
FROM course_offerings 
WHERE offering_id = 2;

-- Commit the transaction to release snapshot
COMMIT;

-- Read after commit (Reflects Session B's committed update)
SELECT capacity AS session_a_t3_post_commit 
FROM course_offerings 
WHERE offering_id = 2;
