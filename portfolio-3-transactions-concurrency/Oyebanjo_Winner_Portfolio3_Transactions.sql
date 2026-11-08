-- ============================================================
-- MIT 8103 - Advanced Database Systems
-- Portfolio 3: Transactions and Concurrency Control
-- MASTER TRANSACTION PROCEDURES AND DEMONSTRATIONS
-- Target: winnermit_usms_p3
-- Student: Winner Oyebanjo (ID: 301909418)
-- ============================================================

USE winnermit_usms_p3;

-- 1. Stored Procedure for Atomic Course Registration with Pessimistic Locking
DELIMITER //

DROP PROCEDURE IF EXISTS sp_enrol_student//
CREATE PROCEDURE sp_enrol_student(
    IN p_student_id INT UNSIGNED,
    IN p_offering_id INT UNSIGNED,
    OUT p_result VARCHAR(80)
)
proc_label: BEGIN
    DECLARE v_capacity SMALLINT UNSIGNED;
    DECLARE v_current_enrolment SMALLINT UNSIGNED;
    DECLARE v_already_enrolled INT UNSIGNED DEFAULT 0;

    -- Error handler to automatically roll back on any SQL exception
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_result = 'ERROR: Database exception encountered. Transaction Rolled Back.';
    END;

    START TRANSACTION;

    -- Step 1: Check duplicate enrolment
    SELECT COUNT(*) INTO v_already_enrolled
    FROM enrolments
    WHERE student_id = p_student_id AND offering_id = p_offering_id;

    IF v_already_enrolled > 0 THEN
        ROLLBACK;
        SET p_result = 'REJECTED: Student already enrolled in this course offering.';
        LEAVE proc_label;
    END IF;

    -- Step 2: Acquire exclusive lock on the course offering to prevent race conditions
    SELECT capacity INTO v_capacity
    FROM course_offerings
    WHERE offering_id = p_offering_id
    FOR UPDATE;

    -- Step 3: Count current enrolments under lock
    SELECT COUNT(*) INTO v_current_enrolment
    FROM enrolments
    WHERE offering_id = p_offering_id;

    -- Step 4: Enforce capacity check
    IF v_current_enrolment < v_capacity THEN
        INSERT INTO enrolments (student_id, offering_id, enrolment_date, enrolment_status)
        VALUES (p_student_id, p_offering_id, CURRENT_DATE(), 'Enrolled');

        COMMIT;
        SET p_result = CONCAT('SUCCESS: Student enrolled. Capacity utilized: ', v_current_enrolment + 1, '/', v_capacity);
    ELSE
        ROLLBACK;
        SET p_result = CONCAT('REJECTED: Course offering full (', v_current_enrolment, '/', v_capacity, '). Transaction Rolled Back.');
    END IF;
END //

DELIMITER ;
