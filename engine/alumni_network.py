import json
import urllib.parse

class AlumniNetworkFinder:
    def __init__(self):
        self.alumni_schools = ["IIM Indore", "Jorhat Engineering College"]
        self.past_companies = ["ICICI Bank", "American Express", "HP Inc"]

        self.company_slugs = {
            "Meta": "meta",
            "JPMorgan Chase": "jpmorganchase",
            "EY GCC": "ernstandyoung",
            "EY": "ernstandyoung",
            "Databricks": "databricks",
            "Stripe": "stripe",
            "Postman": "postman-platform",
            "AppsFlyer": "appsflyer",
            "Amplitude": "amplitude-analytics",
            "Swiggy": "swiggy-in",
            "Airtel": "airtel",
            "Amazon": "amazon"
        }

    def get_alumni_data(self, company_name, job_title):
        slug = self.company_slugs.get(company_name, company_name.lower().replace(" ", ""))
        comp_quoted = urllib.parse.quote(f'"{company_name}"')

        # Company People Page Filtered by IIM Indore
        company_people_url = f"https://www.linkedin.com/company/{slug}/people/?keywords=IIM%20Indore"
        
        # Boolean Search for Exact IIM Indore Alums at Target Company in Bengaluru
        iim_indore_search = f'https://www.linkedin.com/search/results/people/?keywords={comp_quoted}%20AND%20%22IIM%20Indore%22%20AND%20%22Bengaluru%22'
        
        # Boolean Search for Ex-ICICI Bank / AmEx Colleagues at Target Company in Bengaluru
        past_co_search = f'https://www.linkedin.com/search/results/people/?keywords={comp_quoted}%20AND%20(%22ICICI%20Bank%22%20OR%20%22American%20Express%22)%20AND%20%22Bengaluru%22'
        
        # Boolean Search for Exact Hiring Sales Directors & Recruiters for the role
        hiring_mgr_search = f'https://www.linkedin.com/search/results/people/?keywords={comp_quoted}%20AND%20(%22Director%22%20OR%20%22Head%20of%20Partnerships%22%20OR%20%22Recruiter%22)%20AND%20%22Bengaluru%22'

        outreach_template = f"Hi [Name], I noticed you are an IIM Indore alum leading teams at {company_name}! I am currently Chief Manager at ICICI Bank (scaling commercial payments 7.5x) and exploring the {job_title} role at {company_name} in Bengaluru. Would love to connect for a quick 5-min chat!"

        return {
            "company": company_name,
            "company_people_url": company_people_url,
            "iim_indore_search": iim_indore_search,
            "past_company_search": past_co_search,
            "hiring_manager_search": hiring_mgr_search,
            "outreach_template": outreach_template
        }

if __name__ == "__main__":
    finder = AlumniNetworkFinder()
    res = finder.get_alumni_data("Meta", "Strategic Partner Manager WhatsApp")
    print(json.dumps(res, indent=2))
