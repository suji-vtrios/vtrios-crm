from fastapi import APIRouter

from app.services.gpt_assessment_service import (
    evaluate_answer
)

router = APIRouter()


@router.get("/test")
def test():

    return evaluate_answer(

        question=
        "What is the purpose of a roof?",

        answer=
        "A roof protects a building from weather."
    )