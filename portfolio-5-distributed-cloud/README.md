# Portfolio 5: Distributed & Cloud Databases

**Course:** MIT 8103 – Advanced Database Systems  
**Student Name:** Winner Oyebanjo  
**Student ID:** 301909418  
**Institution:** Miva Open University  
**Case Study:** WinnerMIT University Student Management System (USMS)  
**Marks Weighting:** 6 Marks  

---

## 1. Overview & Objectives

Portfolio 5 addresses enterprise scale, high availability, and geographic data distribution for the WinnerMIT University Student Management System across its multi-campus topology (Lagos Main Campus, Abuja Northern Campus, and Cloud Online Learning).

This module delivers:
1. **Multi-Region Replication Architecture:** Production-ready MySQL configurations implementing semi-synchronous replication, GTID auto-positioning, and multi-threaded parallel appliers.
2. **Replication & Failover Automation:** SQL provisioning scripts for secure replication accounts, replication channels, telemetry monitoring, and disaster recovery promotion.
3. **Horizontal Sharding & Query Routing:** Directory-based sharding model partitioning data by department/campus with benchmarked single-shard point lookups vs. cross-shard scatter-gather queries.
4. **Distributed Transactions (2PC):** Implementation and verification of the Two-Phase Commit protocol demonstrating commit atomicity and failure rollback during network partitions.
5. **CAP Theorem Strategic Analysis:** Trade-off analysis contrasting CP mode (course registration seat allocation) with AP mode (student portal transcript viewing).

---

## 2. Directory Contents

| File Name | Description |
| :--- | :--- |
| [`primary-my.cnf`](./primary-my.cnf) | MySQL enterprise configuration file for the Primary Source node (Lagos Campus) configuring GTID, binary logging, and semi-sync source. |
| [`replica-my.cnf`](./replica-my.cnf) | MySQL enterprise configuration file for the Regional Replica node (Abuja Campus) configuring read-only enforcement, relay logs, and parallel appliers. |
| [`Oyebanjo_Winner_Portfolio5_Replication.sql`](./Oyebanjo_Winner_Portfolio5_Replication.sql) | Production SQL script containing user creation, `CHANGE REPLICATION SOURCE`, performance schema health monitoring, and master promotion failover logic. |
| [`Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py`](./Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py) | Python distributed database simulation engine modeling directory sharding, query routing, 2PC coordinator, and network partition failure scenarios. |
| [`Oyebanjo_Winner_Portfolio5_Execution_Logs.txt`](./Oyebanjo_Winner_Portfolio5_Execution_Logs.txt) | Captured empirical output logs generated from the simulation run. |
| [`Oyebanjo_Winner_Portfolio5_Report.md`](./Oyebanjo_Winner_Portfolio5_Report.md) | Comprehensive 6-mark academic and technical report with Mermaid architecture diagrams, sharding benchmarks, 2PC sequence diagrams, and disaster recovery strategies. |

---

## 3. How to Run the Distributed Simulation

Execute the self-contained Python simulation to verify data distribution, routing latencies, 2PC atomicity, and partition tolerance:

```bash
python3 portfolio-5-distributed-cloud/Oyebanjo_Winner_Portfolio5_Sharding_Simulator.py
```

The output confirms:
- $O(1)$ single-shard lookup latency vs. scatter-gather multi-shard latency.
- Successful 2PC commit across Lagos and Abuja nodes.
- Guaranteed atomicity rollback when a participating shard is partitioned/offline.
- CP vs. AP behavioral trade-offs.
