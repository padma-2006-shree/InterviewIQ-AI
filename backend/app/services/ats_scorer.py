from app.services.skill_matcher import match_skills
from app.services.resume_parser import extract_skills
from app.services.semantic_matcher import semantic_similarity
from app.services.suggestion_engine import generate_resume_suggestions


def calculate_ats_score(resume_text: str, job_description: str):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    skill_score = match_skills(resume_skills, job_skills)
    semantic_score = semantic_similarity(resume_text, job_description)

    # Combined composite ATS score: 70% skill overlap + 30% semantic text alignment
    if job_skills:
        composite_score = round((0.70 * skill_score) + (0.30 * semantic_score), 2)
    else:
        # If no explicit skills found in JD, rely more on semantic similarity
        composite_score = round(semantic_score, 2)

    resume_skills_lower = {s.lower(): s for s in resume_skills}
    job_skills_lower = {s.lower(): s for s in job_skills}

    matched_skills = [
        job_skills_lower[k] for k in job_skills_lower if k in resume_skills_lower
    ]

    missing_skills = [
        job_skills_lower[k] for k in job_skills_lower if k not in resume_skills_lower
    ]

    suggestions = generate_resume_suggestions(
        resume_text=resume_text,
        missing_skills=missing_skills,
        ats_score=composite_score
    )

    return {
        "score": composite_score,
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "suggestions": suggestions
    }
