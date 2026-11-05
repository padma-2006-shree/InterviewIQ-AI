import os
from app.services.openrouter_service import get_openrouter_client


def _fallback_evaluate(question: str, answer: str) -> str:
    """Provide a structured evaluation when LLM API is unavailable."""
    answer_len = len(answer.strip().split())
    if answer_len < 10:
        score = 4
        strengths = "- Attempted the question directly."
        weaknesses = "- The answer is too brief and lacks technical depth and examples.\n- Does not fully explain the underlying concepts."
        suggestion = "Provide a more comprehensive answer including real-world examples, architectural implications, and edge cases."
    elif answer_len < 30:
        score = 6
        strengths = "- Identified basic definitions and relevant concepts."
        weaknesses = "- Could explain trade-offs and practical code/design implementations.\n- Answer is somewhat generic."
        suggestion = "Structure your answer using the STAR method (Situation, Task, Action, Result) or discuss performance trade-offs."
    else:
        score = 8
        strengths = "- Thorough explanation with relevant terminology and good clarity.\n- Logical flow and clear technical understanding."
        weaknesses = "- Could highlight failure modes, scaling considerations, or best practices in production."
        suggestion = "Mention specific production experiences or metrics to make your answer stand out to interviewers."

    return f"""Score: {score}/10

Strengths:
{strengths}

Weaknesses:
{weaknesses}

Suggestions:
- {suggestion}

Key Takeaway:
Focus on explaining not just 'what' the technology does, but 'why' and 'how' you apply it effectively in real systems.
"""


def evaluate_answer(question: str, answer: str) -> str:
    """Evaluate candidate answer using OpenRouter with fallback support."""
    if not answer or not answer.strip():
        return "Score: 0/10\n\nStrengths: None\n\nWeaknesses:\n- No answer was provided.\n\nSuggestions:\n- Always attempt to answer by sharing what you know or explaining your reasoning approach."

    client = get_openrouter_client()
    if client:
        try:
            prompt = f"""You are a Senior Technical Interviewer and Hiring Manager.

Question:
{question}

Candidate's Answer:
{answer}

Evaluate the candidate's answer thoroughly and constructively.
Return your evaluation formatted as follows:

Score: <X>/10

Strengths:
- <strength 1>
- <strength 2>

Weaknesses:
- <weakness 1>
- <weakness 2>

Model / Ideal Answer:
<Clear, concise ideal answer for reference>

Suggestions for Improvement:
- <Actionable tip>
"""
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=600,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception:
            pass

    return _fallback_evaluate(question, answer)
