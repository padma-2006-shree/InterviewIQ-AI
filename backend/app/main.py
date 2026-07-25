from app.api.interview import router as interview_router
from fastapi import FastAPI
from app.api.ats import router as ats_router
from app.database.database import Base, engine
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.evaluate import router as evaluate_router
from app.api.report import router as report_router
# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="InterviewIQ AI",
    description="AI-Powered Resume Analyzer & Interview Assistant",
    version="1.0.0"
)

# Register API Routers
app.include_router(report_router)
app.include_router(evaluate_router)
app.include_router(interview_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ats_router)
# Home Route
@app.get("/")
def home():
    return {
        "message": "InterviewIQ AI Backend Running 🚀"
    }

# Health Check Route
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "InterviewIQ AI"
    }