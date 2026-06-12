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

Important Rules:

1. Ask only one question at a time.
2. Never recommend a course until ALL of the following are known:
   - Education
   - Experience
   - BIM Familiarity
   - Career Goal
3. Do not ask for enrollment before the BIM Readiness Assessment.
4. Recommend the BIM Readiness Assessment before enrollment.
5. Do not repeat greetings.
6. Use the Vtrios training methodology and knowledge base.

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
    lead = get_lead_by_phone(
        db,
        phone
    )

    if not message:

        return {
            "status": "empty message"
        }

    restart_words = [
        "start again",
        "start from beginning",
        "start from the beginning",
        "begin again",
        "restart",
        "reset",
        "start over",
        "new conversation",
        "lets start again",
        "let's start again",
        "lets start from beginning",
        "let's start from beginning"
    ]

    if any(
        word in message.lower()
        for word in restart_words
    ):

        if lead:

            session = get_active_session(
                db,
                lead.id
            )

            if session:
                session.status = "Completed"
                db.commit()

            create_session(
                db,
                lead.id
            )

        else:

            lead = create_lead(
                db=db,
                name=payload.get(
                    "senderName",
                    "WhatsApp Lead"
                ),
                phone=phone,
                source="WhatsApp"
            )

            create_session(
                db,
                lead.id
            )

        send_text_message(
            phone=phone,
            message=(
                "Welcome to Vtrios!\n\n"
                "I'm your BIM Career Counselor.\n\n"
                "Our training focuses on real BIM project workflows, documentation, coordination and industry-ready skills.\n\n"
                "Could you tell me about your educational background?"
            )
        )

        return {
            "status": "restarted"
        }

    
    print("=" * 80)

    print(
        "MESSAGE ID =",
        payload.get(
            "whatsappMessageId"
        )
    )

    message_id = payload.get(
        "whatsappMessageId"
    )

    print(
        "WHATSAPP MESSAGE ID =",
        message_id
    )

    print(
        "PHONE =",
        phone
    )

    print(
        "MESSAGE =",
        message
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

        create_session(
            db,
            lead.id
        )

        send_text_message(
            phone=phone,
            message=(
                "Welcome to Vtrios!\n\n"
                "We help students build job-ready BIM skills through real project-based training.\n\n"
                "What is your educational background?"
            )
        )

        return {
            "status": "new lead welcomed"
        }

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

    if session:

        print(
            "SESSION ID =",
            session.id
        )

        print(
            "CURRENT STAGE =",
            session.current_stage
        )

    else:

        print(
            "NO ACTIVE SESSION"
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

    if (
        message.strip().upper() == "YES"
        and
        session
        and
        session.current_stage == "ASSESSMENT"
    ):

        send_text_message(
            phone=phone,
            message=(
                "Welcome to Vtrios!\n\n"
                "We help students build job-ready BIM skills through real project-based training led by an industry BIM expert with 20+ years of experience.\n\n"
                "To help you choose the right BIM learning path, what is your educational background?"
            )
        )

        return {
            "status": "assessment started"
        }

    print("PHONE =", phone)
    print("MESSAGE =", message)
  
    stage = (
        session.current_stage
        if session.current_stage
        else "GREETING"
    )

    print(
        "CURRENT STAGE =",
        stage
    )

    if (
        session.current_stage != "GREETING"
        and
        message.lower().strip()
        in ["hi", "hello", "hey"]
    ):
        send_text_message(
            phone=phone,
            message=(
                "We are currently in the BIM Readiness Assessment process.\n\n"
                "Please continue with your previous response or type 'restart' to begin again."
            )
        )

        return {
            "status": "greeting handled"
        }

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

    print(
        "MESSAGE COUNT =",
        len(history)
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

    result = send_text_message(
        phone=phone,
        message=ai_reply
    )
    print("WATI RESPONSE =", result)

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

    qualification_complete = all([
        education
        and education != "Unknown",

        experience
        and experience != "Unknown",

        bim_familiarity
        and bim_familiarity != "Unknown",

        career_goal
        and career_goal != "Unknown"
    ])

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

    if (
        qualification_complete
        and
        session.current_stage != "ASSESSMENT"
    ):
        update_profile(
            db,
            session.id,
            current_stage="ASSESSMENT"
        )

        session = get_active_session(
            db,
            lead.id
        )

        print(
            "MOVING TO ASSESSMENT"
        )

        print(
            "CURRENT STAGE =",
            session.current_stage
        )

        send_text_message(
            phone=phone,
            message=(
                "Based on your background, I recommend "
                "the BIM Readiness Assessment.\n\n"
                "This assessment will identify the most "
                "suitable BIM learning path for you.\n\n"
                "Reply YES to begin."
            )
        )

        return {
            "status": "awaiting_assessment_confirmation"
        }