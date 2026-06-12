from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from sqlalchemy.orm import Session

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
    update_profile
)


router = APIRouter()


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

            session = create_session(
                db,
                lead.id
            )

            update_profile(
                db,
                session.id,
                current_stage="EDUCATION"
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

            session = create_session(
                db,
                lead.id
            )

            update_profile(
                db,
                session.id,
                current_stage="EDUCATION"
            )

        send_text_message(
            phone=phone,
            message=(
                "Welcome to Vtrios!\n\n"
                "We help students become industry-ready BIM professionals through:\n"
                "• Real project-based training\n"
                "• BIM documentation workflows\n"
                "• Coordination and clash detection\n"
                "• Portfolio development\n"
                "• Mentoring from Suji Sugathan, Senior BIM Manager with 20+ years of industry experience\n\n"
                "To recommend the most suitable BIM learning path, what is your educational background?"
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

        session = create_session(
            db,
            lead.id
        )

        update_profile(
            db,
            session.id,
            current_stage="EDUCATION"
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

        
    session = get_active_session(
        db,
        lead.id
    )

    if not session:

        session = create_session(
            db,
            lead.id
        )

        update_profile(
            db,
            session.id,
            current_stage="EDUCATION"
        )

    stage = (
        session.current_stage
        if session.current_stage
        else "GREETING"
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


    if (
        message.strip().upper() == "YES"
        and
        session
        and
        session.current_stage == "ASSESSMENT"
    ):

        update_profile(
            db,
            session.id,
            current_stage="ASSESSMENT_IN_PROGRESS"
        )

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
        stage != "EDUCATION"
        and
        message.lower().strip() in [
            "hi",
            "hello",
            "hey"
        ]
    ):
        return {
            "status": "ignored greeting"
        }

    save_message(
        db,
        session.id,
        "user",
        message
    )

       
    if stage == "EDUCATION":

        update_profile(
            db,
            session.id,
            education=message,
            current_stage="EXPERIENCE"
        )

        send_text_message(
            phone=phone,
            message=(
                "How many years of industry experience do you have?"
            )
        )

        return {"status": "ok"}
    
    if stage == "EXPERIENCE":

        update_profile(
            db,
            session.id,
            experience=message,
            current_stage="BIM_FAMILIARITY"
        )

        send_text_message(
            phone=phone,
            message=(
                "What is your BIM/Revit experience level?\n\n"
                "Beginner, Intermediate or Advanced?"
            )
        )

        return {"status": "ok"}
    
    if stage == "BIM_FAMILIARITY":

        update_profile(
            db,
            session.id,
            bim_familiarity=message,
            current_stage="CAREER_GOAL"
        )

        send_text_message(
            phone=phone,
            message=(
                "What is your career goal in BIM?"
            )
        )

        return {"status": "ok"}
    
    if stage == "CAREER_GOAL":

        update_profile(
            db,
            session.id,
            career_goal=message,
            current_stage="ASSESSMENT"
        )

        send_text_message(
            phone=phone,
            message=(
                "Thank you.\n\n"
                "Based on your profile, I recommend taking our "
                "BIM Readiness Assessment.\n\n"
                "Reply YES to begin."
            )
        )

        return {"status": "ok"}


 
  