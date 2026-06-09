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

router = APIRouter()


@router.post("/webhook")
async def webhook(
    payload: dict,
    db: Session = Depends(get_db)
):

    phone = payload.get("phone")

    print("PHONE =", phone)

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

    return {

        "lead_id":
        lead.id,

        "session_id":
        session.id,

        "current_question_id":
        session.current_question_id,

        "assessment_status":
        session.assessment_status
    }