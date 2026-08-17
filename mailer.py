import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import Job
from amazon import get_amazon_jobs
from greenhouse import get_greenhouse_jobs

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "aditheprince120@gmail.com"
SENDER_APP_PASS = os.environ.get("APP_PASS")

RECIPIENT_MAILS = ["devanshutripathi2005@gmail.com"]

def get_all_jobs() :
    all_jobs: list[Job] = []

    for j in get_amazon_jobs() :
        all_jobs.append(j)

    for j in get_greenhouse_jobs() :
        all_jobs.append(j)

    return all_jobs

def send_jobless_people_hope():

    hope_for_nalle_people = get_all_jobs()

    formatted_jobs = "\n\n".join(
        f"Company: {job.company}\nRole: {job.job}\nApply Link: {job.apply_url}"
        for job in hope_for_nalle_people
    )

    for unemployed in RECIPIENT_MAILS :


        message = MIMEMultipart()

        message["From"] = SENDER_EMAIL
        message["To"] = unemployed
        message["Subject"] = "Hope!!!"

        body = ";-; No Jobs for today, Sorry!!"

        # body = "Aaj omlette nahi tehelka omlette banaunga!"
        if formatted_jobs :
            body = f"MAUJ KAR AB \n\n{formatted_jobs}"

        message.attach(MIMEText(body, "plain"))

        try :
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            
            server.starttls() 
            
            server.login(SENDER_EMAIL, SENDER_APP_PASS)
            
            server.send_message(message)
            print(f"Email sent successfully to {unemployed}!")

        except Exception as e :
            print(f"An error occured: {e}")

        finally :
            server.quit()

if __name__ == "__main__" :
    send_jobless_people_hope()

