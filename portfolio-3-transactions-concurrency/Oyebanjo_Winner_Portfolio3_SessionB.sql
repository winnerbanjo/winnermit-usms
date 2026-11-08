-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 3: Transactions and Concurrency Control
-- SESSION B INSTRUCTIONS (Run in Terminal 2 or Workbench Tab 2)
-- Target: winnermit_usms_p3
-- ============================================================

USE winnermit_usms_p3;

-- STEP 1: Demonstrate Lock Contention & Timeout
START TRANSACTION;
SET innodb_lock_wait_timeout = 3;

-- This statement will BLOCK because Session A holds an exclusive lock on offering_id = 2
-- After 3 seconds, it will abort with:
-- ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
SELECT offering_id, capacity 
FROM course_offerings 
WHERE offering_id = 2 
FOR UPDATE;

ROLLBACK;

-- STEP 2: Modify Data Concurrently for Session A's REPEATABLE READ Test
START TRANSACTION;
UPDATE course_offerings 
SET capacity = 10 
WHERE offering_id = 2;

-- Commit immediately to verify Session A's read consistency
COMMIT;
