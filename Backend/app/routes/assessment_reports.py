from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_report import (
    AssessmentReport
)

router = APIRouter()


@router.get("/")
def get_reports(
    db: Session = Depends(get_db)
):

    return (
        db.query(
            AssessmentReport
        )
        .all()
    )


@router.get("/generate/{session_id}")
def get_report(
    session_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(
            AssessmentReport
        )
        .filter(
            AssessmentReport.session_id
            == session_id
        )
        .first()
    )