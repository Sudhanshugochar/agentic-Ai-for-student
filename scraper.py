import os
import requests
import time
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

QUERIES = [
    {"query": "Data Scientist entry level jobs in India remote", "category": "Data Science"},
    {"query": "Web Developer fresher jobs in India remote", "category": "Web Development"},
    {"query": "Data Analyst 0-2 years jobs in India remote", "category": "Data Analytics"},
    {"query": "Frontend Developer fresher jobs in India remote", "category": "Frontend Development"},
    {"query": "AI Engineer entry level jobs in India remote", "category": "AI Engineering"}
]

def fetch_jobs_from_serpapi() -> List[Dict]:
    """
    Fetches jobs from Google Jobs via SerpAPI using the predefined queries.
    Returns a list of parsed job dictionaries.
    """
    if not SERPAPI_KEY:
        logger.error("SERPAPI_KEY is not set. Cannot fetch jobs.")
        return []

    all_jobs = []
    
    for item in QUERIES:
        query = item["query"]
        category = item["category"]
        
        logger.info(f"Fetching jobs for query: '{query}'")
        
        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": SERPAPI_KEY,
            "hl": "en",
            "gl": "in",  # Google location: India
            "chips": "date_posted:today" # Only jobs posted within last 24 hours
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            jobs_results = data.get("jobs_results", [])
            logger.info(f"Found {len(jobs_results)} results for query: '{query}'")
            
            for job in jobs_results:
                parsed_job = {
                    "job_id": job.get("job_id", ""),
                    "title": job.get("title", "Unknown Title"),
                    "company": job.get("company_name", "Unknown Company"),
                    "category": category,
                    "location": job.get("location", "Unknown Location"),
                    "posted_date": job.get("detected_extensions", {}).get("posted_at", "Unknown"),
                    "apply_link": job.get("related_links", [{}])[0].get("link", "")
                }
                # Some jobs might have multiple apply links, taking the first or falling back to empty.
                if not parsed_job["apply_link"]:
                     # Alternatively, try providing a generic google search if no link attached
                     parsed_job["apply_link"] = job.get("share_link", "Google Jobs Link not available")
                     
                all_jobs.append(parsed_job)
                
            # API Rate Protection: Add a small delay between queries to avoid hitting SerpAPI limit
            logger.info("Sleeping for 3 seconds to respect API rate limits...")
            time.sleep(3)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch jobs for '{query}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching '{query}': {e}")
            
    return all_jobs
