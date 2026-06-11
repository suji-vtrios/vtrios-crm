import json

from openai import OpenAI

from app.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def extract_profile(
    transcript
):

    try:

        prompt = f"""
        Conversation:

        {transcript}

        Extract:

        1. Education
        2. Experience
        3. BIM Familiarity
        4. Career Goal
        5. Lead Quality
        6. Lead Intent

        Lead Quality Rules:

        HOT
        WARM
        COLD

        Lead Intent Options:

        Career Change
        Skill Upgrade
        Student Learning
        Job Preparation
        Exploration
        Unknown

        Return ONLY valid JSON.

        Do not include markdown.
        Do not include explanations.
        Do not include code fences.
        If information is not available,
        return "Unknown".

        Example:

        {{
        "education":"",
        "experience":"",
        "bim_familiarity":"",
        "career_goal":"",
        "lead_quality":"",
        "lead_intent":""
        }}
        """

        response = client.chat.completions.create(

            model="gpt-4o-mini",
            response_format={
                "type": "json_object"
            },

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

        print(
            "PROFILE RAW =",
            content
        )

        return json.loads(
            content
        )

    except Exception as e:

        print(
            "PROFILE ERROR =",
            str(e)
        )

        return {
            "education": None,
            "experience": None,
            "bim_familiarity": None,
            "career_goal": None,
            "lead_quality": None,
            "lead_intent": None
        }