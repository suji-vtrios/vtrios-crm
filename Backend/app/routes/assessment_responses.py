from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_response import (
    AssessmentResponse as AssessmentResponseModel
)

from app.schemas.assessment_response import (
    AssessmentResponseCreate
)

router = APIRouter()


@router.get("/")
def get_responses(
    db: Session = Depends(get_db)
):

    return db.query(
        AssessmentResponseModel
    ).all()


@router.post("/")
def create_response(
    response: AssessmentResponseCreate,
    db: Session = Depends(get_db)
):

    new_response = (
        AssessmentResponseModel(
            **response.model_dump()
        )
    )

    db.add(new_response)

    db.commit()

    db.refresh(new_response)

    return new_response