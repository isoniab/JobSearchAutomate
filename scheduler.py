import time
import schedule
from datetime import datetime
from main import run_job_search_automation

def job():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering automated daily scan...")
    try:
        run_job_search_automation()
    except Exception as e:
        print(f"Error during scan: {e}")

# Run scan immediately on launch
job()

# Schedule daily run at 08:00 AM
schedule.every().day.at("08:00").do(job)

print("📅 JobSearchAutomate Scheduler is running in background (Daily at 08:00 AM)...")
while True:
    schedule.run_pending()
    time.sleep(60)
