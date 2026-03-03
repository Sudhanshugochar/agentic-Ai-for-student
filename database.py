from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Provide a fallback for local testing without DB if needed, though the prompt requires Postgres
if not DATABASE_URL:
    # Use sqlite for local fallback if DATABASE_URL is not set, just to avoid crashing outright during initial tests.
    DATABASE_URL = "sqlite:///local_jobs.db"

# Render uses postgres:// in old configs, but SQLAlchemy 1.4+ requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
