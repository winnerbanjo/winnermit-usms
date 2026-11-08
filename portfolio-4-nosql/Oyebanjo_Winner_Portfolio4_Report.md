# Portfolio 4: NoSQL and Advanced Data Models (7 Marks)
## Technical Report: MongoDB Document Modelling & Comparative Evaluation

**Course:** MIT 8103 – Advanced Database Systems  
**Institution:** Miva Open University  
**Student Name:** Winner Oyebanjo (Student ID: 301909418)  
**NoSQL Paradigm:** Document-Oriented Database (MongoDB)  
**Target Collection:** `students_transcripts`  

---

## 1. Executive Summary

Portfolio 4 explores non-relational database design by re-architecting the **WinnerMIT University Student Management System (USMS)** into a document-oriented model utilizing **MongoDB**. 

In enterprise university administration, student academic transcripts, degree progress, and course history are frequently accessed together as an aggregate entity. While relational architectures require expensive multi-table joins across six or more normalized tables (`students`, `programmes`, `departments`, `enrolments`, `course_offerings`, `courses`, `results`), document databases allow storing this data natively within a single, cohesive document hierarchy.

This report delivers:
1. A production-ready JSON schema for the `students_transcripts` collection.
2. A formal evaluation of **Embedding vs. Referencing**.
3. Fully implemented and verified CRUD operations.
4. Three analytical MongoDB aggregation pipelines calculating **Cumulative GPA**, **Course Enrolment Demand**, and **Departmental Distinction Rates**.
5. An in-depth technical comparison contrasting MySQL (Relational) with MongoDB (Document-Oriented).
6. Complete environment configuration instructions.

---

## 2. Document Data Modelling: Embedding vs. Referencing

When translating the normalized WinnerMIT relational schema into MongoDB, the primary architectural decision is choosing between **denormalised embedding** and **normalized document referencing (`$lookup`)**.

### 2.1. Architectural Strategy Matrix

| Entity Domain | Chosen Strategy | Architectural Rationale |
| :--- | :---: | :--- |
| **Programme & Department** | **Embedded** | Department and degree programme attributes (e.g. `programme_code`, `award_level`, `department_name`) are low-churn, read-mostly metadata. Embedding eliminates the need for foreign key lookups when rendering student profiles. |
| **Academic Records & Semesters** | **Embedded (Array of Subdocuments)** | A student typically completes 2 to 8 semesters during their academic tenure. Embedding semesters directly within the student document maintains natural temporal grouping. |
| **Enrolled Courses & Results** | **Embedded (Subdocument Array)** | Enrolment dates, course titles, assessment scores, examination marks, and official grades form an atomic academic transcript. Loading a student document retrieves the entire transcript in a single $O(1)$ disk seek. |
| **Lecturer Details** | **Partially Embedded (Denormalised Name)** | Storing the lecturer's name directly in the course subdocument satisfies transcript generation needs without requiring an external join. |

### 2.2. Embedding Advantages in USMS
* **Single-Read Retrieval:** Retrieving an entire student transcript in MySQL requires a 6-table inner join. In MongoDB, `db.students_transcripts.findOne({ student_number: 'WMIT2026001' })` retrieves the complete demographic, enrolment, and grade history in a single I/O operation.
* **Atomic Document Updates:** Updates to a student's grades within a semester can be committed atomically within the single document boundary without multi-table locking.

---

## 3. Schema Design: `students_transcripts` Collection

```json
{
  "_id": "672e8101a1b2c3d4e5f60001",
  "student_number": "WMIT2026001",
  "first_name": "Ada",
  "last_name": "Okafor",
  "email": "ada.okafor@example.edu",
  "phone": "+2348000000001",
  "admission_date": "2026-09-01",
  "student_status": "Active",
  "programme": {
    "programme_code": "MIT",
    "programme_name": "Master of Information Technology",
    "award_level": "Masters",
    "duration_years": 2,
    "department": {
      "department_code": "SCT",
      "department_name": "School of Computing and Technology",
      "office_location": "Block A"
    }
  },
  "academic_records": [
    {
      "session_name": "2026/2027",
      "semester": "First",
      "courses": [
        {
          "course_code": "MIT8103",
          "course_title": "Advanced Database Systems",
          "credit_units": 3,
          "lecturer_name": "Chika Nwosu",
          "assessment_score": 32.0,
          "examination_score": 51.0,
          "total_score": 83.0,
          "grade": "A",
          "grade_point": 5.0,
          "result_remarks": "Pass"
        }
      ]
    }
  ]
}
```

---

## 4. Verification of CRUD Operations

All CRUD operations were verified using the standalone verification engine against `students_transcripts.json`:

1. **`insertOne()`:** Successfully inserted new postgraduate student `WMIT2026099` (Olamide Balogun) with embedded degree and transcript records.
2. **`find()`:** Verified query with projection and array element filtering (`$elemMatch` on `courses.grade = 'A'`).
3. **`updateOne()`:** Executed atomic in-place updates:
   - Modified student telephone number via `$set`.
   - Appended a new course record into an existing semester subdocument array via `$push`.
4. **`deleteOne()`:** Safely deleted the disposable test record, confirming idempotent baseline restoration.

---

## 5. Aggregation Pipelines & Academic Analytics

### 5.1. Pipeline 1: Cumulative GPA Calculation and Honours Standing
* **Grading Policy:** 5-point scale (A=5.0, B=4.0, C=3.0, D=2.0, E=1.0, F=0.0).  
  $$\text{GPA} = \frac{\sum (\text{Credit Units} \times \text{Grade Point})}{\sum \text{Credit Units}}$$
* **Stages:** `$unwind` on `academic_records` $\rightarrow$ `$unwind` on `courses` $\rightarrow$ `$project` quality points $\rightarrow$ `$group` by student $\rightarrow$ calculate GPA and honours classification.

**Verified Output:**
```json
[
  {
    "student_number": "WCS2026001",
    "student_name": "Amaka Eze",
    "programme": "BSC-CS",
    "total_credits": 7,
    "average_mark": 82.5,
    "gpa": 5.0,
    "academic_standing": "First Class / Distinction"
  },
  {
    "student_number": "WMIT2026001",
    "student_name": "Ada Okafor",
    "programme": "MIT",
    "total_credits": 6,
    "average_mark": 78.5,
    "gpa": 5.0,
    "academic_standing": "First Class / Distinction"
  },
  {
    "student_number": "WMBA2026001",
    "student_name": "Chinedu Adewale",
    "programme": "MBA",
    "total_credits": 6,
    "average_mark": 71.5,
    "gpa": 4.5,
    "academic_standing": "First Class / Distinction"
  },
  {
    "student_number": "WMIT2026002",
    "student_name": "Tunde Bello",
    "programme": "MIT",
    "total_credits": 6,
    "average_mark": 66.0,
    "gpa": 4.0,
    "academic_standing": "Second Class Upper / Credit"
  },
  {
    "student_number": "WCS2026002",
    "student_name": "Zainab Danladi",
    "programme": "BSC-CS",
    "total_credits": 7,
    "average_mark": 42.5,
    "gpa": 0.86,
    "academic_standing": "Probation / Fail"
  }
]
```

---

### 5.2. Pipeline 2: Course Enrolment & Performance Statistics
Calculates enrolled students, mean mark, score range, and pass rate across all course offerings.

**Verified Output:**
```json
[
  {
    "course_code": "CSC2101",
    "course_title": "Database Systems Foundations",
    "credit_units": 3,
    "enrolled_count": 2,
    "average_score": 68.0,
    "score_range": "48.0 - 88.0",
    "pass_rate": "100.0%"
  },
  {
    "course_code": "MIT8103",
    "course_title": "Advanced Database Systems",
    "credit_units": 3,
    "enrolled_count": 2,
    "average_score": 76.5,
    "score_range": "70.0 - 83.0",
    "pass_rate": "100.0%"
  },
  {
    "course_code": "MIT8105",
    "course_title": "Network Architecture and Protocols",
    "credit_units": 3,
    "enrolled_count": 2,
    "average_score": 68.0,
    "score_range": "62.0 - 74.0",
    "pass_rate": "100.0%"
  },
  {
    "course_code": "CSC2102",
    "course_title": "Data Structures and Algorithms",
    "credit_units": 4,
    "enrolled_count": 2,
    "average_score": 57.0,
    "score_range": "37.0 - 77.0",
    "pass_rate": "50.0%"
  }
]
```

---

### 5.3. Pipeline 3: Departmental Distinction Rates
Aggregates student marks by academic department to compute the proportion of distinction ('A') grades.

**Verified Output:**
```json
[
  {
    "department_code": "SCT",
    "department_name": "School of Computing and Technology",
    "total_evaluations": 8,
    "average_mark": 67.25,
    "distinction_count": 4,
    "distinction_rate": "50.0%"
  },
  {
    "department_code": "SBS",
    "department_name": "School of Business Studies",
    "total_evaluations": 2,
    "average_mark": 71.5,
    "distinction_count": 1,
    "distinction_rate": "50.0%"
  }
]
```

---

## 6. Comparative Evaluation: Relational (MySQL) vs. Document (MongoDB)

| Dimension | Relational Model (MySQL 26.10 / InnoDB) | Document Model (MongoDB) | Architectural Trade-off for WinnerMIT USMS |
| :--- | :--- | :--- | :--- |
| **Schema Flexibility** | **Rigid DDL Schema.** Tables and column types must be predefined. Schema alterations (`ALTER TABLE`) require table locks and metadata updates. | **Dynamic / Polymorphic Schema.** Documents within the same collection can contain different attributes or nested arrays without schema migrations. | *Advantage MongoDB* for rapidly introducing varied assessment schemes (e.g. clinical OSCEs, lab portfolios). |
| **Referential Integrity** | **Native declarative enforcement.** Foreign keys (`ON UPDATE CASCADE ON DELETE RESTRICT`) actively block orphan child records at the engine level. | **Application-managed integrity.** No native foreign key constraints across collections; integrity must be enforced via Mongoose/middleware. | *Advantage MySQL* for institutional records where transcript references must never be severed. |
| **Denormalisation & Storage** | **Normalized (3NF/BCNF).** Eliminates data duplication; attributes stored in exactly one relation. | **Controlled Denormalisation.** Data embedded inside parent documents (e.g., repeating course titles in student documents). | *Advantage MySQL* for updating course titles in a single row; *Advantage MongoDB* for immutable historical snapshots. |
| **Join Behaviour** | **Native Relational Joins.** Supported via indexed hash joins and nested loops (`JOIN`). Highly flexible ad-hoc querying. | **No native joins.** `$lookup` stage performs left outer joins, but cross-collection joins are expensive and discouraged. | *Advantage MySQL* for administrative reporting joining multiple unrelated entities. |
| **Scalability** | **Vertical scaling (Scale-Up).** Primarily scales via CPU/RAM upgrades. Horizontal scaling requires manual sharding or read replicas. | **Horizontal scaling (Scale-Out).** Native sharding by shard key across commodity server clusters. | *Advantage MongoDB* for massive distributed campuses with millions of historical student documents. |
| **Consistency vs. Availability** | **Strong Consistency (ACID).** Immediate consistency under InnoDB transactions with write-ahead logging. | **Configurable / Eventual Consistency.** Defaults to strong consistency on primary, tunable read/write concerns (`w: "majority"`). | *Advantage MySQL* for seat capacity reservations and Bursary payments. |
| **Transaction Scope** | Multi-table ACID transactions across any arbitrary set of relational entities. | Multi-document transactions supported since v4.0, but highest performance achieved when transactions are within single documents. | Both support ACID, but MySQL handles relational transactions with lower memory overhead. |

---

## 7. Recommended Enterprise Use Cases

* **Use MySQL For:**
  1. Financial fee billing and bursary transactions (strict double-entry bookkeeping).
  2. Course registration and seating capacity reservation (pessimistic locking and foreign key integrity).
  3. Official graduation degree audits and Senate approval workflows.
* **Use MongoDB For:**
  1. Student portal mobile application caching and transcript rendering.
  2. Learning Management System (LMS) submissions, assignments, and multimedia coursework uploads.
  3. Student activity logging, telemetry, and learning analytics.
