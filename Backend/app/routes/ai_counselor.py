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
    get_messages,
    get_session,
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
You are Vtrios AI Counselor.

{KNOWLEDGE}
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

    stage = session.current_stage

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

    transcript = "\n".join(

        [
            f"{item.role}: {item.message}"

            for item in history
        ]
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

    save_message(
        db,
        session.id,
        "assistant",
        ai_reply
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
    education = profile.get("education")
    experience = profile.get("experience")
    career_goal = profile.get("career_goal")
    bim_familiarity = profile.get("bim_familiarity")

    if (
        education
        and education != "Unknown"
        and
        experience
        and experience != "Unknown"
        and
        career_goal
        and career_goal != "Unknown"
        and
        bim_familiarity
        and bim_familiarity != "Unknown"
    ):

        update_profile(
            db,
            session.id,
            current_stage="ASSESSMENT"
        )

        ai_reply = (
            "START_ASSESSMENT\n\n"
            "Based on your background, "
            "the BIM Readiness Assessment "
            "will help identify the most "
            "suitable learning path. "
            "Shall we begin?"
        )

    update_profile(

        db,

        session.id,

        education=
        profile.get(
            "education"
        ),

        experience=
        profile.get(
            "experience"
        ),

        bim_familiarity=
        profile.get(
            "bim_familiarity"
        ),

        career_goal=
        profile.get(
            "career_goal"
        ),

        lead_quality=
        profile.get(
            "lead_quality"
        ),

        lead_intent=
        profile.get(
            "lead_intent"
        )
    )

    return {
        "session_id": session.id,
        "message": ai_reply
    }

@router.get("/session/{session_id}")
def get_counselor_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = get_session(
        db,
        session_id
    )

    if not session:

        return {
            "error":
            "Session not found"
        }

    return {

        "session_id":
        session.id,

        "lead_id":
        session.lead_id,

        "lead_quality":
        session.lead_quality,

        "lead_intent":
        session.lead_intent,

        "education":
        session.education,

        "experience":
        session.experience,

        "bim_familiarity":
        session.bim_familiarity,

        "career_goal":
        session.career_goal,

        "current_stage":
        session.current_stage,

        "assessment_score":
        session.assessment_score,

        "assessment_completed":
        session.assessment_completed,

        "recommended_course":
        session.recommended_course,

        "next_action":
        session.next_action,

        "objection_type":
        session.objection_type,

        "enrollment_probability":
        session.enrollment_probability,

        "status":
        session.status
    }