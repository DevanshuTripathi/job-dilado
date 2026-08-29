import re
from models import Job
import hashlib

SENIOR_TITLE_PATTERN = r"\b(senior|sr|lead|manager|head|principal|staff|director|vp|avp|executive|tl|sse|architect|ii|iii|iv|2|3|4|l5|l6)\b"
# EXPLICIT_SENIOR_EXP = r"\b([2-9]|\d{2})\s*(\+|\-|to)?\s*years?\b"
EXPLICIT_SENIOR_EXP = r"\b([2-9]|\d{2})(?:\s*[\-–+]\s*\d+)?\+?\s*years?\b(?:\s+of)?(?:\s+[\w\-]+){0,7}\s+(?:exp|experience|working)\b"
ENTRY_PATTERN = r"\b(0|0-1|0-2)\s*(?:-\s*\d+)?\s*years?\b|\b(fresher|entry[- ]level|intern|internship|graduate|trainee|associate sde|sde[- ]?1|sde[- ]?i)\b"


EXPLICIT_SENIOR_EXP = re.compile(EXPLICIT_SENIOR_EXP, re.IGNORECASE | re.VERBOSE)
# ENTRY_EXP_PATTERN = r"\b(0|1)\s*(?:-\s*\d+)?\s*years?\b|\b(fresher|entry[- ]level|intern(?:ship)?)\b"

SOFTWARE_PATTERN = r"\b(software|sde|swe|backend|frontend|fullstack|full-stack|web developer|devops|sdet|qa engineer|data engineer|golang|python|java|react|node)\b"

LOCATION_PATTERN = r"\b(india|ind|bangalore|bengaluru|gurgaon|gurugram|hyderabad|noida|mumbai|pune|chennai|delhi)\b"


def safe_str(val):
    return str(val).lower() if val else ""


def is_global_fresher_job(title: str, description: str = "") -> bool:
    title_clean = safe_str(title)
    desc_clean = safe_str(description)
    full_text = f"{title_clean} {desc_clean}"

    if re.search(EXPLICIT_SENIOR_EXP, desc_clean):
        return False

    if re.search(SENIOR_TITLE_PATTERN, title_clean):
        return False

    if re.search(ENTRY_PATTERN, full_text):
        return True

    if re.search(SOFTWARE_PATTERN, title_clean) and not re.search(
        EXPLICIT_SENIOR_EXP, full_text
    ):
        return True

    return False


def is_global_software_job(context):
    return bool(re.search(SOFTWARE_PATTERN, safe_str(context)))

def is_global_india_job(context):
    return bool(re.search(LOCATION_PATTERN, safe_str(context)))

def create_model_job(company, job, apply_url) :
    model_job = Job(company=company, job=job, apply_url=apply_url, job_hash="")
    
    job_text = model_job.company + model_job.job + model_job.apply_url
            
    hash_object = hashlib.sha256(job_text.encode())
    hash_dig = hash_object.hexdigest()

    model_job.job_hash = hash_dig
    
    return model_job
