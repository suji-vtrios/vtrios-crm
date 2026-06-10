import json

from openai import OpenAI

from app.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def extract_profile(
    transcript
):

    prompt = f"""
Conversation:

{transcript}

Extract:

1. Education
2. Experience
3. Career Goal
4. Lead Quality
5. Lead Intent

Return ONLY JSON:

{{
  "education":"",
  "experience":"",
  "career_goal":"",
  "lead_quality":"",
  "lead_intent":""
}}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return json.loads(
        response
        .choices[0]
        .message
        .content
    )