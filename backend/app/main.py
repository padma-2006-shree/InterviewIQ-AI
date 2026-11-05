from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.models.user import User  # Ensures user table is registered
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.interview import router as interview_router
from app.api.evaluate import router as evaluate_router
from app.api.report import router as report_router
from app.api.roadmap import router as roadmap_router
from app.api.dashboard import router as dashboard_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI Application
app = FastAPI(
    title="InterviewIQ AI",
    description="AI-Powered Resume Analyzer, ATS Scorer & Interview Preparation Platform",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(interview_router)
app.include_router(evaluate_router)
app.include_router(report_router)
app.include_router(roadmap_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "InterviewIQ AI Backend Running 🚀",
        "status": "online",
        "docs_url": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "InterviewIQ AI"
    }
