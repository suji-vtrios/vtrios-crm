from app.models.assessment_conversation import (
    AssessmentConversation
)

from app.models.assessment_session import (
    AssessmentSession
)

from openai import OpenAI
from app.config import settings


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


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

def generate_recommendation(
    average_score,
    transcript
):

    prompt = f"""
Assessment Score:
{average_score}

Assessment Responses:
{transcript}

Recommend ONLY ONE course:

- BIM Foundation
- BIM Architecture Professional
- BIM Architecture Advanced
- BIM Coordinator
- BIM Automation with Python
- BIM Manager Track

Return ONLY JSON:

{{
    "recommendation": "",
    "reason": ""
}}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )

def generate_report(
    db,
    session_id
):

    session = (
        db.query(
            AssessmentSession
        )
        .filter(
            AssessmentSession.id
            == session_id
        )
        .first()
    )

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
        .all()
    )

    return {

        "session_id":
        session.id,

        "overall_score":
        session.overall_score,

        "recommendation":
        session.recommendation,

        "questions_answered":
        len(answers),

        "answers": [

            {
                "question_id":
                a.question_id,

                "score":
                a.score,

                "feedback":
                a.feedback,

                "strengths":
                a.strengths,

                "weaknesses":
                a.weaknesses
            }

            for a in answers
        ]
    }