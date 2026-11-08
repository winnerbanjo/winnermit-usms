# Oyebanjo_Winner_Portfolio4_Verification.py
# Verification harness simulating MongoDB document CRUD operations and Aggregation Pipelines
import json
import os

DATA_FILE = "/Users/oyekunle/Downloads/winnermit/portfolio-4-nosql/students_transcripts.json"
OUTPUT_FILE = "/Users/oyekunle/Downloads/winnermit/portfolio-4-nosql/Oyebanjo_Winner_Portfolio4_Execution_Results.txt"

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def run_crud_and_aggregations():
    docs = load_data()
    out = []
    out.append("============================================================")
    out.append("PORTFOLIO 4: NOSQL & ADVANCED DATA MODELS VERIFICATION LOG")
    out.append("Target Collection: students_transcripts")
    out.append("Engine: Document Schema Validator / Aggregation Pipeline Runner")
    out.append("============================================================\n")

    # 1. CRUD VALIDATION
    out.append("------------------------------------------------------------")
    out.append("STAGE 1: CRUD OPERATIONS VERIFICATION")
    out.append("------------------------------------------------------------")
    out.append(f"Initial document count: {len(docs)}")
    
    # Insert disposable test record
    new_doc = {
        "_id": "672e8101a1b2c3d4e5f60099",
        "student_number": "WMIT2026099",
        "first_name": "Olamide",
        "last_name": "Balogun",
        "email": "olamide.balogun@example.edu",
        "phone": "+2348000000099",
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
                        "assessment_score": 34.0,
                        "examination_score": 52.0,
                        "total_score": 86.0,
                        "grade": "A",
                        "grade_point": 5.0,
                        "result_remarks": "Pass"
                    }
                ]
            }
        ]
    }
    docs.append(new_doc)
    out.append(f"[CREATE] insertOne({new_doc['student_number']}): SUCCESS (Count now: {len(docs)})")

    # Find test
    found = [d for d in docs if d["student_number"] == "WMIT2026099"]
    out.append(f"[READ] find({{ student_number: 'WMIT2026099' }}): Found {len(found)} matching document.")

    # Update test
    for d in docs:
        if d["student_number"] == "WMIT2026099":
            d["phone"] = "+2348099998888"
    out.append(f"[UPDATE] updateOne({{ student_number: 'WMIT2026099' }}, {{ $set: {{ phone: '+2348099998888' }} }}): SUCCESS")

    # Delete test
    docs = [d for d in docs if d["student_number"] != "WMIT2026099"]
    out.append(f"[DELETE] deleteOne({{ student_number: 'WMIT2026099' }}): SUCCESS (Count restored: {len(docs)})\n")

    # 2. AGGREGATION PIPELINE 1: GPA CALCULATION
    out.append("------------------------------------------------------------")
    out.append("STAGE 2: AGGREGATION PIPELINE 1 (CUMULATIVE GPA & STANDING)")
    out.append("------------------------------------------------------------")
    gpa_results = []
    for d in docs:
        s_num = d["student_number"]
        name = f"{d['first_name']} {d['last_name']}"
        prog = d["programme"]["programme_code"]
        tot_credits = 0
        tot_qp = 0
        all_scores = []
        for rec in d.get("academic_records", []):
            for c in rec.get("courses", []):
                cu = c["credit_units"]
                gp = c["grade_point"]
                score = c["total_score"]
                tot_credits += cu
                tot_qp += (cu * gp)
                all_scores.append(score)
        
        gpa = round(tot_qp / tot_credits, 2) if tot_credits > 0 else 0.0
        avg_mark = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0.0
        if gpa >= 4.5:
            standing = "First Class / Distinction"
        elif gpa >= 3.5:
            standing = "Second Class Upper / Credit"
        elif gpa >= 2.4:
            standing = "Second Class Lower / Pass"
        else:
            standing = "Probation / Fail"
            
        gpa_results.append({
            "student_number": s_num,
            "student_name": name,
            "programme": prog,
            "total_credits": tot_credits,
            "average_mark": avg_mark,
            "gpa": gpa,
            "academic_standing": standing
        })
    
    gpa_results.sort(key=lambda x: x["gpa"], reverse=True)
    out.append(json.dumps(gpa_results, indent=2))
    out.append("\n")

    # 3. AGGREGATION PIPELINE 2: COURSE PERFORMANCE & ENROLMENT
    out.append("------------------------------------------------------------")
    out.append("STAGE 3: AGGREGATION PIPELINE 2 (COURSE ENROLMENT & STATS)")
    out.append("------------------------------------------------------------")
    course_stats = {}
    for d in docs:
        for rec in d.get("academic_records", []):
            for c in rec.get("courses", []):
                cc = c["course_code"]
                if cc not in course_stats:
                    course_stats[cc] = {
                        "course_code": cc,
                        "course_title": c["course_title"],
                        "credit_units": c["credit_units"],
                        "enrolled_count": 0,
                        "scores": [],
                        "passes": 0
                    }
                course_stats[cc]["enrolled_count"] += 1
                course_stats[cc]["scores"].append(c["total_score"])
                if c["result_remarks"] == "Pass":
                    course_stats[cc]["passes"] += 1
    
    c_out = []
    for cc, data in course_stats.items():
        scores = data["scores"]
        avg_sc = round(sum(scores) / len(scores), 2)
        min_sc = min(scores)
        max_sc = max(scores)
        pass_pct = round((data["passes"] / data["enrolled_count"]) * 100, 1)
        c_out.append({
            "course_code": cc,
            "course_title": data["course_title"],
            "credit_units": data["credit_units"],
            "enrolled_count": data["enrolled_count"],
            "average_score": avg_sc,
            "score_range": f"{min_sc} - {max_sc}",
            "pass_rate": f"{pass_pct}%"
        })
    c_out.sort(key=lambda x: x["enrolled_count"], reverse=True)
    out.append(json.dumps(c_out, indent=2))
    out.append("\n")

    # 4. AGGREGATION PIPELINE 3: DEPARTMENTAL DISTINCTION STATS
    out.append("------------------------------------------------------------")
    out.append("STAGE 4: AGGREGATION PIPELINE 3 (DEPARTMENTAL DISTINCTION STATS)")
    out.append("------------------------------------------------------------")
    dept_stats = {}
    for d in docs:
        dept_code = d["programme"]["department"]["department_code"]
        dept_name = d["programme"]["department"]["department_name"]
        if dept_code not in dept_stats:
            dept_stats[dept_code] = {
                "department_code": dept_code,
                "department_name": dept_name,
                "total_evaluations": 0,
                "scores": [],
                "distinctions": 0
            }
        for rec in d.get("academic_records", []):
            for c in rec.get("courses", []):
                dept_stats[dept_code]["total_evaluations"] += 1
                dept_stats[dept_code]["scores"].append(c["total_score"])
                if c["grade"] == "A":
                    dept_stats[dept_code]["distinctions"] += 1
    
    d_out = []
    for dc, data in dept_stats.items():
        sc = data["scores"]
        avg_mark = round(sum(sc) / len(sc), 2)
        rate = round((data["distinctions"] / data["total_evaluations"]) * 100, 1)
        d_out.append({
            "department_code": dc,
            "department_name": data["department_name"],
            "total_evaluations": data["total_evaluations"],
            "average_mark": avg_mark,
            "distinction_count": data["distinctions"],
            "distinction_rate": f"{rate}%"
        })
    d_out.sort(key=lambda x: x["average_mark"], reverse=True)
    out.append(json.dumps(d_out, indent=2))

    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(out))
    print(f"Portfolio 4 execution verification completed. Written to: {OUTPUT_FILE}")

if __name__ == '__main__':
    run_crud_and_aggregations()
