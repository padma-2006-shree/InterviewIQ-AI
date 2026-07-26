def match_skills(resume_skills, job_skills):

    if not resume_skills or not job_skills:
        return 0

    resume_set = {skill.lower() for skill in resume_skills}
    job_set = {skill.lower() for skill in job_skills}

    matched_skills = resume_set.intersection(job_set)

    score = (len(matched_skills) / len(job_set)) * 100

    return round(score, 2)