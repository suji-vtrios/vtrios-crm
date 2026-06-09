from openai import OpenAI

client = OpenAI()

def evaluate_answer(
    question: str,
    answer: str
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
 "feedback": "short feedback"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content