import requests
from mailer import load_seen_hashes
from typing import List
from models import Job
from utils import create_model_job

def get_amazon_service_jobs() :
    amzs_jobs: List[Job] = []
    response = requests.get("https://amazon-jobs-service.onrender.com/api/v1/jobs")
    data = response.json()
    
    jobs = data.get("jobs")
    
    seen_jobs = load_seen_hashes()
    
    if jobs :
        for job in jobs :
            if job.get("job_hash") not in seen_jobs :
                model_job = create_model_job(job.get("company"), job.get("title"), job.get("apply_url"))
                
                amzs_jobs.append(model_job)
                
    print("AMAZON SERVICE JOBS DONE")
    return amzs_jobs