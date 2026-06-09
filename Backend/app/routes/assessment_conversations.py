from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_question import (
    AssessmentQuestion
)

from app.schemas.assessment_conversation import (
    ConversationReply
)

from app.services.assessment_conversation_service import (
    save_message,
    get_next_question
)

from app.services.assessment_conversation_service import (
    get_transcript
)

from app.services.assessment_conversation_service import (
    save_message,
    get_next_question,
    get_next_sequence,
    get_transcript
)

router = APIRouter()


@router.get("/test")
def test():

    return {
        "message":
        "Assessment Conversation Ready"
    }

@router.get(
    "/start/{session_id}"
)
def start_assessment(
    session_id: int,
    db: Session = Depends(get_db)
):

    question = (

        db.query(
            AssessmentQuestion
        )

        .order_by(
            AssessmentQuestion.id
        )

        .first()
    )

    save_message(

        db=db,

        session_id=session_id,

        question_id=question.id,

        role="assistant",

        message=question.question,

        sequence_no=
        get_next_sequence(
            db,
            session_id
        )
    )

    return {

        "question_id":
        question.id,

        "question":
        question.question
    }

@router.post("/reply")
def reply(

    payload:
    ConversationReply,

    db: Session =
    Depends(get_db)
):

    save_message(

        db=db,

        session_id=
        payload.session_id,

        question_id=
        payload.question_id,

        role="user",

        message=
        payload.answer,

        sequence_no=
        get_next_sequence(
            db,
            payload.session_id
        )
    )

    next_question = (
        get_next_question(
            db,
            payload.question_id
        )
    )

    if not next_question:

        return {

            "completed":
            True
        }

    save_message(

        db=db,

        session_id=
        payload.session_id,

        question_id=
        next_question.id,

        role="assistant",

        message=
        next_question.question,

        sequence_no=
        get_next_sequence(
            db,
            payload.session_id
        )
    )

    return {

        "completed":
        False,

        "question_id":
        next_question.id,

        "question":
        next_question.question
    }

@router.get("/{session_id}")
def transcript(
    session_id: int,
    db: Session = Depends(get_db)
):

    return get_transcript(
        db,
        session_id
    )