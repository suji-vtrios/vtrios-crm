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

from app.services.knowledge_loader import (
    load_knowledge
)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

KNOWLEDGE = load_knowledge()

SYSTEM_PROMPT = f"""
You are the official Vtrios BIM Career Counselor.

{KNOWLEDGE}
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

        stage = session.current_stage

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
            "content": (
                SYSTEM_PROMPT
                +
                f"\n\nCurrent Counseling Stage: {stage}"
            )
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
    education = profile.get(
        "education"
    )

    experience = profile.get(
        "experience"
    )

    bim_familiarity = profile.get(
        "bim_familiarity"
    )

    career_goal = profile.get(
        "career_goal"
    )

    if (
        education
        and education != "Unknown"
        and
        experience
        and experience != "Unknown"
        and
        bim_familiarity
        and bim_familiarity != "Unknown"
        and
        career_goal
        and career_goal != "Unknown"
        and
        session.current_stage != "ASSESSMENT"
    ):
        update_profile(
            db,
            session.id,
            current_stage="ASSESSMENT"
        )

        print(
            "MOVING TO ASSESSMENT"
        )

        print(
            "PROFILE =",
            profile
        )

        print(
            "CURRENT STAGE =",
            session.current_stage
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

        bim_familiarity=profile.get(
            "bim_familiarity"
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