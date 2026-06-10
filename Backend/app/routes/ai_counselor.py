from fastapi import APIRouter

from openai import OpenAI

from app.config import settings

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


@router.post("/chat")
def chat(payload: dict):

    message = payload.get("message")

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content": """
You are the Vtrios AI BIM Counselor.

Your objectives:

1. Understand education.
2. Understand software knowledge.
3. Understand BIM knowledge.
4. Understand career goals.
5. Ask only ONE question at a time.
6. Keep responses short.
7. Do not recommend a course yet.
"""
            },

            {
                "role": "user",
                "content": message
            }
        ]
    )

    return {
        "message":
        response.choices[0].message.content
    }