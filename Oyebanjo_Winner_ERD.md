# WinnerMIT University USMS — Entity Relationship Diagram

```mermaid
erDiagram
    DEPARTMENTS ||--o{ PROGRAMMES : manages
    DEPARTMENTS ||--o{ LECTURERS : employs
    DEPARTMENTS ||--o{ COURSES : offers
    PROGRAMMES ||--o{ STUDENTS : admits
    COURSES ||--o{ COURSE_OFFERINGS : scheduled_as
    LECTURERS ||--o{ COURSE_OFFERINGS : teaches
    ACADEMIC_SESSIONS ||--o{ COURSE_OFFERINGS : contains
    STUDENTS ||--o{ ENROLMENTS : makes
    COURSE_OFFERINGS ||--o{ ENROLMENTS : receives
    ENROLMENTS ||--o| RESULTS : receives

    DEPARTMENTS {
        int department_id PK
        varchar department_code UK
        varchar department_name UK
        varchar office_location
        timestamp created_at
    }
    PROGRAMMES {
        int programme_id PK
        int department_id FK
        varchar programme_code UK
        varchar programme_name
        varchar award_level
        tinyint duration_years
    }
    STUDENTS {
        int student_id PK
        int programme_id FK
        varchar student_number UK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar phone
        date admission_date
        varchar student_status
    }
    LECTURERS {
        int lecturer_id PK
        int department_id FK
        varchar staff_number UK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar employment_status
    }
    COURSES {
        int course_id PK
        int department_id FK
        varchar course_code UK
        varchar course_title
        tinyint credit_units
        text course_description
    }
    ACADEMIC_SESSIONS {
        int session_id PK
        varchar session_name UK
        date start_date
        date end_date
    }
    COURSE_OFFERINGS {
        int offering_id PK
        int course_id FK
        int lecturer_id FK
        int session_id FK
        varchar semester
        smallint capacity
    }
    ENROLMENTS {
        int enrolment_id PK
        int student_id FK
        int offering_id FK
        date enrolment_date
        varchar enrolment_status
    }
    RESULTS {
        int result_id PK
        int enrolment_id FK, UK
        decimal assessment_score
        decimal examination_score
        decimal total_score
        varchar grade
        varchar result_remarks
    }
```

## Relationship explanation

- One department can manage many programmes, lecturers and courses.
- One programme can have many students.
- One course can have multiple offerings across academic sessions.
- One lecturer can teach multiple course offerings.
- One academic session can contain multiple course offerings.
- Students and course offerings have a many-to-many relationship, resolved through ENROLMENTS.
- Each enrolment can have zero or one result record. A result cannot exist without an enrolment.
