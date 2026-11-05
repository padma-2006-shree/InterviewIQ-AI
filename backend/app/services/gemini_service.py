import os
from app.services.openrouter_service import get_openrouter_client


SKILL_QUESTION_BANK = {
    "python": [
        "What is the difference between deep copy and shallow copy in Python?",
        "Explain how Python's memory management and Garbage Collection work.",
        "What are decorators in Python and how would you create one with arguments?",
        "Explain the difference between generators and iterators in Python."
    ],
    "fastapi": [
        "How does FastAPI achieve high performance compared to other Python frameworks?",
        "Explain the role of Pydantic models in FastAPI for request validation and response serialization.",
        "What is dependency injection in FastAPI and how do you implement it using Depends?"
    ],
    "react": [
        "Explain the virtual DOM in React and how the reconciliation process works.",
        "What are the key differences between useMemo and useCallback hooks?",
        "How do you manage complex application state in React?"
    ],
    "sql": [
        "What are the differences between clustered and non-clustered indexes in SQL?",
        "Explain the ACID properties of database transactions.",
        "When would you use an INNER JOIN versus an OUTER JOIN or CROSS APPLY?"
    ],
    "machine learning": [
        "How do you address overfitting in a machine learning model?",
        "Explain the trade-off between Precision and Recall. When would you prioritize one over the other?",
        "What is cross-validation and why is it important?"
    ],
    "git": [
        "What is the difference between git merge and git rebase?",
        "How do you resolve a complex merge conflict in a collaborative environment?"
    ],
    "docker": [
        "What is the difference between a Docker image and a Docker container?",
        "How do you optimize a multi-stage Dockerfile for production deployment?"
    ],
    "rest api": [
        "What are the core constraints of RESTful architecture?",
        "What is the difference between PUT and PATCH HTTP methods?"
    ]
}


def _get_fallback_questions(skills: list[str]) -> str:
    """Generate curated, relevant technical questions when LLM service is unavailable."""
    selected_questions = []
    normalized_skills = [s.lower().strip() for s in skills]

    for skill in normalized_skills:
        for bank_key, bank_qs in SKILL_QUESTION_BANK.items():
            if bank_key in skill or skill in bank_key:
                for q in bank_qs:
                    if q not in selected_questions:
                        selected_questions.append(q)

    # Add general technical questions if we need more
    general_qs = [
        "Describe a challenging technical problem you solved and how you approached debugging it.",
        "How do you ensure code quality, testability, and maintainability in your projects?",
        "How do you design scalable RESTful APIs with proper authentication and error handling?",
        "Explain how you approach CI/CD and deployment automation in your workflow."
    ]

    for q in general_qs:
        if len(selected_questions) < 8 and q not in selected_questions:
            selected_questions.append(q)

    return "\n".join(f"{i+1}. {q}" for i, q in enumerate(selected_questions[:10]))


def generate_interview_questions(skills: list[str]) -> str:
    """Generate technical interview questions using OpenRouter LLM with fallback support."""
    if not skills:
        skills = ["Software Engineering", "Python", "Problem Solving"]

    client = get_openrouter_client()
    if client:
        try:
            prompt = f"""You are a Senior Technical Interviewer at a top tech company.
Generate exactly 8-10 targeted technical interview questions evaluating the candidate on these skills:
{', '.join(skills)}

Requirements:
1. Provide a mix of conceptual, practical, and problem-solving questions.
2. Number each question from 1 to 10.
3. Return only the numbered questions without conversational intro or outro text.
"""
            response = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception:
            # Fallback to curated question bank on LLM failure
            pass

    return _get_fallback_questions(skills)
