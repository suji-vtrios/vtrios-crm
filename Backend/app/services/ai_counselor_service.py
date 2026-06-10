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

def update_profile(
    db,
    session_id,
    education=None,
    experience=None,
    career_goal=None,
    lead_quality=None,
    lead_intent=None
):

    session = (
        db.query(
            AICounselorSession
        )
        .filter(
            AICounselorSession.id
            == session_id
        )
        .first()
    )

    if not session:
        return None

    if education:
        session.education = education

    if experience:
        session.experience = experience

    if career_goal:
        session.career_goal = career_goal

    if lead_quality:
        session.lead_quality = lead_quality

    if lead_intent:
        session.lead_intent = lead_intent

    db.commit()

    db.refresh(session)

    return session

def get_session(
    db,
    session_id
):

    return (

        db.query(
            AICounselorSession
        )

        .filter(
            AICounselorSession.id
            == session_id
        )

        .first()
    )