import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import Job
from amazon import get_amazon_jobs
from greenhouse import get_greenhouse_jobs
from lever import get_lever_jobs
from ashby import get_ashby_jobs
import json

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "aditheprince120@gmail.com"
SENDER_APP_PASS = os.environ.get("APP_PASS")

SEEN_JOBS_FILE = "seen_jobs.json"

RECIPIENT_MAILS = [
    "devanshutripathi2005@gmail.com",
    "sakshambajpai.1604@gmail.com",
    "manpuriadevdhar95@gmail.com",
    "tanishaagarwala2510@gmail.com",
    "saketruia18@gmail.com",
    "armaanitsingh6@gmail.com",
    "preetgupta0423@gmail.com",
    "adityamukherjee1972@gmail.com",
]


def load_seen_hashes():
    if os.path.exists(SEEN_JOBS_FILE):
        try:
            with open(SEEN_JOBS_FILE, "r") as f:
                data = json.load(f)
                return set(data)
        except Exception as e:
            print(f"Error reading {SEEN_JOBS_FILE}: {e}")
            return set()
    return set()

def save_seen_hashes(seen_hashes: set):
    try:
        with open(SEEN_JOBS_FILE, "w") as f:
            json.dump(list(seen_hashes), f, indent=4)
    except Exception as e:
        print(f"Error saving to {SEEN_JOBS_FILE}: {e}")


def get_all_jobs():
    all_jobs: list[Job] = []

    for j in get_amazon_jobs():
        all_jobs.append(j)

    for j in get_greenhouse_jobs():
        all_jobs.append(j)

    for j in get_lever_jobs():
        all_jobs.append(j)

    for j in get_ashby_jobs():
        all_jobs.append(j)

    print("ALL JOBS DONE")
    return all_jobs


def send_jobless_people_hope():

    seen_hashes = load_seen_hashes()
    hope_for_nalle_people = get_all_jobs()

    new_jobs = [
        job for job in hope_for_nalle_people 
        if hasattr(job, 'job_hash') and job.job_hash and job.job_hash not in seen_hashes
    ]

    if not new_jobs:
        print("No new jobs found since last run. Skipping email dispatch.")
        return {"message": "No new jobs."}

    formatted_jobs = "\n\n".join(
        f"Company: {job.company}\nRole: {job.job}\nApply Link: {job.apply_url}"
        for job in new_jobs
    )

    for unemployed in RECIPIENT_MAILS:

        message = MIMEMultipart()

        message["From"] = SENDER_EMAIL
        message["To"] = unemployed
        message["Subject"] = "Hope!!!"

        body = ";-; No Jobs for today, Sorry!!"

        # body = "Aaj omlette nahi tehelka omlette banaunga!"
        if formatted_jobs:
            body = f"Current Market Jobs: \n\n{formatted_jobs} \n\n The list will keep on growing"

        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

            server.starttls()

            server.login(SENDER_EMAIL, SENDER_APP_PASS)

            server.send_message(message)
            print(f"Email sent successfully to {unemployed}!")

        except Exception as e:
            print(f"An error occured: {e}")
            return {"error": e}

        finally:
            server.quit()
            
    for job in new_jobs:
        seen_hashes.add(job.job_hash)

    save_seen_hashes(seen_hashes)

    return {"message": "success!"}


if __name__ == "__main__":
    send_jobless_people_hope()
