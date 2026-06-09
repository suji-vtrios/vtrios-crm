from app.models.assessment_question import (
    AssessmentQuestion
)


def get_question_by_id(
    db,
    question_id
):

    return (

        db.query(
            AssessmentQuestion
        )

        .filter(
            AssessmentQuestion.id
            == question_id
        )

        .first()
    )