from app.models.assessment_session import (
    AssessmentSession
)


def update_session_progress(
    db,
    session_id,
    question_id,
    status
):

    session = (

        db.query(
            AssessmentSession
        )

        .filter(
            AssessmentSession.id
            == session_id
        )

        .first()
    )

    if not session:
        return None

    session.current_question_id = (
        question_id
    )

    session.assessment_status = (
        status
    )

    db.commit()

    db.refresh(session)

    return session

def get_active_session(
    db,
    lead_id
):

    return (

        db.query(
            AssessmentSession
        )

        .filter(
            AssessmentSession.lead_id
            == lead_id
        )

        .filter(
            AssessmentSession
            .assessment_status
            != "Completed"
        )

        .first()
    )