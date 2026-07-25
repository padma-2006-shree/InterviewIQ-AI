from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_interview_questions

router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


class SkillInput(BaseModel):
    skills: list[str]


@router.post("/questions")
def interview(data: SkillInput):

    questions = generate_interview_questions(data.skills)

    return {
        "questions": questions
    }