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
    bim_familiarity=None,
    career_goal=None,
    lead_quality=None,
    lead_intent=None,
    current_stage=None,
    recommended_course=None,
    assessment_score=None,
    assessment_completed=None,
    next_action=None,
    objection_type=None,
    enrollment_probability=None
):

    session = (
        db.query(
            AICounselorSession
        )
        .filter(
            AICounselorSession.id == session_id
        )
        .first()
    )

    if not session:
        return None

    if education is not None:
        session.education = education

    if experience is not None:
        session.experience = experience

    if bim_familiarity is not None:
        session.bim_familiarity = bim_familiarity

    if career_goal is not None:
        session.career_goal = career_goal

    if lead_quality is not None:
        session.lead_quality = lead_quality

    if lead_intent is not None:
        session.lead_intent = lead_intent

    if current_stage is not None:
        session.current_stage = current_stage

    if recommended_course is not None:
        session.recommended_course = recommended_course

    if assessment_score is not None:
        session.assessment_score = assessment_score

    if assessment_completed is not None:
        session.assessment_completed = assessment_completed

    if next_action is not None:
        session.next_action = next_action

    if objection_type is not None:
        session.objection_type = objection_type

    if enrollment_probability is not None:
        session.enrollment_probability = enrollment_probability

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