import hashlib
from typing import List
from playwright.sync_api import sync_playwright
from models import Job
from utils import is_global_fresher_job

BASE_URL = "https://www.google.com/about/careers/applications/jobs/results?location=India&target_level=EARLY&target_level=INTERN_AND_APPRENTICE&q=software"

def is_fresher_job(job):
    title = job.get("title") or ""
    return is_global_fresher_job(title, "")

def parse_jobs_to_model(jobs):
    ggl_jobs: List[Job] = []
    
    for job in jobs:
        model_job = Job(
            company="Google",
            job=job.get("title"),
            apply_url=job.get("url"),
            job_hash=""
        )
        
        job_text = model_job.company + model_job.job + (model_job.apply_url or "")
        hash_object = hashlib.sha256(job_text.encode())
        model_job.job_hash = hash_object.hexdigest()
        
        ggl_jobs.append(model_job)
        
    print("GOOGLE JOBS DONE")
    return ggl_jobs

def get_google_jobs():
    url = BASE_URL
    ggl_jobs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url, wait_until="networkidle")
        
        page.wait_for_selector("li.lLd3Je")
        
        cards = page.query_selector_all("li.lLd3Je")
        jobs = []
        
        for card in cards:
            title_elem = card.query_selector("h3")
            title = title_elem.inner_text().strip() if title_elem else ""
            
            link_elem = card.query_selector("a[href*='jobs/results']") or card.query_selector("a")
            link = link_elem.get_attribute("href") if link_elem else ""
            
            if link and link.startswith("/"):
                link = f"https://www.google.com/about/careers/applications{link}"
            elif link and not link.startswith("http"):
                link = f"https://www.google.com/about/careers/applications/jobs/results/{link}"
                
            if title:
                jobs.append({"title": title, "url": link})
                
        browser.close()
        
        for job in jobs:
            if is_fresher_job(job):
                ggl_jobs.append(job)
                
        return parse_jobs_to_model(ggl_jobs)