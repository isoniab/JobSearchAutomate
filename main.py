import os
import json
from datetime import datetime
from engine.job_fetcher import JobFetcher
from engine.matcher import Matcher
from engine.tailor import ResumeTailor
from engine.notifier import Notifier

def run_job_search_automation():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting JobSearchAutomate Engine...")
    
    # 1. Fetch job listings
    fetcher = JobFetcher()
    jobs = fetcher.fetch_all_jobs()
    print(f"Fetched {len(jobs)} total jobs matching Bangalore location preference.")

    # 2. Evaluate and match jobs against Sonia's profile
    matcher = Matcher()
    tailor = ResumeTailor()
    matched_jobs = []

    for job in jobs:
        eval_res = matcher.evaluate_job(job)
        if eval_res["is_match"]:
            job["match_score"] = eval_res["match_score"]
            job["matched_skills"] = eval_res["matched_skills"]
            job["skill_gaps"] = eval_res["skill_gaps"]
            job["recommended_courses"] = eval_res["recommended_courses"]
            
            # Generate 95-99% tailored resume file for this specific JD
            resume_path = tailor.generate_tailored_resume(job)
            job["tailored_resume_path"] = resume_path
            
            matched_jobs.append(job)

    # Sort matched jobs by match score descending
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)

    # 3. Generate daily markdown digest report & mac notification
    notifier = Notifier()
    report_path = notifier.generate_daily_report(matched_jobs)
    print(f"Generated Daily Report at: {report_path}")

    # 4. Save latest matches for Web UI Dashboard
    os.makedirs("data", exist_ok=True)
    dashboard_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location_filter": "Bangalore / Bengaluru",
        "total_matched": len(matched_jobs),
        "jobs": matched_jobs
    }
    with open("data/latest_matches.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)

    print(f"Automated scan completed! Found {len(matched_jobs)} high-fit jobs.")
    return matched_jobs

if __name__ == "__main__":
    run_job_search_automation()
