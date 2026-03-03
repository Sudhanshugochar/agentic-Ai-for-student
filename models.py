from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)  # SerpAPI job_id
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    posted_date = Column(String, nullable=True) # Could be string like "10 hours ago"
    apply_link = Column(String, nullable=True)
    notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
