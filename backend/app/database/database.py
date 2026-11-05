import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# On Vercel serverless functions, the root filesystem is read-only; use /tmp for SQLite
if os.getenv("VERCEL"):
    default_db_url = "sqlite:////tmp/interviewiq.db"
else:
    default_db_url = "sqlite:///./interviewiq.db"

DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
