from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ats_scorer import calculate_ats_score

router = APIRouter(
    prefix="/ats",
    tags=["ATS"]
)


class ATSRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/score")
def score_resume(data: ATSRequest):

    return calculate_ats_score(
        data.resume_text,
        data.job_description
    )