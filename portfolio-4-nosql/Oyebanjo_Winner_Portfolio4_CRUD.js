// ============================================================
// MIT 8103 - Advanced Database Systems
// Portfolio 4: NoSQL and Advanced Data Models
// MONGODB SHELL (mongosh) CRUD OPERATIONS
// Collection: students_transcripts
// Student: Winner Oyebanjo (ID: 301909418)
// ============================================================

// 1. CREATE (Insert New Student Document)
db.students_transcripts.insertOne({
  student_number: "WMIT2026099",
  first_name: "Olamide",
  last_name: "Balogun",
  email: "olamide.balogun@example.edu",
  phone: "+2348000000099",
  admission_date: new Date("2026-09-01"),
  student_status: "Active",
  programme: {
    programme_code: "MIT",
    programme_name: "Master of Information Technology",
    award_level: "Masters",
    duration_years: 2,
    department: {
      department_code: "SCT",
      department_name: "School of Computing and Technology",
      office_location: "Block A"
    }
  },
  academic_records: [
    {
      session_name: "2026/2027",
      semester: "First",
      courses: [
        {
          course_code: "MIT8103",
          course_title: "Advanced Database Systems",
          credit_units: 3,
          lecturer_name: "Chika Nwosu",
          assessment_score: 34.0,
          examination_score: 52.0,
          total_score: 86.0,
          grade: "A",
          grade_point: 5.0,
          result_remarks: "Pass"
        }
      ]
    }
  ]
});

// 2. READ (Find Query with Projection and Filter on Embedded Document)
// Find active Master's students who scored an 'A' in 'MIT8103'
db.students_transcripts.find(
  {
    "programme.award_level": "Masters",
    "academic_records.courses": {
      $elemMatch: {
        course_code: "MIT8103",
        grade: "A"
      }
    }
  },
  {
    student_number: 1,
    first_name: 1,
    last_name: 1,
    "programme.programme_code": 1,
    "academic_records.courses.$": 1
  }
).pretty();

// 3. UPDATE (Atomic Updates on Top-Level and Nested Embedded Arrays)
// A. Update student phone number
db.students_transcripts.updateOne(
  { student_number: "WMIT2026001" },
  { $set: { phone: "+2348099998888" } }
);

// B. Push a new course enrolment into an existing semester array
db.students_transcripts.updateOne(
  { 
    student_number: "WMIT2026099",
    "academic_records.session_name": "2026/2027"
  },
  {
    $push: {
      "academic_records.$.courses": {
        course_code: "MIT8105",
        course_title: "Network Architecture and Protocols",
        credit_units: 3,
        lecturer_name: "Ibrahim Yusuf",
        assessment_score: 30.0,
        examination_score: 48.0,
        total_score: 78.0,
        grade: "A",
        grade_point: 5.0,
        result_remarks: "Pass"
      }
    }
  }
);

// 4. DELETE (Remove Disposable Test Record)
// Deletes the temporary student document created in Step 1
db.students_transcripts.deleteOne({ student_number: "WMIT2026099" });
