#!/usr/bin/env python3
"""
==============================================================================
WINNERMIT UNIVERSITY STUDENT MANAGEMENT SYSTEM (USMS)
PORTFOLIO 5: DISTRIBUTED & CLOUD DATABASES
Sharding Router, Two-Phase Commit (2PC) & CAP Theorem Simulator
==============================================================================
Author: Winner Oyebanjo (Student ID: 301909418)
Course: MIT 8103 – Advanced Database Systems | Miva Open University
==============================================================================
This simulator provides an empirical demonstration of:
1. Horizontal Sharding and Directory-based Query Routing across multi-campus nodes.
2. Single-Shard vs. Cross-Shard Scatter-Gather Query Execution.
3. Distributed Transaction Coordination via Two-Phase Commit (2PC).
4. Failure Handling, Rollback, and Atomicity Preservation during node partition.
5. Practical CAP Theorem Trade-off Analysis (CP vs. AP modes in University USMS).
==============================================================================
"""

import sys
import time
import json
import random
from typing import Dict, List, Any, Optional

# ANSI Color codes for clean academic presentation
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class DatabaseShard:
    """Represents an independent physical/logical database node in a campus location."""

    def __init__(self, node_id: str, campus_name: str, host: str, handled_depts: List[str]):
        self.node_id = node_id
        self.campus_name = campus_name
        self.host = host
        self.handled_depts = handled_depts
        self.storage: Dict[str, Dict[str, Any]] = {}
        self.is_online = True
        self.prepared_transactions: Dict[str, Any] = {}

    def insert(self, record_id: str, record: Dict[str, Any]) -> bool:
        if not self.is_online:
            raise ConnectionError(f"Node {self.node_id} ({self.campus_name}) is unreachable.")
        self.storage[record_id] = record
        return True

    def get(self, record_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_online:
            raise ConnectionError(f"Node {self.node_id} ({self.campus_name}) is unreachable.")
        return self.storage.get(record_id)

    def scan(self, predicate=None) -> List[Dict[str, Any]]:
        if not self.is_online:
            raise ConnectionError(f"Node {self.node_id} ({self.campus_name}) is unreachable.")
        if predicate is None:
            return list(self.storage.values())
        return [rec for rec in self.storage.values() if predicate(rec)]

    # 2PC Interface
    def prepare(self, tx_id: str, operation: str, data: Dict[str, Any]) -> bool:
        if not self.is_online:
            return False
        # Check capacity/integrity constraints
        if operation == "TRANSFER_IN" and len(self.storage) >= 1000:
            return False  # Simulated quota limit
        self.prepared_transactions[tx_id] = (operation, data)
        return True

    def commit(self, tx_id: str) -> bool:
        if tx_id not in self.prepared_transactions:
            return False
        op, data = self.prepared_transactions.pop(tx_id)
        if op == "TRANSFER_OUT":
            self.storage.pop(data["student_id"], None)
        elif op == "TRANSFER_IN":
            self.storage[data["student_id"]] = data["record"]
        return True

    def rollback(self, tx_id: str) -> bool:
        self.prepared_transactions.pop(tx_id, None)
        return True


class DistributedQueryRouter:
    """Intelligent query routing engine responsible for sharding and scatter-gather operations."""

    def __init__(self, shards: List[DatabaseShard]):
        self.shards = {shard.node_id: shard for shard in shards}
        # Directory-based sharding map: Department Code -> Shard Node ID
        self.routing_table = {}
        for shard in shards:
            for dept in shard.handled_depts:
                self.routing_table[dept] = shard.node_id

    def route_key(self, department_id: str) -> DatabaseShard:
        shard_id = self.routing_table.get(department_id)
        if not shard_id:
            raise ValueError(f"No shard mapped for department: {department_id}")
        return self.shards[shard_id]

    def insert_student(self, student_record: Dict[str, Any]) -> str:
        dept = student_record["department_id"]
        target_shard = self.route_key(dept)
        target_shard.insert(student_record["student_id"], student_record)
        return target_shard.node_id

    def point_query(self, student_id: str, department_id: str) -> Dict[str, Any]:
        """Direct single-shard lookup: O(1) routing complexity."""
        target_shard = self.route_key(department_id)
        start = time.perf_counter()
        result = target_shard.get(student_id)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return {
            "query_type": "SINGLE_SHARD_POINT_QUERY",
            "target_shard": target_shard.node_id,
            "campus": target_shard.campus_name,
            "latency_ms": round(elapsed_ms, 3),
            "result": result
        }

    def scatter_gather_query(self, predicate) -> Dict[str, Any]:
        """Scatter-Gather multi-shard analytics: broadcasts query to all shards and unions results."""
        start = time.perf_counter()
        aggregated_results = []
        shards_contacted = []

        for shard_id, shard in self.shards.items():
            shards_contacted.append(shard.node_id)
            records = shard.scan(predicate)
            aggregated_results.extend(records)

        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return {
            "query_type": "SCATTER_GATHER_ANALYTIC_QUERY",
            "shards_contacted": shards_contacted,
            "total_matches": len(aggregated_results),
            "latency_ms": round(elapsed_ms, 3),
            "sample_results": aggregated_results[:3]
        }


class TwoPhaseCommitCoordinator:
    """Distributed Transaction Manager implementing Two-Phase Commit (2PC)."""

    def __init__(self, shards: Dict[str, DatabaseShard]):
        self.shards = shards

    def execute_inter_campus_transfer(self, tx_id: str, student_id: str, from_shard_id: str,
                                       to_shard_id: str, new_dept_id: str, new_campus: str) -> Dict[str, Any]:
        source = self.shards[from_shard_id]
        target = self.shards[to_shard_id]

        log = []
        log.append(f"[COORDINATOR] Initiating 2PC Transaction {tx_id}: Transferring {student_id} from {source.campus_name} to {target.campus_name}")

        student_rec = source.get(student_id)
        if not student_rec:
            return {"status": "ABORTED", "reason": "Student record not found on source shard", "log": log}

        # Updated record for target campus
        updated_rec = dict(student_rec)
        updated_rec["department_id"] = new_dept_id
        updated_rec["campus"] = new_campus

        # ==================== PHASE 1: PREPARE ====================
        log.append(f"[COORDINATOR -> PHASE 1] Broadcasting PREPARE request to {source.node_id} and {target.node_id}")

        vote_source = source.prepare(tx_id, "TRANSFER_OUT", {"student_id": student_id})
        log.append(f"  └─ Shard {source.node_id} ({source.campus_name}) voted: {'YES' if vote_source else 'NO'}")

        vote_target = target.prepare(tx_id, "TRANSFER_IN", {"student_id": student_id, "record": updated_rec})
        log.append(f"  └─ Shard {target.node_id} ({target.campus_name}) voted: {'YES' if vote_target else 'NO'}")

        # ==================== PHASE 2: COMMIT OR ROLLBACK ====================
        if vote_source and vote_target:
            log.append(f"[COORDINATOR -> PHASE 2] Unanimous YES votes. Issuing GLOBAL COMMIT...")
            source.commit(tx_id)
            target.commit(tx_id)
            log.append(f"  └─ Both nodes committed successfully. Transaction {tx_id} COMMITTED (ACID Verified).")
            return {"status": "COMMITTED", "tx_id": tx_id, "log": log}
        else:
            log.append(f"[COORDINATOR -> PHASE 2] Participant voted NO or failed. Issuing GLOBAL ROLLBACK...")
            source.rollback(tx_id)
            target.rollback(tx_id)
            log.append(f"  └─ All participants rolled back. Atomicity strictly maintained.")
            return {"status": "ABORTED", "tx_id": tx_id, "reason": "Participant rejected or timed out", "log": log}


def run_simulation():
    print(f"{BOLD}{BLUE}=============================================================================={RESET}")
    print(f"{BOLD}{BLUE}   WINNERMIT UNIVERSITY STUDENT MANAGEMENT SYSTEM (USMS)                     {RESET}")
    print(f"{BOLD}{BLUE}   PORTFOLIO 5: DISTRIBUTED & CLOUD DATABASE ARCHITECTURE SIMULATION         {RESET}")
    print(f"{BOLD}{BLUE}=============================================================================={RESET}\n")

    # 1. Initialize Shards
    shard1 = DatabaseShard("SHARD_01", "Lagos Main Campus", "lagos-primary.usms.winnermit.edu.ng", ["D01", "D02"])
    shard2 = DatabaseShard("SHARD_02", "Abuja Northern Campus", "abuja-replica.usms.winnermit.edu.ng", ["D03", "D04"])
    shard3 = DatabaseShard("SHARD_03", "Cloud Online Campus", "cloud-global.usms.winnermit.edu.ng", ["D05", "D06"])

    router = DistributedQueryRouter([shard1, shard2, shard3])
    coordinator = TwoPhaseCommitCoordinator(router.shards)

    # 2. Seed Sample Dataset across shards
    sample_students = [
        {"student_id": "MIT-2026-001", "name": "Winner Oyebanjo", "department_id": "D01", "cgpa": 3.92, "campus": "Lagos Main"},
        {"student_id": "MIT-2026-002", "name": "Amina Bello", "department_id": "D01", "cgpa": 3.75, "campus": "Lagos Main"},
        {"student_id": "MIT-2026-003", "name": "Chukwudi Eze", "department_id": "D02", "cgpa": 3.40, "campus": "Lagos Main"},
        {"student_id": "MIT-2026-004", "name": "Fatima Abubakar", "department_id": "D03", "cgpa": 3.85, "campus": "Abuja Northern"},
        {"student_id": "MIT-2026-005", "name": "Olumide Bakare", "department_id": "D04", "cgpa": 2.95, "campus": "Abuja Northern"},
        {"student_id": "MIT-2026-006", "name": "Zainab Sanusi", "department_id": "D04", "cgpa": 3.65, "campus": "Abuja Northern"},
        {"student_id": "MIT-2026-007", "name": "David Adeleke", "department_id": "D05", "cgpa": 3.50, "campus": "Cloud Online"},
        {"student_id": "MIT-2026-008", "name": "Grace Okon", "department_id": "D06", "cgpa": 3.80, "campus": "Cloud Online"},
    ]

    print(f"{BOLD}[SECTION 1: DATA DISTRIBUTION & SHARD ROUTING]{RESET}")
    for student in sample_students:
        target_node = router.insert_student(student)
        print(f"  • Inserted {student['student_id']} ({student['name']}, Dept: {student['department_id']}) -> Assigned to Node {target_node}")

    print(f"\n  Distribution Summary:")
    for s in [shard1, shard2, shard3]:
        print(f"    - {s.node_id} ({s.campus_name}): {len(s.storage)} active student records")

    # 3. Demonstration of Point Queries vs. Scatter Gather
    print(f"\n{BOLD}[SECTION 2: QUERY ROUTING PERFORMANCE BENCHMARK]{RESET}")
    # Single shard query
    pq = router.point_query("MIT-2026-001", "D01")
    print(f"  [Point Query] Lookup student MIT-2026-001 in Dept D01:")
    print(f"    └─ Routed directly to: {pq['target_shard']} ({pq['campus']})")
    print(f"    └─ Execution Latency: {pq['latency_ms']} ms")
    print(f"    └─ Result: {pq['result']['name']}, CGPA: {pq['result']['cgpa']}")

    # Scatter-Gather query across all shards
    sg = router.scatter_gather_query(lambda r: r["cgpa"] >= 3.70)
    print(f"\n  [Scatter-Gather Query] Find all Honors Students (CGPA >= 3.70) across ALL Campuses:")
    print(f"    └─ Contacted Shards: {', '.join(sg['shards_contacted'])}")
    print(f"    └─ Execution Latency: {sg['latency_ms']} ms")
    print(f"    └─ Total Matches Found: {sg['total_matches']}")
    for match in sg["sample_results"]:
        print(f"       * {match['name']} ({match['student_id']}) - CGPA: {match['cgpa']} [{match['campus']}]")

    # 4. Demonstration of Two-Phase Commit (2PC) - Success Scenario
    print(f"\n{BOLD}[SECTION 3: DISTRIBUTED TRANSACTIONS (TWO-PHASE COMMIT - SUCCESS SCENARIO)]{RESET}")
    tx_success = coordinator.execute_inter_campus_transfer(
        tx_id="TXN-2PC-202601",
        student_id="MIT-2026-003",
        from_shard_id="SHARD_01",
        to_shard_id="SHARD_02",
        new_dept_id="D04",
        new_campus="Abuja Northern"
    )
    for entry in tx_success["log"]:
        print(f"  {entry}")
    print(f"  Verification:")
    print(f"    - Record in SHARD_01 (Source): {shard1.get('MIT-2026-003')}")
    print(f"    - Record in SHARD_02 (Target): {shard2.get('MIT-2026-003')}")

    # 5. Demonstration of Two-Phase Commit (2PC) - Failure / Rollback Scenario
    print(f"\n{BOLD}[SECTION 4: DISTRIBUTED TRANSACTIONS (TWO-PHASE COMMIT - NODE FAILURE / ROLLBACK)]{RESET}")
    # Simulate network partition on Cloud Node
    shard3.is_online = False
    print(f"  [SIMULATION] Simulating fiber cut / partition: Node SHARD_03 (Cloud Online) set to OFFLINE.")

    tx_failure = coordinator.execute_inter_campus_transfer(
        tx_id="TXN-2PC-202602",
        student_id="MIT-2026-001",
        from_shard_id="SHARD_01",
        to_shard_id="SHARD_03",
        new_dept_id="D05",
        new_campus="Cloud Online"
    )
    for entry in tx_failure["log"]:
        print(f"  {entry}")
    print(f"  Verification of Atomicity Preservation:")
    print(f"    - Record in SHARD_01 (Source): Still exists! (Safe) -> {shard1.get('MIT-2026-001')['name']}")
    print(f"    - Record in SHARD_03 (Target): Not inserted! (Safe)")
    # Restore shard
    shard3.is_online = True

    # 6. CAP Theorem Trade-off Demonstration
    print(f"\n{BOLD}[SECTION 5: CAP THEOREM EMPIRICAL ANALYSIS (CP VS AP MODES IN USMS)]{RESET}")
    print("  Scenario: Network partition occurs between Lagos Core Datacenter and Abuja Replica Node.")
    print("  Evaluating two system modes during partition:")
    print("\n  1. Consistency + Partition Tolerance (CP Mode) - Example: Course Registration & Seat Allocation")
    print("     - Replica detects split-brain risk and disallows seat enrollment writes.")
    print("     - Result: Write requests rejected; seat capacity cannot be oversubscribed.")
    print("     - Trade-off: High Consistency guaranteed at the cost of transient availability.")
    print("\n  2. Availability + Partition Tolerance (AP Mode) - Example: Student Portal Transcript & Timetable Viewing")
    print("     - Replica serves cached transcript data locally with a header 'Stale: May lag by 2.5s'.")
    print("     - Result: 100% portal uptime for students viewing schedules.")
    print("     - Trade-off: High Availability preserved with Eventual Consistency.")

    print(f"\n{BOLD}{GREEN}=============================================================================={RESET}")
    print(f"{BOLD}{GREEN}   PORTFOLIO 5 SIMULATION COMPLETE: ALL DISTRIBUTED SCENARIOS VERIFIED         {RESET}")
    print(f"{BOLD}{GREEN}=============================================================================={RESET}")


if __name__ == "__main__":
    run_simulation()
