from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_session import (
    AssessmentSession
)

from app.models.assessment_response import (
    AssessmentResponse
)

from app.models.assessment_question import (
    AssessmentQuestion
)
from app.models.assessment_report import (
    AssessmentReport
)

router = APIRouter()


@router.post("/{session_id}")
def evaluate_assessment(
    session_id: int,
    db: Session = Depends(get_db)
):

    responses = (
        db.query(
            AssessmentResponse
        )
        .filter(
            AssessmentResponse
            .session_id == session_id
        )
        .all()
    )

    total_score = 0

    for response in responses:

        answer = (
            response.response or ''
        ).lower()

        question = (
            db.query(
                AssessmentQuestion
            )
            .filter(
                AssessmentQuestion.id
                ==
                response.question_id
            )
            .first()
        )

        keywords = (
            question.expected_keywords
            or ''
        )

        score = 0

        for keyword in (
            keywords.split(',')
        ):

            keyword = (
                keyword
                .strip()
                .lower()
            )

            if (
                keyword
                and
                keyword in answer
            ):
                score += 10

        response.score = score

        total_score += score

    session = (
        db.query(
            AssessmentSession
        )
        .filter(
            AssessmentSession.id
            ==
            session_id
        )
        .first()
    )

    session.overall_score = (
        total_score
    )

    if total_score < 50:

        recommendation = (
            "BIM Fundamentals"
        )

    elif total_score < 100:

        recommendation = (
            "BIM Professional"
        )

    else:

        recommendation = (
            "Advanced BIM Professional"
        )

    session.recommendation = (
        recommendation
    )

    session.status = (
        "Completed"
    )

    existing_report = (
        db.query(
            AssessmentReport
        )
        .filter(
            AssessmentReport.session_id
            == session_id
        )
        .first()
    )

    if not existing_report:

        report = AssessmentReport(

            session_id=session_id,

            overall_score=total_score,

            strengths=
            "Basic BIM Knowledge",

            weaknesses=
            "Needs Further Assessment",

            recommendation=
            recommendation,

            gpt_feedback=
            "Rule based evaluation"
        )

        db.add(report)

    db.commit()

    return {

        "score":
        total_score,

        "recommendation":
        recommendation
    }

@router.get("/{session_id}")
def get_result(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(
            AssessmentSession
        )
        .filter(
            AssessmentSession.id
            ==
            session_id
        )
        .first()
    )

    return {

        "session_id":
        session.id,

        "score":
        session.overall_score,

        "recommendation":
        session.recommendation,

        "status":
        session.status
    }