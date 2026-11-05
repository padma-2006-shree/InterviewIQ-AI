from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class DashboardMetrics(BaseModel):
    total_skills_detected: int = 0
    ats_score: float = 0.0
    matched_skills_count: int = 0
    missing_skills_count: int = 0


@router.get("/overview")
def get_dashboard_overview():
    """Returns general system status and analytics capabilities."""
    return {
        "status": "active",
        "modules": [
            "Resume Parsing (PDF/DOCX)",
            "ATS Scoring Engine",
            "Skill Gap Analysis",
            "AI Interview Practice",
            "Answer Evaluation",
            "HR Report Generation",
            "Personalized Learning Roadmap"
        ],
        "version": "1.0.0"
    }
