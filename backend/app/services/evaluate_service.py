import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def evaluate_answer(question, answer):

    prompt = f"""
You are a Senior Software Engineer interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return:

Score: /10

Strengths

Weaknesses

Correct Answer
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content