import json

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

Return ONLY valid JSON:

{{
  "score": 0,
  "feedback": "",
  "strengths": "",
  "weaknesses": ""
}}
"""

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        return json.loads(content)

    except Exception as e:

        return {

            "score": 0,

            "feedback":
            f"GPT Error: {str(e)}",

            "strengths": "",

            "weaknesses": ""
        }