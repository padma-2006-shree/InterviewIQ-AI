from fastapi import APIRouter
from pydantic import BaseModel
from app.services.report_service import generate_report

router = APIRouter(prefix="/report", tags=["Report"])

class ReportRequest(BaseModel):
    evaluation: str

@router.post("/")
def report(data: ReportRequest):
    result = generate_report(data.evaluation)
    return {
        "report": result
    }