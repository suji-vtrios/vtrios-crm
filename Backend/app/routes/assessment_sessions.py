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

# ADD THESE IMPORTS
from app.models.lead import Lead
from app.models.student import Student
from datetime import datetime

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


# ADD THIS NEW ENDPOINT
@router.post("/{session_id}/enroll")
def enroll_student(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(
            AssessmentSessionModel
        )
        .filter(
            AssessmentSessionModel.id
            == session_id
        )
        .first()
    )

    if not session:

        return {
            "error":
            "Session not found"
        }

    lead = (
        db.query(
            Lead
        )
        .filter(
            Lead.id
            == session.lead_id
        )
        .first()
    )

    if not lead:

        return {
            "error":
            "Lead not found"
        }

    student = Student(

        name=lead.name,

        phone=lead.phone,

        email=lead.email,

        course=
        session.recommendation,

        enrollment_date=
        str(
            datetime.now()
            .date()
        ),

        status="Active"
    )

    db.add(student)

    db.commit()

    db.refresh(student)

    return student