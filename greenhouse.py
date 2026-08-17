import requests
from utils import is_global_software_job, is_global_fresher_job
from models import Job
from typing import List
import hashlib

"""
GreenHouse API structure
company: company_name
job: title
apply_url: absolute_url
"""

GH_COMPANIES = ['Stripe', 'Cloudflare', 'Twilio', 'Atlassian', 'Datadog', 'Rubrik', 'Coinbase', 'Canva', 'Airbnb', 'Razorpay', 'Meesho']

# GreenHouse Base URL for job board
# Pass company without spaces
def get_base_url(company) :
    return f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"

def is_fresher_job(job) :
    title = job.get("title")
    content = job.get("content")

    return is_global_fresher_job(title + " " + content)

def is_software_job(job) :
    title = job.get("title")
    job_dept = ""
    dept = job.get("departments")
    for d in dept :
        job_dept += d.get("name")

    return is_global_software_job(title + " " + job_dept)

def parse_jobs_to_model(jobs) :
    gh_jobs: List[Job] = []

    for job in jobs :
        model_job = Job(company=job.get("company_name"), job=job["title"], apply_url=job["absolute_url"], job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url
        
        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        gh_jobs.append(model_job)

    return gh_jobs

def get_greenhouse_jobs() :
    gh_jobs = []
    for company in GH_COMPANIES :

        response = requests.get(get_base_url(company))
        data = response.json()

        jobs = data.get("jobs")

        if jobs :
            for job in jobs :
                if is_software_job(job) and is_fresher_job(job) :
                    gh_jobs.append(job)

    return parse_jobs_to_model(gh_jobs)