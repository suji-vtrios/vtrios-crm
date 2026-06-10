from app.models.assessment_conversation import (
    AssessmentConversation
)


def calculate_session_score(
    db,
    session_id
):

    answers = (

        db.query(
            AssessmentConversation
        )

        .filter(
            AssessmentConversation.session_id
            == session_id
        )

        .filter(
            AssessmentConversation.role
            == "user"
        )

        .filter(
            AssessmentConversation.score
            != None
        )

        .all()
    )

    if not answers:
        return 0

    total = sum(
        a.score
        for a in answers
    )

    return round(
        total / len(answers),
        2
    )


def generate_recommendation(
    average_score
):

    if average_score < 4:

        return "BIM Foundation"

    elif average_score < 7:

        return "Intermediate BIM"

    return "Advanced BIM"