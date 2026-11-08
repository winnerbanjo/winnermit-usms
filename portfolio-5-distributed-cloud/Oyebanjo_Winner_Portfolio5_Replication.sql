-- ==============================================================================
-- WINNERMIT UNIVERSITY STUDENT MANAGEMENT SYSTEM (USMS)
-- PORTFOLIO 5: DISTRIBUTED & CLOUD DATABASES
-- Production MySQL GTID-Based Replication Provisioning & Failover Script
-- Author: Winner Oyebanjo (Student ID: 301909418)
-- Course: MIT 8103 Advanced Database Systems | Miva Open University
-- Target Server Version: MySQL 8.0.16+ / 26.10.0+
-- ==============================================================================

-- ==============================================================================
-- PART 1: PRIMARY SOURCE CONFIGURATION (Lagos Campus Node)
-- Execute on: lagos-primary.usms.winnermit.edu.ng
-- ==============================================================================

-- 1.1 Verify GTID and Binary Logging State
SELECT 
    @@server_id AS server_id,
    @@gtid_mode AS gtid_mode,
    @@enforce_gtid_consistency AS enforce_gtid_consistency,
    @@log_bin AS log_bin_enabled,
    @@binlog_format AS binlog_format;

-- 1.2 Create Dedicated Replication Service Account
-- Principle of Least Privilege: only REPLICATION SLAVE is granted
-- Password placeholder used for academic submission security
CREATE USER IF NOT EXISTS 'repl_user'@'%' 
IDENTIFIED BY 'ReplSecurePass_2026!#WinnerMIT'
REQUIRE SSL;

GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
FLUSH PRIVILEGES;

-- 1.3 Enable and Verify Semi-Synchronous Replication (Source Side)
INSTALL PLUGIN rpl_semi_sync_source SONAME 'semisync_source.so';
SET GLOBAL rpl_semi_sync_source_enabled = 1;
SET GLOBAL rpl_semi_sync_source_timeout = 10000; -- 10 seconds timeout

-- 1.4 Inspect Primary Binary Log Coordinates and GTID Set
SHOW BINARY LOG STATUS;


-- ==============================================================================
-- PART 2: SECONDARY REPLICA CONFIGURATION (Abuja Campus Node)
-- Execute on: abuja-replica.usms.winnermit.edu.ng
-- ==============================================================================

-- 2.1 Enforce Read-Only Safety on Replica Node
SET GLOBAL read_only = ON;
SET GLOBAL super_read_only = ON;

-- 2.2 Configure Replication Connection using MySQL 8.0+ Syntax
-- Using GTID Auto-Positioning (Eliminates manual binary log file/offset drift)
CHANGE REPLICATION SOURCE TO
    SOURCE_HOST = 'lagos-primary.usms.winnermit.edu.ng',
    SOURCE_PORT = 3306,
    SOURCE_USER = 'repl_user',
    SOURCE_PASSWORD = 'ReplSecurePass_2026!#WinnerMIT',
    SOURCE_AUTO_POSITION = 1,
    SOURCE_SSL = 1,
    SOURCE_CONNECT_RETRY = 60,
    SOURCE_RETRY_COUNT = 86400,
    SOURCE_HEARTBEAT_PERIOD = 2.5;

-- 2.3 Enable Semi-Synchronous Replication (Replica Side)
INSTALL PLUGIN rpl_semi_sync_replica SONAME 'semisync_replica.so';
SET GLOBAL rpl_semi_sync_replica_enabled = 1;

-- 2.4 Start Replication Threads
START REPLICA;


-- ==============================================================================
-- PART 3: REPLICATION TELEMETRY & HEALTH MONITORING
-- Execute on: abuja-replica.usms.winnermit.edu.ng
-- ==============================================================================

-- 3.1 Classic Replication Thread Status
SHOW REPLICA STATUS\G

-- 3.2 Detailed Performance Schema Lag and Applier Diagnostics
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE AS IO_THREAD_STATE,
    LAST_ERROR_NUMBER AS IO_ERR_NUM,
    LAST_ERROR_MESSAGE AS IO_ERR_MSG
FROM performance_schema.replication_connection_status;

SELECT 
    CHANNEL_NAME,
    SERVICE_STATE AS SQL_THREAD_STATE,
    REMAINING_DELAY,
    COUNT_TRANSACTIONS_ROWS_AFFECTED
FROM performance_schema.replication_applier_status_by_worker;

-- 3.3 Seconds Behind Source Calculation
SELECT 
    SERVICE_STATE,
    LAST_HEARTBEAT_TIMESTAMP,
    RECEIVED_TRANSACTION_SET
FROM performance_schema.replication_connection_status;


-- ==============================================================================
-- PART 4: DISASTER RECOVERY & MANUAL FAILOVER PROCEDURE
-- Scenario: Lagos Primary experiences catastrophic hardware/network outage.
-- Target: Promote Abuja Replica to Primary Read/Write Node.
-- ==============================================================================

-- Step 4.1: Ensure Replica has applied all received relay logs
STOP REPLICA IO_THREAD;
-- Wait until SQL thread applies all buffered transactions:
START REPLICA SQL_THREAD;

-- Step 4.2: Sever Replication Channel and Disable Read-Only Restrictions
STOP REPLICA;
RESET REPLICA ALL;

SET GLOBAL read_only = OFF;
SET GLOBAL super_read_only = OFF;

-- Step 4.3: Configure Abuja as new Source (Enable Binary Logging & Semi-Sync)
INSTALL PLUGIN rpl_semi_sync_source SONAME 'semisync_source.so';
SET GLOBAL rpl_semi_sync_source_enabled = 1;

-- Step 4.4: Verify Node is Ready for Campus Read/Write Traffic
SELECT 
    @@server_id AS promoted_server_id,
    @@read_only AS is_read_only,
    @@super_read_only AS is_super_read_only,
    @@gtid_executed AS current_executed_gtids;
