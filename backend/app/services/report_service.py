import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_report(evaluation):

    prompt = f"""
You are an HR Manager.

Based on this interview evaluation:

{evaluation}

Generate a professional report.

Format:

Overall Score:
/10

Technical Skills:
/10

Communication:
/10

Strengths:
- ...

Weaknesses:
- ...

Recommendation:
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content