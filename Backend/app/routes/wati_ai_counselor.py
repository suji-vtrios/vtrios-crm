from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from openai import OpenAI

from app.config import settings
from app.dependencies import get_db

from app.schemas.wati_assessment import (
    WatiAssessmentMessage
)

from app.services.lead_service import (
    get_lead_by_phone
)

from app.services.ai_counselor_service import (
    get_active_session,
    create_session,
    save_message,
    get_messages
)

from app.services.wati_service import (
    send_text_message
)

from app.routes.ai_counselor import (
    SYSTEM_PROMPT
)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


@router.post("/webhook")
async def webhook(
    payload: WatiAssessmentMessage,
    db: Session = Depends(get_db)
):

    phone = payload.phone
    message = payload.message

    lead = get_lead_by_phone(
        db,
        phone
    )

    if not lead:

        return {
            "status": "lead not found"
        }

    session = get_active_session(
        db,
        lead.id
    )

    if not session:

        session = create_session(
            db,
            lead.id
        )

    save_message(
        db,
        session.id,
        "user",
        message
    )

    history = get_messages(
        db,
        session.id
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for item in history:

        messages.append(
            {
                "role": item.role,
                "content": item.message
            }
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    ai_reply = (
        response
        .choices[0]
        .message
        .content
    )

    save_message(
        db,
        session.id,
        "assistant",
        ai_reply
    )

    send_text_message(
        phone=phone,
        message=ai_reply
    )

    return {
        "status": "ok"
    }