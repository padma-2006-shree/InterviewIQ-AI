from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def match_skills(resume_skills, job_skills):
    """
    Returns similarity score between resume skills and job skills.
    """

    if len(resume_skills) == 0 or len(job_skills) == 0:
        return 0

    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])

    score = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    return round(float(score) * 100, 2)