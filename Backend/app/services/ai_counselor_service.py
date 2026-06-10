from app.models.ai_counselor_message import (
    AICounselorMessage
)

from app.models.ai_counselor_session import (
    AICounselorSession
)


def save_message(
    db,
    session_id,
    role,
    message
):

    item = AICounselorMessage(

        session_id=session_id,

        role=role,

        message=message
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item


def get_messages(
    db,
    session_id
):

    return (

        db.query(
            AICounselorMessage
        )

        .filter(
            AICounselorMessage
            .session_id
            == session_id
        )

        .order_by(
            AICounselorMessage.id
        )

        .all()
    )


def create_session(
    db,
    lead_id
):

    session = AICounselorSession(

        lead_id=lead_id,

        status="Active"
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def get_active_session(
    db,
    lead_id
):

    return (

        db.query(
            AICounselorSession
        )

        .filter(
            AICounselorSession.lead_id
            == lead_id
        )

        .filter(
            AICounselorSession.status
            == "Active"
        )

        .first()
    )