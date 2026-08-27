import requests
from utils import is_global_software_job, is_global_fresher_job, is_global_india_job
from models import Job
from typing import List
import hashlib

"""
GreenHouse API structure
company: company_name
job: title
apply_url: absolute_url
"""

GH_COMPANIES = [
    'stripe', 'cloudflare', 'twilio', 'atlassian', 'datadog', 'rubrik', 
    'coinbase', 'canva', 'airbnb', 'razorpay', 'meesho', 'nirmata',
    'enterpret', 'groww', 'ethoslife', 'commercelq', 'amtechsoftware',
    'yipitdata', 'applovin', 'motive'
]

# GreenHouse Base URL for job board
# Pass company without spaces
def get_base_url(company) :
    return f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"

def is_fresher_job(job) :
    title = job.get("title") or ""
    content = job.get("content") or ""

    return is_global_fresher_job(title, content)

def is_software_job(job) :
    title = job.get("title") or ""
    job_dept = ""
    dept = job.get("departments") or []
    for d in dept :
        job_dept += d.get("name") or ""

    return is_global_software_job(f"{title} {job_dept}")

def parse_jobs_to_model(jobs) :
    gh_jobs: List[Job] = []

    for job in jobs :
        model_job = Job(company=job.get("company_name") or "", job=job["title"], apply_url=job["absolute_url"], job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url
        
        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        gh_jobs.append(model_job)
    print("GH JOBS DONE!")
    return gh_jobs

def is_india_job(job) :
    location = job.get("location") or {}
    loc_name = location.get("name") or ""

    return is_global_india_job(loc_name)

def get_greenhouse_jobs() :
    gh_jobs = []
    for company in GH_COMPANIES :

        response = requests.get(get_base_url(company))
        data = response.json()

        jobs = data.get("jobs")

        if jobs :
            for job in jobs :
                if is_india_job(job) and is_software_job(job) and is_fresher_job(job) :
                    gh_jobs.append(job)

    return parse_jobs_to_model(gh_jobs)

# print(get_greenhouse_jobs())