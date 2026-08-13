from pydantic import BaseModel
from typing import Optional

class Job(BaseModel) :
    company: str
    job: str
    apply_url: Optional[str]
    job_hash: str
    