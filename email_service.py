import os
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_job_alerts(new_jobs: list):
    """
    Sends an email digest of new jobs. Only sends if there are new jobs.
    """
    if not new_jobs:
        logger.info("No new jobs to email.")
        return
        
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVER_EMAIL]):
        logger.error("Email credentials are not fully configured in environment variables.")
        return

    msg = EmailMessage()
    msg['Subject'] = "🚀 New Job Alerts - Hourly Update"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    body = "New Jobs Found:\n\n"
    
    for job in new_jobs:
        body += f"Category: {job['category']}\n"
        body += f"Title: {job['title']}\n"
        body += f"Company: {job['company']}\n"
        body += f"Location: {job['location']}\n"
        body += f"Posted: {job['posted_date']}\n"
        body += f"Apply Link: {job['apply_link']}\n"
        body += "-" * 40 + "\n\n"

    msg.set_content(body)

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            
        logger.info(f"Successfully sent email alert with {len(new_jobs)} jobs.")
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
