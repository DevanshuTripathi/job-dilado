from utils import is_global_fresher_job, is_global_software_job
from typing import List
from models import Job
import hashlib
import requests

"""
GreenHouse API structure
company: Company via array
job: text
apply_url: applyUrl
"""

LEVER_COMPANIES = [
    'meesho', 'mindtickle', 'paytm', 'drivetrain', 'doxel', 'entrata',
    'peoplegrove', 'netomi', 'binance', 'entrata', 'spreetail',
    'nium', 'shyftlabs'
]

def get_base_url(company) :
    return f"https://api.lever.co/v0/postings/{company}?mode=json"

def is_fresher_job(job) :
    title = job.get("text") or ""
    content = job.get("descriptionPlain") or ""

    return is_global_fresher_job(title, content)

def is_software_job(job) :
    title = job.get("text")
    category = job.get("categories") or {}
    dept = category.get("department") or ""

    return is_global_software_job(f"{title} {dept}")

def parse_jobs_to_model(jobs) :
    lv_jobs: List[Job] = []

    for job in jobs :
        model_job = Job(company=job.get("company_name"), job=job["text"], apply_url=job["applyUrl"], job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url
        
        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        lv_jobs.append(model_job)
    print("LEVER JOBS DONE")
    return lv_jobs

def is_indian_job(job) :
    return "IN" == (job.get("country") or "")

def get_lever_jobs() :
    lv_jobs = []
    for company in LEVER_COMPANIES :
        response = requests.get(get_base_url(company))

        if response.status_code != 200 :
            continue

        data = response.json()

        for d in data :
            d["company_name"] = company

        if data :
            for job in data :
                if is_indian_job(job) and is_software_job(job) and is_fresher_job(job) :
                    lv_jobs.append(job)

    return parse_jobs_to_model(lv_jobs)

# print(get_lever_jobs())