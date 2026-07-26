from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_similarity(resume_text: str, jd_text: str):

    if not resume_text or not jd_text:
        return 0

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        [resume_text, jd_text]
    )

    score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(float(score) * 100, 2)