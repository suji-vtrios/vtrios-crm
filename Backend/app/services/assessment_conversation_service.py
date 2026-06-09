from app.models.assessment_conversation import (
    AssessmentConversation
)

QUESTIONS = [

    "What is your educational background?",

    "Which BIM software have you used?",

    "Have you worked with Revit?",

    "Have you created Revit Families?",

    "Have you used Navisworks?",

    "Have you worked on live projects?",

    "Have you done clash detection?",

    "Have you used BIM 360 or ACC?",

    "What is your career goal?",

    "Why do you want to learn BIM?"
]


def save_message(
    db,
    session_id,
    role,
    message,
    question_number
):

    item = AssessmentConversation(

        session_id=session_id,

        role=role,

        message=message,

        question_number=
        question_number
    )

    db.add(item)

    db.commit()