from fastapi import APIRouter
from fastapi import Request

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.lead_service import get_lead_by_phone
from app.services.ai_counselor_service import (
    get_active_session,
    create_session,
    save_message,
    get_messages
)
from app.services.wati_service import send_text_message

router = APIRouter()


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    payload = await request.json()

    phone = payload.get("waId")
    message = payload.get("text")

    print("PHONE =", phone)
    print("MESSAGE =", message)

    lead = get_lead_by_phone(
        db,
        phone
    )

    print("LEAD =", lead)

    if not lead:

        return {
            "status": "lead not found"
        }

    send_text_message(
        phone=phone,
        message=f"I received: {message}"
    )

    return {
        "status": "ok"
    }