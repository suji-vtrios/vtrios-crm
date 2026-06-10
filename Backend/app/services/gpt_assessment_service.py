from openai import OpenAI
from app.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def evaluate_answer(
    question,
    answer
):

    prompt = f"""
Question:
{question}

Student Answer:
{answer}

Evaluate the answer.

Return JSON:

{{
  "score": 0-10,
  "feedback": "...",
  "strengths": "...",
  "weaknesses": "..."
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

    return response.choices[0].message.content