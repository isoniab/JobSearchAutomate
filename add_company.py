import json
import urllib.request
import urllib.parse
import re
import os

CONFIG_PATH = "config.json"

def add_company(company_name, career_url=None):
    """Adds a new company to config.json and determines board type."""
    if not os.path.exists(CONFIG_PATH):
        print("config.json not found!")
        return False

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    # Check if company already exists
    existing = [c["name"].lower() for c in config.get("target_companies", [])]
    if company_name.lower() in existing:
        print(f"Company '{company_name}' is already in your target list!")
        return True

    company_entry = {
        "name": company_name,
        "domain": career_url if career_url else f"{company_name.lower().replace(' ', '')}.com",
        "board": "custom",
        "token": company_name.lower().replace(' ', '')
    }

    # Detect if Greenhouse or Lever URL
    if career_url:
        if "greenhouse.io" in career_url or "boards.greenhouse.io" in career_url:
            company_entry["board"] = "greenhouse"
            match = re.search(r'greenhouse\.io/([^/]+)', career_url)
            if match:
                company_entry["token"] = match.group(1)
        elif "lever.co" in career_url or "jobs.lever.co" in career_url:
            company_entry["board"] = "lever"
            match = re.search(r'lever\.co/([^/]+)', career_url)
            if match:
                company_entry["token"] = match.group(1)

    config["target_companies"].append(company_entry)

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Successfully added '{company_name}' to your target company list!")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        comp_name = sys.argv[1]
        url = sys.argv[2] if len(sys.argv) > 2 else None
        add_company(comp_name, url)
    else:
        print("Usage: python3 add_company.py 'Company Name' [Career URL]")
