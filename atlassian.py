from playwright.sync_api import sync_playwright
from utils import is_global_fresher_job
from models import Job
from typing import List
import hashlib

def is_fresher_job(job) :
    title = job.get('title') or ""
    return is_global_fresher_job(title, "")
    
def parse_jobs_to_model(jobs) :
    atl_jobs: List[Job] = []
    
    for job in jobs :
        model_job = Job(company="Atlassian", job=job.get("title"), apply_url=job.get("url"), job_hash="")
        
        job_text = model_job.company + model_job.job + model_job.apply_url
        
        hash_object = hashlib.sha256(job_text.encode())
        hash_dig = hash_object.hexdigest()
        
        model_job.job_hash = hash_dig
        
        atl_jobs.append(model_job)
        
    print("ATLASSIAN JOBS DONE")
    return atl_jobs

def get_atlassian_jobs(team="Engineering", location="India", search=""):
    url = f"https://www.atlassian.com/company/careers/all-jobs?team={team}&location={location}&search={search}"
    atl_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url, wait_until="networkidle")
        
        page.wait_for_selector("table tbody tr")
        
        jobs = []
        rows = page.query_selector_all("table tbody tr")
        
        for row in rows:
            cols = row.query_selector_all("td")
            if len(cols) >= 2:
                title_elem = cols[0].query_selector("a")
                title = title_elem.inner_text().strip() if title_elem else cols[0].inner_text().strip()
                link = title_elem.get_attribute("href") if title_elem else None
                loc = cols[1].inner_text().strip()
                
                if link and link.startswith("/"):
                    link = f"https://www.atlassian.com{link}"
                    
                jobs.append({"title": title, "location": loc, "url": link})
                
        browser.close()
        for job in jobs :
            if is_fresher_job(job) :
                atl_jobs.append(job)
        return parse_jobs_to_model(atl_jobs)
