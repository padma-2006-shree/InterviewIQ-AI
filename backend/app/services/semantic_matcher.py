import math
import re
from collections import Counter


def semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Compute semantic text alignment between resume and job description.
    Uses pure-Python TF-IDF cosine similarity for high speed and minimal bundle size,
    with automatic fallback to scikit-learn if installed.
    """
    if not resume_text or not jd_text:
        return 0.0

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception:
        pass

    # Lightweight, high-accuracy pure Python TF-IDF cosine similarity
    stopwords = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
        "by", "can", "did", "do", "does", "doing", "don", "down", "during", "each", "few", "for",
        "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
        "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
        "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
        "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
        "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs", "them",
        "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
        "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
        "who", "whom", "why", "with", "will", "would", "you", "your", "yours", "yourself"
    }

    def tokenize(text):
        words = re.findall(r'[a-zA-Z0-9+#.-]+', text.lower())
        return [w for w in words if len(w) >= 2 and w not in stopwords]

    tokens1 = tokenize(resume_text)
    tokens2 = tokenize(jd_text)

    if not tokens1 or not tokens2:
        return 0.0

    tf1 = Counter(tokens1)
    tf2 = Counter(tokens2)

    all_vocab = set(tf1.keys()).union(set(tf2.keys()))
    vec1 = {}
    vec2 = {}

    for term in all_vocab:
        # Document frequency: 1 if term is in 1 document, 2 if in both
        df = (1 if term in tf1 else 0) + (1 if term in tf2 else 0)
        idf = math.log((2 + 1) / (df + 1)) + 1.0
        vec1[term] = tf1.get(term, 0) * idf
        vec2[term] = tf2.get(term, 0) * idf

    dot_product = sum(vec1[t] * vec2[t] for t in all_vocab)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    cosine = (dot_product / (mag1 * mag2)) * 100
    return round(float(cosine), 2)
