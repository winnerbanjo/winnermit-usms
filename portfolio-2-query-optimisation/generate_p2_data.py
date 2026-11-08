# generate_p2_data.py
# Generates realistic synthetic benchmark dataset for winnermit_usms_p2
import random

def generate_sql():
    sql = []
    sql.append("USE winnermit_usms_p2;\n")

    # Departments (4)
    depts = [
        ('SCT', 'School of Computing and Technology', 'Block A'),
        ('SBS', 'School of Business Studies', 'Block B'),
        ('SOE', 'School of Engineering', 'Block C'),
        ('SHS', 'School of Health Sciences', 'Block D')
    ]
    sql.append("INSERT IGNORE INTO departments (department_code, department_name, office_location) VALUES")
    sql.append(",\n".join([f"('{c}', '{n}', '{loc}')" for c, n, loc in depts]) + ";\n")

    # Programmes (6)
    progs = [
        (1, 'MIT', 'Master of Information Technology', 'Masters', 2),
        (1, 'BSC-CS', 'BSc Computer Science', 'Undergraduate', 4),
        (1, 'MSC-DS', 'MSc Data Science', 'Masters', 2),
        (2, 'MBA', 'Master of Business Administration', 'Masters', 2),
        (3, 'BENG-SE', 'BEng Software Engineering', 'Undergraduate', 5),
        (4, 'BSC-HI', 'BSc Health Informatics', 'Undergraduate', 4)
    ]
    sql.append("INSERT IGNORE INTO programmes (department_id, programme_code, programme_name, award_level, duration_years) VALUES")
    sql.append(",\n".join([f"({d}, '{c}', '{n}', '{a}', {dur})" for d, c, n, a, dur in progs]) + ";\n")

    # Lecturers (12)
    first_names = ['Chika', 'Ibrahim', 'Grace', 'Oluwaseun', 'Emeka', 'Fatima', 'Babatunde', 'Ngozi', 'Amina', 'Kelechi', 'Folake', 'Tari']
    last_names = ['Nwosu', 'Yusuf', 'Adeyemi', 'Ogunleye', 'Okeke', 'Bello', 'Balogun', 'Eze', 'Abubakar', 'Nnamdi', 'Ajayi', 'Briggs']
    sql.append("INSERT IGNORE INTO lecturers (department_id, staff_number, first_name, last_name, email, employment_status) VALUES")
    lect_rows = []
    for i in range(12):
        dept_id = (i % 4) + 1
        staff_num = f"WML{i+1:03d}"
        fn = first_names[i]
        ln = last_names[i]
        email = f"{fn.lower()}.{ln.lower()}{i+1}@example.edu"
        lect_rows.append(f"({dept_id}, '{staff_num}', '{fn}', '{ln}', '{email}', 'Active')")
    sql.append(",\n".join(lect_rows) + ";\n")

    # Courses (15)
    courses = [
        (1, 'MIT8103', 'Advanced Database Systems', 3, 'Relational, NoSQL and distributed database concepts.'),
        (1, 'MIT8105', 'Network Architecture and Protocols', 3, 'Network models, protocols and architecture.'),
        (1, 'CSC2101', 'Database Systems Foundations', 3, 'Relational model, SQL querying, and database normalization.'),
        (1, 'CSC2102', 'Data Structures and Algorithms', 4, 'Abstract data types, trees, graphs, sorting and search.'),
        (1, 'CSC3105', 'Web Application Development', 3, 'Full-stack modern web application architecture.'),
        (1, 'DSC8101', 'Applied Machine Learning', 3, 'Supervised and unsupervised learning, evaluation metrics.'),
        (1, 'DSC8102', 'Big Data Engineering', 3, 'Distributed processing engines and pipeline architectures.'),
        (2, 'MBA8101', 'Strategic Management', 3, 'Strategy formulation and organisational performance.'),
        (2, 'MBA8102', 'Corporate Finance and Accounting', 3, 'Financial statement analysis and capital budgeting.'),
        (2, 'MBA8103', 'Marketing Management', 3, 'Consumer behavior, market research, and brand strategy.'),
        (3, 'ENG1101', 'Engineering Mathematics I', 4, 'Calculus, linear algebra, and differential equations.'),
        (3, 'ENG2105', 'Computer Systems Architecture', 3, 'Instruction set design, pipelining, and memory hierarchies.'),
        (3, 'ENG3102', 'Embedded Systems Engineering', 3, 'Microcontroller architecture, real-time operating systems.'),
        (4, 'HLT1101', 'Introduction to Health Informatics', 3, 'Health record systems, privacy standards, and clinical data.'),
        (4, 'HLT2103', 'Biostatistics and Clinical Analytics', 3, 'Statistical inference, hypothesis testing, clinical trials.')
    ]
    sql.append("INSERT IGNORE INTO courses (department_id, course_code, course_title, credit_units, course_description) VALUES")
    sql.append(",\n".join([f"({d}, '{c}', '{t}', {cu}, '{desc}')" for d, c, t, cu, desc in courses]) + ";\n")

    # Academic Sessions (2)
    sql.append("INSERT IGNORE INTO academic_sessions (session_name, start_date, end_date) VALUES")
    sql.append("('2025/2026', '2025-09-01', '2026-08-31'),\n('2026/2027', '2026-09-01', '2027-08-31');\n")

    # Course Offerings (24)
    # Courses 1 to 12 in Session 1 & 2
    sql.append("INSERT IGNORE INTO course_offerings (course_id, lecturer_id, session_id, semester, capacity) VALUES")
    off_rows = []
    for c_id in range(1, 13):
        lect_id = ((c_id - 1) % 12) + 1
        off_rows.append(f"({c_id}, {lect_id}, 1, 'First', 80)")
    for c_id in range(1, 13):
        lect_id = (c_id % 12) + 1
        off_rows.append(f"({c_id}, {lect_id}, 2, 'First', 90)")
    sql.append(",\n".join(off_rows) + ";\n")

    # Students (100)
    sql.append("INSERT IGNORE INTO students (programme_id, student_number, first_name, last_name, email, phone, admission_date, student_status) VALUES")
    stud_rows = []
    first_pool = ['Ada', 'Tunde', 'Amaka', 'Chinedu', 'Zainab', 'Olamide', 'Ifeanyi', 'Khadijah', 'Damilola', 'Obinna',
                  'Fisayo', 'Yakubu', 'Uche', 'Aisha', 'Segun', 'Nkechi', 'Mustapha', 'Yetunde', 'Efe', 'Maryam']
    last_pool = ['Okafor', 'Bello', 'Eze', 'Adewale', 'Danladi', 'Balogun', 'Okoro', 'Garba', 'Ojo', 'Nnamani',
                 'Suleiman', 'Alabi', 'Chukwu', 'Odu', 'Sani', 'Lawal', 'Oni', 'Bassey', 'Kanu', 'Idris']
    random.seed(42)
    for i in range(1, 101):
        p_id = random.randint(1, 6)
        s_num = f"WMIT{2026000 + i}"
        fn = first_pool[i % len(first_pool)]
        ln = last_pool[(i * 3) % len(last_pool)]
        email = f"{fn.lower()}.{ln.lower()}{i}@student.example.edu"
        phone = f"+23480{i:08d}"
        stud_rows.append(f"({p_id}, '{s_num}', '{fn}', '{ln}', '{email}', '{phone}', '2026-09-01', 'Active')")
    sql.append(",\n".join(stud_rows) + ";\n")

    # Enrolments (250)
    sql.append("INSERT IGNORE INTO enrolments (student_id, offering_id, enrolment_date, enrolment_status) VALUES")
    enr_rows = []
    enr_set = set()
    enr_id = 1
    # Distribute 2-3 enrolments per student across available offerings
    for s_id in range(1, 101):
        num_courses = random.randint(2, 3)
        off_choices = random.sample(range(1, 25), num_courses)
        for off_id in off_choices:
            if (s_id, off_id) not in enr_set:
                enr_set.add((s_id, off_id))
                enr_rows.append(f"({s_id}, {off_id}, '2026-09-05', 'Enrolled')")
    sql.append(",\n".join(enr_rows) + ";\n")

    # Results (for first 200 enrolments)
    sql.append("INSERT IGNORE INTO results (enrolment_id, assessment_score, examination_score, grade, result_remarks) VALUES")
    res_rows = []
    for eid in range(1, len(enr_rows) - 20):  # leave some pending
        ass = round(random.uniform(18.0, 38.0), 2)
        exam = round(random.uniform(25.0, 58.0), 2)
        tot = ass + exam
        if tot >= 70:
            grd, rem = 'A', 'Pass'
        elif tot >= 60:
            grd, rem = 'B', 'Pass'
        elif tot >= 50:
            grd, rem = 'C', 'Pass'
        elif tot >= 45:
            grd, rem = 'D', 'Pass'
        elif tot >= 40:
            grd, rem = 'E', 'Pass'
        else:
            grd, rem = 'F', 'Fail'
        res_rows.append(f"({eid}, {ass:.2f}, {exam:.2f}, '{grd}', '{rem}')")
    sql.append(",\n".join(res_rows) + ";\n")

    return "\n".join(sql)

if __name__ == '__main__':
    content = generate_sql()
    with open('/Users/oyekunle/Downloads/winnermit/portfolio-2-query-optimisation/Oyebanjo_Winner_Portfolio2_Data.sql', 'w') as f:
        f.write(content)
    print("Generated Oyebanjo_Winner_Portfolio2_Data.sql successfully.")
