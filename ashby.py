import requests
from utils import is_global_fresher_job, is_global_software_job, is_global_india_job
from models import Job
from typing import List
import hashlib

ASHBY_COMPANIES = [
    'handshake', 'astronomer', 
    # 'crusoe', 'cohere', 'cartesia', 'confluent',
    # 'menlosecurity', 'pavebank', 'pylon', 'nooks', 'cerebras', 'northwoodspace',
    'certifyos', 'anyscale'
]

def get_base_url(company) :
    return f"https://api.ashbyhq.com/posting-api/job-board/{company}?includeCompensation=true"

def is_fresher_job(job) :
    title = job.get("title") or ""
    content = job.get("descriptionPlain") or ""

    return is_global_fresher_job(title, content)

def is_software_job(job) :
    title = job.get("title") or ""
    job_dept = f"{job.get("department") or "" } {job.get("team") or ""}"

    return is_global_software_job(f"{title} {job_dept}")

def parse_jobs_to_model(jobs) :
    ab_jobs: List[Job] = []

    for job in jobs :
        model_job = Job(company=job.get("company_name") or "", job=job.get("title") or "", apply_url=job.get("applyUrl") or "", job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url

        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        ab_jobs.append(model_job)
    print("ASHBY JOBS DONE")
    return ab_jobs

def is_india_job(job) :
    location = job.get("location") or ""

    return is_global_india_job(location)

def get_ashby_jobs() :
    ab_jobs = []
    for company in ASHBY_COMPANIES :
        response = requests.get(get_base_url(company))
        data = response.json()

        jobs = data.get("jobs")

        for j in jobs :
            j["company_name"] = company

        if jobs :
            for job in jobs :
                if is_india_job(job) and is_software_job(job) and is_fresher_job(job) :
                    ab_jobs.append(job)

    return parse_jobs_to_model(ab_jobs)