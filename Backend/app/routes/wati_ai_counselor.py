from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from sqlalchemy.orm import Session

from openai import OpenAI

from app.config import settings
from app.dependencies import get_db

from app.services.lead_service import (
    get_lead_by_phone,
    create_lead
)

from app.services.wati_service import (
    send_text_message
)

from app.services.ai_counselor_service import (
    get_active_session,
    create_session,
    save_message,
    get_messages,
    update_profile
)

from app.services.ai_counselor_profile_service import (
    extract_profile
)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

SYSTEM_PROMPT = """
You are the official Vtrios BIM Career Counselor.

Your primary objective is to qualify the lead quickly.

Collect only:

1. Education
2. Years of experience
3. BIM/Revit familiarity
4. Career objective

Rules:

- Ask only ONE short question at a time.
- Keep replies below 40 words.
- Avoid generic chatbot behaviour.
- Avoid repeating questions.
- Do not ask for information already provided.
- Maximum 4 qualification questions.

Once these are known:

- Education
- Experience
- BIM familiarity
- Career objective

When Education, Experience,
BIM Familiarity and Career Objective
are known, respond exactly:

START_ASSESSMENT

Do not ask any additional questions.
Do not ask for email.
Do not ask for contact information.
Do not continue normal conversation.
"""

@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    payload = await request.json()

    print("================================")
    print("WATI WEBHOOK RECEIVED")
    print(payload)
    print("================================")

    event_type = payload.get(
        "eventType"
    )

    if event_type != "message":

        return {
            "status": "ignored"
        }

    if payload.get("owner"):

        return {
            "status": "own message ignored"
        }

    phone = payload.get(
        "waId"
    )

    message = payload.get(
        "text"
    )

    if message.strip().upper() == "YES":

        send_text_message(
            phone=phone,
            message=(
                "Great! Let's begin the BIM Readiness Assessment.\n\n"
                "Question 1:\n"
                "What is BIM and how is it different from CAD?"
            )
        )

        return {
            "status": "assessment started"
        }

    print("PHONE =", phone)
    print("MESSAGE =", message)

    lead = get_lead_by_phone(
        db,
        phone
    )

    if not lead:

        lead = create_lead(
            db=db,
            name=payload.get(
                "senderName",
                "WhatsApp Lead"
            ),
            phone=phone,
            source="WhatsApp"
        )

        print(
            "NEW LEAD CREATED =",
            lead.id
        )

    session = get_active_session(
        db,
        lead.id
    )

    if not session:

        session = create_session(
            db,
            lead.id
        )

        print(
            "NEW SESSION CREATED =",
            session.id
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

    print("AI REPLY =", ai_reply)

    if "START_ASSESSMENT" in ai_reply:

        ai_reply = (
            "Based on your background, I recommend "
            "the BIM Readiness Assessment.\n\n"
            "This assessment will identify the most "
            "suitable BIM learning path for you.\n\n"
            "Reply YES to begin."
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

    history = get_messages(
        db,
        session.id
    )

    transcript = "\n".join(
        [
            f"{item.role}: {item.message}"
            for item in history
        ]
    )

    profile = extract_profile(
        transcript
    )

    print(
        "PROFILE =",
        profile
    )

    update_profile(
        db,
        session.id,
        education=profile.get(
            "education"
        ),
        experience=profile.get(
            "experience"
        ),
        career_goal=profile.get(
            "career_goal"
        ),
        lead_quality=profile.get(
            "lead_quality"
        ),
        lead_intent=profile.get(
            "lead_intent"
        )
    )

    return {
        "status": "ok"
    }