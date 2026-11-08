// ============================================================
// MIT 8103 - Advanced Database Systems
// Portfolio 4: NoSQL and Advanced Data Models
// MONGODB AGGREGATION PIPELINES
// Collection: students_transcripts
// Student: Winner Oyebanjo (ID: 301909418)
// ============================================================

// PIPELINE 1: Student Cumulative GPA and Academic Standing Calculation
// Grading Assumptions:
// A (70-100) = 5.0 points | B (60-69) = 4.0 points | C (50-59) = 3.0 points
// D (45-49) = 2.0 points  | E (40-44) = 1.0 points | F (0-39) = 0.0 points
// GPA = SUM(credit_units * grade_point) / SUM(credit_units)
db.students_transcripts.aggregate([
  { $unwind: "$academic_records" },
  { $unwind: "$academic_records.courses" },
  {
    $project: {
      student_number: 1,
      full_name: { $concat: ["$first_name", " ", "$last_name"] },
      programme_code: "$programme.programme_code",
      award_level: "$programme.award_level",
      course_code: "$academic_records.courses.course_code",
      credit_units: "$academic_records.courses.credit_units",
      grade_point: "$academic_records.courses.grade_point",
      total_score: "$academic_records.courses.total_score",
      quality_points: {
        $multiply: [
          "$academic_records.courses.credit_units",
          "$academic_records.courses.grade_point"
        ]
      }
    }
  },
  {
    $group: {
      _id: "$student_number",
      student_name: { $first: "$full_name" },
      programme: { $first: "$programme_code" },
      award_level: { $first: "$award_level" },
      total_credits_registered: { $sum: "$credit_units" },
      total_quality_points: { $sum: "$quality_points" },
      average_mark: { $avg: "$total_score" }
    }
  },
  {
    $project: {
      _id: 0,
      student_number: "$_id",
      student_name: 1,
      programme: 1,
      award_level: 1,
      total_credits: "$total_credits_registered",
      average_mark: { $round: ["$average_mark", 2] },
      gpa: {
        $round: [
          { $divide: ["$total_quality_points", "$total_credits_registered"] },
          2
        ]
      },
      academic_standing: {
        $cond: {
          if: { $gte: [{ $divide: ["$total_quality_points", "$total_credits_registered"] }, 4.5] },
          then: "First Class / Distinction",
          else: {
            $cond: {
              if: { $gte: [{ $divide: ["$total_quality_points", "$total_credits_registered"] }, 3.5] },
              then: "Second Class Upper / Credit",
              else: {
                $cond: {
                  if: { $gte: [{ $divide: ["$total_quality_points", "$total_credits_registered"] }, 2.4] },
                  then: "Second Class Lower / Pass",
                  else: "Probation / Fail"
                }
              }
            }
          }
        }
      }
    }
  },
  { $sort: { gpa: -1 } }
]);

// PIPELINE 2: Course Enrolment & Performance Statistics
db.students_transcripts.aggregate([
  { $unwind: "$academic_records" },
  { $unwind: "$academic_records.courses" },
  {
    $group: {
      _id: "$academic_records.courses.course_code",
      course_title: { $first: "$academic_records.courses.course_title" },
      credit_units: { $first: "$academic_records.courses.credit_units" },
      enrolled_count: { $sum: 1 },
      average_score: { $avg: "$academic_records.courses.total_score" },
      min_score: { $min: "$academic_records.courses.total_score" },
      max_score: { $max: "$academic_records.courses.total_score" },
      passes: {
        $sum: {
          $cond: [{ $eq: ["$academic_records.courses.result_remarks", "Pass"] }, 1, 0]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      course_title: 1,
      credit_units: 1,
      enrolled_count: 1,
      average_score: { $round: ["$average_score", 2] },
      score_range: { $concat: [{ $toString: "$min_score" }, " - ", { $toString: "$max_score" }] },
      pass_rate: {
        $concat: [
          { $toString: { $round: [{ $multiply: [{ $divide: ["$passes", "$enrolled_count"] }, 100] }, 1] } },
          "%"
        ]
      }
    }
  },
  { $sort: { enrolled_count: -1, average_score: -1 } }
]);

// PIPELINE 3: Departmental Performance and Distinction Analysis
db.students_transcripts.aggregate([
  { $unwind: "$academic_records" },
  { $unwind: "$academic_records.courses" },
  {
    $group: {
      _id: "$programme.department.department_code",
      department_name: { $first: "$programme.department.department_name" },
      total_course_evaluations: { $sum: 1 },
      overall_avg_mark: { $avg: "$academic_records.courses.total_score" },
      distinctions: {
        $sum: {
          $cond: [{ $eq: ["$academic_records.courses.grade", "A"] }, 1, 0]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      department_code: "$_id",
      department_name: 1,
      total_evaluations: "$total_course_evaluations",
      average_mark: { $round: ["$overall_avg_mark", 2] },
      distinction_count: "$distinctions",
      distinction_rate: {
        $concat: [
          { $toString: { $round: [{ $multiply: [{ $divide: ["$distinctions", "$total_course_evaluations"] }, 100] }, 1] } },
          "%"
        ]
      }
    }
  },
  { $sort: { average_mark: -1 } }
]);
