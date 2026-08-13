import requests
import re
from models import Job
import hashlib

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

SENIOR_TITLE_PATTERN = r"\b(senior|sr|lead|manager|head|principal|staff|director|vp)\b"
EXPLICIT_SENIOR_EXP = r"\b([2-9]|\d{2})\+\s*years?\b|\b([3-9]|\d{2})\s*years?\b"
ENTRY_EXP_PATTERN = r"\b(0|1)\s*(?:-\s*\d+)?\s*years?\b|\b(fresher|entry[- ]level|intern(?:ship)?)\b"

SOFTWARE_PATTERN = r"\b(software|sde|swe)\b"

def is_fresher_job(job) :
    title = job.get("title", "").lower() 
    basic_qualification = job.get("basic_qualifications", "").lower()

    if re.search(SENIOR_TITLE_PATTERN, title):
        return False

    if job.get("university_job") or job.get("is_intern"):
        return True

    if re.search(EXPLICIT_SENIOR_EXP, basic_qualification):
        return False

    if re.search(ENTRY_EXP_PATTERN, basic_qualification):
        return True

    job_category = job.get("job_category", "").lower()
    if "university" in job_category or "internship" in job_category:
        return True

    return True

def is_software_job(job) :
    title = job.get("title", "").lower()
    job_category = job.get("job_category", "").lower()
    job_family = job.get("job_family", "").lower()

    if re.search(SOFTWARE_PATTERN, title) or re.search(SOFTWARE_PATTERN, job_category) or re.search(SOFTWARE_PATTERN, job_family) :
        return True

    return False

def parse_jobs_to_model(jobs) :
    amazon_jobs: list[Job] = []

    for job in jobs :
        model_job = Job(company="Amazon", job=job["title"], apply_url=job["url_next_step"], job_hash="")

        job_text = model_job.company + model_job.job + model_job.apply_url

        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()

        model_job.job_hash = hash_dig

        amazon_jobs.append(model_job)

    return amazon_jobs

def get_amazon_jobs(params = params) :
    response = requests.get(url, params)
    data = response.json()
    jobs = data["jobs"]

    # software_jobs = [job for job in jobs if is_software_job(job)]
    wow_jobs = [job for job in jobs if is_fresher_job(job)]

    return parse_jobs_to_model(wow_jobs)

get_amazon_jobs()