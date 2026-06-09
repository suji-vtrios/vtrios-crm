from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.services.lead_service import (
    get_lead_by_phone
)

from app.services.assessment_session_service import (
    get_active_session
)

from app.services.assessment_question_service import (
    get_question_by_id
)

from app.schemas.wati_assessment import (
    WatiAssessmentMessage
)

from app.services.assessment_conversation_service import (
    save_message,
    get_next_question,
    get_next_sequence
)

from app.services.assessment_session_service import (
    get_active_session,
    update_session_progress
)

router = APIRouter()


@router.post("/webhook")
async def webhook(
    payload: WatiAssessmentMessage,
    db: Session = Depends(get_db)
):

    phone = payload.phone

    message = payload.message

    print("PHONE =", phone)

    print("MESSAGE =", message)

    lead = get_lead_by_phone(
        db,
        phone
    )

    print("LEAD =", lead)

    if lead:
        print("LEAD ID =", lead.id)

    if not lead:

        return {
            "status": "lead not found"
        }

    session = get_active_session(
        db,
        lead.id
    )

    print("SESSION =", session)

    if not session:

        return {
            "status": "session not found"
        }

    question = get_question_by_id(
        db,
        session.current_question_id
    )

    save_message(

        db=db,

        session_id=session.id,

        question_id=question.id,

        role="user",

        message=message,

        sequence_no=
        get_next_sequence(
            db,
            session.id
        )
    )

    next_question = get_next_question(
        db,
        question.id
    )

    if not next_question:

        update_session_progress(

            db=db,

            session_id=session.id,

            question_id=None,

            status="Completed"
        )

        return {

            "completed":
            True
        }

    update_session_progress(

        db=db,

        session_id=session.id,

        question_id=next_question.id,

        status="In Progress"
    )

    save_message(

        db=db,

        session_id=session.id,

        question_id=next_question.id,

        role="assistant",

        message=next_question.question,

        sequence_no=
        get_next_sequence(
            db,
            session.id
        )
    )

    return {

        "completed":
        False,

        "question_id":
        next_question.id,

        "question":
        next_question.question
    }