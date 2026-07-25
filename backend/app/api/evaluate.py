from fastapi import APIRouter
from pydantic import BaseModel
from app.services.evaluate_service import evaluate_answer

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])

class AnswerRequest(BaseModel):
    question: str
    answer: str

@router.post("/")
def evaluate(data: AnswerRequest):
    result = evaluate_answer(
        data.question,
        data.answer
    )

    return {
        "evaluation": result
    }