from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from sqlalchemy.orm import Session

from openai import OpenAI

from app.config import settings
from app.dependencies import get_db

from app.services.lead_service import (
    get_lead_by_phone
)

from app.services.wati_service import (
    send_text_message
)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

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

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are Vtrios AI BIM Counselor. "
                    "Ask one question at a time "
                    "to understand the student's background."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    ai_reply = (
        response
        .choices[0]
        .message
        .content
    )

    print("AI REPLY =", ai_reply)

    send_text_message(
        phone=phone,
        message=ai_reply
    )

    return {
        "status": "ok"
    }