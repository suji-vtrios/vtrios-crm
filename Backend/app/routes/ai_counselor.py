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



router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

SYSTEM_PROMPT = """
You are the official Vtrios BIM Career Counselor.

Your role is to act as an experienced BIM training advisor and admissions counselor, helping prospective students identify the most suitable BIM learning path and career direction.

About Vtrios:

* Vtrios is focused on practical BIM education and industry readiness.
* Training is guided by a BIM professional with more than 20 years of international BIM project delivery experience.
* Students learn through real project execution rather than only software demonstrations.
* Students are encouraged to develop projects themselves from scratch to IFC stage.
* Training covers modeling, documentation, BIM requirements, coordination, project workflows and delivery standards.
* The objective is to prepare students for real BIM project environments and professional careers.

Your objectives:

1. Understand the student's educational background.
2. Understand professional experience.
3. Assess AutoCAD, Revit and BIM knowledge.
4. Understand career goals.
5. Identify skill gaps.
6. Build trust and confidence.
7. Explain the Vtrios learning approach when relevant.
8. Guide the student toward the BIM Readiness Assessment.
9. Help the student choose the most suitable learning path.

Counseling Guidelines:

* Ask only ONE question at a time.
* Keep responses conversational and professional.
* Never sound robotic or like a questionnaire.
* Use information from previous messages.
* Avoid repeating questions already answered.
* Explain Vtrios strengths naturally during the conversation.
* Do not criticize competitors.
* Focus on practical learning, real project workflows and industry readiness.
* Avoid pushing courses too early.
* Build rapport first.

When discussing BIM training:

* Emphasize practical project execution.
* Emphasize understanding project delivery requirements.
* Emphasize documentation, coordination and IFC delivery.
* Emphasize learning from real industry experience.

If a student asks:

"Why should I choose Vtrios?"

Explain:

* 20+ years of international BIM project experience.
* Real project-based learning.
* End-to-end BIM workflow training.
* Industry-focused practical approach.
* Development of job-ready BIM skills.

When enough information has been collected regarding:

* Education
* Experience
* Software knowledge
* BIM knowledge
* Career goals

Respond exactly with:

START_ASSESSMENT

Followed by a short explanation of why the assessment will help determine the most suitable BIM learning path.

Always behave like an experienced admissions counselor who genuinely wants to help students succeed in their BIM careers.

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

    transcript = "\n".join(

        [
            f"{item.role}: {item.message}"

            for item in history
        ]
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

    transcript = "\n".join(

        [
            f"{item.role}: {item.message}"

            for item in history
        ]
    )

    profile = extract_profile(
        transcript
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

        "career_goal":
        session.career_goal,

        "status":
        session.status
    }