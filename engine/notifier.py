import os
import json
import subprocess
from datetime import datetime

class Notifier:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def send_mac_notification(self, title, message):
        """Sends a native macOS banner / dialog popup on the user's screen."""
        try:
            script = f'display notification "{message}" with title "{title}" subtitle "JobSearchAutomate Alert"'
            subprocess.run(["osascript", "-e", script], check=False)
        except Exception:
            pass

    def generate_daily_report(self, matched_jobs):
        today_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.reports_dir, f"daily_report_{today_str}.md")

        content = f"# Daily Job Matches Report ({today_str})\n"
        content += f"**Location Filter**: Bangalore / Bengaluru, Karnataka | **Match Threshold**: >= 50%\n\n"

        if not matched_jobs:
            content += "No new high-match jobs found today.\n"
        else:
            content += f"Found **{len(matched_jobs)}** target job openings with >= 50% match score today!\n\n"
            content += "| Company | Job Title | Location | Match Score | Link | Tailored Resume |\n"
            content += "| :--- | :--- | :--- | :---: | :---: | :---: |\n"

            for job in matched_jobs:
                comp = job.get("company", "")
                title = job.get("title", "")
                loc = job.get("location", "")
                score = job.get("match_score", 0)
                url = job.get("url", "#")
                res_path = job.get("tailored_resume_path", "#")
                
                content += f"| **{comp}** | {title} | {loc} | **{score}%** | [View Posting]({url}) | [Tailored Resume](file://{os.path.abspath(res_path)}) |\n"

            content += "\n---\n\n## Detailed Job Breakdown & Recommended Certifications\n\n"
            for idx, job in enumerate(matched_jobs, 1):
                content += f"### {idx}. {job['title']} at {job['company']} (Match: {job['match_score']}%)\n"
                content += f"- **Direct Job URL**: {job['url']}\n"
                content += f"- **Matched Key Strengths**: {', '.join(job.get('matched_skills', []))}\n"
                
                gaps = job.get("skill_gaps", [])
                if gaps:
                    content += f"- **Identified Keyword Gaps**: {', '.join(gaps)}\n"
                
                courses = job.get("recommended_courses", [])
                if courses:
                    content += f"- **Recommended Courses & Certifications to Add**: \n"
                    for c in courses:
                        content += f"  - 🎓 *{c}*\n"
                
                content += f"- **Generated 95-99% Tailored Resume**: [View Resume](file://{os.path.abspath(job['tailored_resume_path'])})\n\n"

        with open(filepath, "w") as f:
            f.write(content)

        # Notify Mac user
        if matched_jobs:
            self.send_mac_notification(
                title=f"🎯 {len(matched_jobs)} New Job Matches in Bangalore!",
                message=f"Top match: {matched_jobs[0]['company']} - {matched_jobs[0]['title']} ({matched_jobs[0]['match_score']}%)"
            )

        return filepath

if __name__ == "__main__":
    notifier = Notifier()
    notifier.send_mac_notification("Test Alert", "JobSearchAutomate engine is working!")
    print("Notification sent.")
