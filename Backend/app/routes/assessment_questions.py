from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_question import (
    AssessmentQuestion as AssessmentQuestionModel
)

from app.schemas.assessment_question import (
    AssessmentQuestionCreate
)

router = APIRouter()


@router.get("/")
def get_questions(
    db: Session = Depends(get_db)
):
    return db.query(
        AssessmentQuestionModel
    ).all()


@router.post("/")
def create_question(
    question: AssessmentQuestionCreate,
    db: Session = Depends(get_db)
):

    new_question = AssessmentQuestionModel(
        competency_id=question.competency_id,
        question=question.question,
        stream=question.stream,
        difficulty=question.difficulty,
        question_type=question.question_type,
        expected_keywords=question.expected_keywords,
        scoring_guidance=question.scoring_guidance,
        source=question.source,
        is_active=question.is_active
    )

    db.add(new_question)

    db.commit()

    db.refresh(new_question)

    return new_question


@router.put("/{id}")
def update_question(
    id: int,
    question: AssessmentQuestionCreate,
    db: Session = Depends(get_db)
):

    existing_question = db.query(
        AssessmentQuestionModel
    ).filter(
        AssessmentQuestionModel.id == id
    ).first()

    if not existing_question:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    existing_question.competency_id = question.competency_id
    existing_question.question = question.question
    existing_question.stream = question.stream
    existing_question.difficulty = question.difficulty
    existing_question.question_type = question.question_type
    existing_question.expected_keywords = question.expected_keywords
    existing_question.scoring_guidance = question.scoring_guidance
    existing_question.source = question.source
    existing_question.is_active = question.is_active

    db.commit()

    db.refresh(existing_question)

    return existing_question


@router.delete("/{id}")
def delete_question(
    id: int,
    db: Session = Depends(get_db)
):

    question = db.query(
        AssessmentQuestionModel
    ).filter(
        AssessmentQuestionModel.id == id
    ).first()

    if not question:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    db.delete(question)

    db.commit()

    return {
        "message": "Question deleted"
    }