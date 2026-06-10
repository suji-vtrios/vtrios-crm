from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from openai import OpenAI

from app.config import settings
from app.dependencies import get_db

from app.services.ai_counselor_service import (
    get_active_session,
    create_session,
    save_message,
    get_messages
)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

SYSTEM_PROMPT = """
You are the Vtrios BIM Career Counselor.

Your goal is to collect:

1. Education
2. Experience
3. AutoCAD knowledge
4. Revit knowledge
5. BIM knowledge
6. Career goals

Ask only ONE question at a time.

Keep replies short.

Remember previous answers.
"""


@router.post("/chat")
def chat(
    payload: dict,
    db: Session = Depends(get_db)
):

    lead_id = payload.get(
        "lead_id",
        1
    )

    message = payload.get(
        "message"
    )

    session = get_active_session(
        db,
        lead_id
    )

    if not session:

        session = create_session(
            db,
            lead_id
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

    return {
        "session_id": session.id,
        "message": ai_reply
    }