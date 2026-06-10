from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_report import (
    AssessmentReport
)

from app.services.assessment_report_service import (
    calculate_session_score,
    generate_recommendation,
    generate_report
)

router = APIRouter()
print("ASSESSMENT REPORT ROUTES LOADED")


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

@router.get("/{session_id}")
def get_report_by_session(
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

@router.get("/test-score/{session_id}")
def test_score(
    session_id: int,
    db: Session = Depends(get_db)
):

    average_score = calculate_session_score(
        db,
        session_id
    )

    recommendation = generate_recommendation(
        average_score
    )

    return {

        "average_score":
        average_score,

        "recommendation":
        recommendation
    }

@router.get("/summary/{session_id}")
def summary(
    session_id: int,
    db: Session = Depends(get_db)
):

    return generate_report(
        db,
        session_id
    )