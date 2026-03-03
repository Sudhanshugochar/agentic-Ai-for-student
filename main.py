import logging
import sys
from dotenv import load_dotenv

# Load env variables first before importing modules that need them
load_dotenv()

from database import engine, SessionLocal, Base
from models import Job
from scraper import fetch_jobs_from_serpapi
from email_service import send_job_alerts

# Configure explicit logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI Job Alert Agent...")

    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        jobs_data = fetch_jobs_from_serpapi()
        
        if not jobs_data:
            logger.info("No jobs fetched from SerpAPI. Exiting.")
            return

        new_jobs_found = []

        for job_data in jobs_data:
            # Check if job already exists in PostgreSQL to prevent duplicates
            existing_job = db.query(Job).filter(Job.job_id == job_data["job_id"]).first()
            
            if not existing_job:
                # Add new job to database
                db_job = Job(**job_data)
                db.add(db_job)
                new_jobs_found.append(job_data)
        
        if new_jobs_found:
            db.commit() # Commit all new jobs to DB
            logger.info(f"Found and saved {len(new_jobs_found)} new jobs.")
            # Send Email
            send_job_alerts(new_jobs_found)
            
            # Optionally mark as notified if email was successful
            for job_data in new_jobs_found:
                db_updated = db.query(Job).filter(Job.job_id == job_data["job_id"]).first()
                if db_updated:
                     db_updated.notified = True
            db.commit()
            
        else:
            logger.info("No new jobs found. Skipping email.")
            
    except Exception as e:
        logger.error(f"Error in main orchestration: {e}")
        db.rollback()
    finally:
        db.close()
        logger.info("Hourly job finished.")

if __name__ == "__main__":
    main()
