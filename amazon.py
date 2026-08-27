import requests
import re
from models import Job
import hashlib
from utils import is_global_fresher_job, is_global_software_job

url = "https://amazon.jobs/en/search.json"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

params = {
    # "normalized_country_code": ["IND"],
    "country": "IND",

}

def is_fresher_job(job) :
    if job.get("university_job") or job.get("is_intern"):
        return True

    job_category = job.get("job_category", "").lower()
    if "university" in job_category or "internship" in job_category:
        return True

    title = job.get("title", "").lower() 
    basic_qualification = job.get("basic_qualifications", "").lower()

    return is_global_fresher_job(title, basic_qualification)

def is_software_job(job) :
    title = job.get("title", "").lower()
    job_category = job.get("job_category", "").lower()
    job_family = job.get("job_family", "").lower()

    return is_global_software_job(title + " " + job_category + " " + job_family)

def parse_jobs_to_model(jobs) :
    amazon_jobs: list[Job] = []

    for job in jobs :
        model_job = Job(company="Amazon", job=job["title"], apply_url=job["url_next_step"], job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url

        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        amazon_jobs.append(model_job)
    print("AMAZON JOBS DONE")
    return amazon_jobs

def get_amazon_jobs(params = params) :
    response = requests.get(url, params)
    data = response.json()
    jobs = data["jobs"]

    software_jobs = [job for job in jobs if is_software_job(job)]
    wow_jobs = [job for job in software_jobs if is_fresher_job(job)]

    return parse_jobs_to_model(wow_jobs)