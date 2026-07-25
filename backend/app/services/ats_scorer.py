from app.services.skill_matcher import match_skills
from app.services.resume_parser import extract_skills


def calculate_ats_score(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    score = match_skills(
        resume_skills,
        job_skills
    )

    matched_skills = [
        skill for skill in resume_skills
        if skill.lower() in [s.lower() for s in job_skills]
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill.lower() not in [s.lower() for s in resume_skills]
    ]

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }