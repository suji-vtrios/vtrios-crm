from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.services.lead_service import (
    get_lead_by_phone
)

from app.services.assessment_question_service import (
    get_question_by_id
)

from app.schemas.wati_assessment import (
    WatiAssessmentMessage
)

from app.services.assessment_conversation_service import (
    save_message,
    get_next_question,
    get_next_sequence
)

from app.services.wati_service import (
    send_text_message
)

from app.services.gpt_assessment_service import (
    evaluate_answer
)

from app.services.assessment_report_service import (
    calculate_session_score,
    generate_recommendation
)

from app.services.assessment_session_service import (
    get_active_session,
    update_session_progress,
    update_final_result
)
router = APIRouter()


@router.post("/webhook")
async def webhook(
    payload: WatiAssessmentMessage,
    db: Session = Depends(get_db)
):

    phone = payload.phone

    message = payload.message

    print("PHONE =", phone)

    print("MESSAGE =", message)

    lead = get_lead_by_phone(
        db,
        phone
    )

    print("LEAD =", lead)

    if lead:
        print("LEAD ID =", lead.id)

    if not lead:

        return {
            "status": "lead not found"
        }

    session = get_active_session(
        db,
        lead.id
    )

    print("SESSION =", session)

    if not session:

        return {
            "status": "session not found"
        }

    question = get_question_by_id(
        db,
        session.current_question_id
    )

    evaluation = evaluate_answer(

        question=question.question,

        answer=message
    )

    if not isinstance(evaluation, dict):

        evaluation = {

            "score": 0,

            "feedback":
            "Evaluation failed",

            "strengths": "",

            "weaknesses": ""
        }

    print("EVALUATION =", evaluation)

    save_message(

        db=db,

        session_id=session.id,

        question_id=question.id,

        role="user",

        message=message,

        sequence_no=
        get_next_sequence(
            db,
            session.id
        ),
        score=evaluation["score"],

        feedback=evaluation["feedback"],

        strengths=evaluation["strengths"],

        weaknesses=evaluation["weaknesses"]
    )

    next_question = get_next_question(
        db,
        question.id
    )

    if not next_question:

        average_score = (
            calculate_session_score(
                db,
                session.id
            )
        )

        recommendation = (
            generate_recommendation(
                average_score
            )
        )

        update_final_result(

            db=db,

            session_id=session.id,

            score=average_score,

            recommendation=recommendation
        )

        update_session_progress(

            db=db,

            session_id=session.id,

            question_id=None,

            status="Completed"
        )

        return {

            "completed":
            True,

            "average_score":
            average_score,

            "recommendation":
            recommendation
        }

    update_session_progress(

        db=db,

        session_id=session.id,

        question_id=next_question.id,

        status="In Progress"
    )

    save_message(

        db=db,

        session_id=session.id,

        question_id=next_question.id,

        role="assistant",

        message=next_question.question,

        sequence_no=
        get_next_sequence(
            db,
            session.id
        )
    )

    return {

        "completed": False,

        "question_id":
        next_question.id,

        "question":
        next_question.question,

        "score":
        evaluation["score"],

        "feedback":
        evaluation["feedback"]
    }

@router.get("/test-message")
def test_message():

    return send_text_message(

        phone="918891393010",

        message="Vtrios AI Assessment Test Message"
    )