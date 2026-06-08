from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_session import (
    AssessmentSession as AssessmentSessionModel
)

from app.schemas.assessment_session import (
    AssessmentSessionCreate
)

router = APIRouter()


@router.get("/")
def get_sessions(
    db: Session = Depends(get_db)
):

    return db.query(
        AssessmentSessionModel
    ).all()


@router.post("/")
def create_session(
    session: AssessmentSessionCreate,
    db: Session = Depends(get_db)
):

    new_session = (
        AssessmentSessionModel(
            **session.model_dump()
        )
    )

    db.add(new_session)

    db.commit()

    db.refresh(new_session)

    return new_session