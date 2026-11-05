import re
from pathlib import Path
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = spacy.blank("en")


# ---------------- EMAIL ----------------
def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else ""


# ---------------- PHONE ----------------
def extract_phone(text: str) -> str:
    match = re.search(r'(\+?\d[\d\s\-]{8,15}\d)', text)
    return match.group(0).strip() if match else ""


# ---------------- NAME ----------------
def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Look only at the first few lines
    for line in lines[:6]:
        upper = line.upper()

        # Skip headings, labels, contact information, URLs
        if (
            "RESUME" in upper
            or "CURRICULUM" in upper
            or "CV" in upper
            or "ENGINEER" in upper
            or "DEVELOPER" in upper
            or "STUDENT" in upper
            or "@" in line
            or "HTTP" in upper
            or "WWW" in upper
            or "GITHUB" in upper
            or "LINKEDIN" in upper
            or any(ch.isdigit() for ch in line)
        ):
            continue

        words = line.replace(".", " ").split()

        # Candidate name usually has 2-4 words
        if 2 <= len(words) <= 4:
            return line.title()

    # Fallback to spaCy NER
    try:
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                return ent.text.strip().title()
    except Exception:
        pass

    return ""


# ---------------- SKILLS ----------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_FILE = BASE_DIR / "datasets" / "skills.txt"


def load_skills():
    skills_map = {}
    if SKILLS_FILE.exists():
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                skill = line.strip()
                if skill:
                    skills_map[skill.lower()] = skill
    else:
        # Built-in fallback skills
        defaults = [
            "Python", "Java", "C++", "JavaScript", "TypeScript", "SQL", "HTML", "CSS",
            "React", "Node.js", "FastAPI", "Flask", "Django", "TensorFlow", "PyTorch",
            "Scikit-learn", "Pandas", "NumPy", "Docker", "Git", "GitHub", "AWS",
            "Azure", "MongoDB", "PostgreSQL", "Machine Learning", "REST API"
        ]
        for d in defaults:
            skills_map[d.lower()] = d
    return skills_map


skills_map = load_skills()


def extract_skills(text: str):
    found = {}
    lower_text = text.lower()

    for lower_skill, display_skill in skills_map.items():
        # Word-boundary check preventing substring false positives
        pattern = r'(?<!\w)' + re.escape(lower_skill) + r'(?!\w)'
        if re.search(pattern, lower_text):
            found[display_skill] = True

    return sorted(list(found.keys()))


# ---------------- PARSER ----------------
def parse_resume(text: str):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
