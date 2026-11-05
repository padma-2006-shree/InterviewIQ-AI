from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.openrouter_service import get_openrouter_client

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])


class RoadmapRequest(BaseModel):
    missing_skills: List[str]
    target_role: str = "Software Engineer"


def _fallback_roadmap(skills: List[str], role: str) -> str:
    if not skills:
        return "Congratulations! You currently match all key skills for this role. Focus on system design and mock interviews."

    weeks = []
    chunk_size = max(1, len(skills) // 4 + 1)
    chunks = [skills[i:i + chunk_size] for i in range(0, len(skills), chunk_size)]

    for idx, chunk in enumerate(chunks[:4], 1):
        skill_str = ", ".join(chunk)
        weeks.append(
            f"### Week {idx}: Fundamentals of {skill_str}\n"
            f"- Study core documentation, architecture, and syntax for {skill_str}.\n"
            f"- Build a hands-on mini project implementing {chunk[0]}.\n"
            f"- Learn common interview questions and debugging techniques."
        )

    return f"# 4-Week Skill Mastery Roadmap: {role}\n\n" + "\n\n".join(weeks)


@router.post("/generate")
def generate_roadmap(data: RoadmapRequest):
    """Generate a structured personalized learning roadmap to bridge skill gaps."""
    if not data.missing_skills:
        return {
            "roadmap": "No skill gaps identified! You are well-aligned with the target role."
        }

    client = get_openrouter_client()
    if client:
        try:
            prompt = f"""You are a Senior Technical Career Coach.
Create a focused, practical, 4-week learning roadmap for a candidate aiming to become a {data.target_role}.
They need to master the following missing skills:
{', '.join(data.missing_skills)}

Format as clean markdown:
- Break it down into Week 1, Week 2, Week 3, Week 4.
- For each week, provide specific topics, recommended practical project tasks, and key interview concepts.
Keep it practical, motivating, and concise.
"""
            response = client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=700,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return {"roadmap": content.strip()}
        except Exception:
            pass

    return {"roadmap": _fallback_roadmap(data.missing_skills, data.target_role)}
