from app.models.assessment_conversation import (
    AssessmentConversation
)

from app.models.assessment_question import (
    AssessmentQuestion
)


def save_message(
    db,
    session_id,
    question_id,
    role,
    message,
    sequence_no
):

    item = AssessmentConversation(

        session_id=session_id,

        question_id=question_id,

        role=role,

        message=message,

        sequence_no=sequence_no
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item


def get_transcript(
    db,
    session_id
):

    return (

        db.query(
            AssessmentConversation
        )

        .filter(
            AssessmentConversation
            .session_id
            == session_id
        )

        .order_by(
            AssessmentConversation
            .sequence_no
        )

        .all()
    )


def get_next_question(
    db,
    sequence_no
):

    return (

        db.query(
            AssessmentQuestion
        )

        .order_by(
            AssessmentQuestion.id
        )

        .offset(
            sequence_no
        )

        .first()
    )