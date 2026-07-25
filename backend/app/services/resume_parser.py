import re
import spacy
from pathlib import Path

nlp = spacy.load("en_core_web_sm")


# ---------------- EMAIL ----------------
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else ""


# ---------------- PHONE ----------------
def extract_phone(text):
    match = re.search(r'(\+?\d[\d\s\-]{8,15}\d)', text)
    return match.group(0) if match else ""


# ---------------- NAME ----------------
def extract_name(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Look only at the first few lines
    for line in lines[:5]:

        upper = line.upper()

        # Skip headings and contact information
        if (
            "ENGINEER" in upper
            or "STUDENT" in upper
            or "@" in line
            or "HTTP" in upper
            or "WWW" in upper
            or any(ch.isdigit() for ch in line)
        ):
            continue

        words = line.replace(".", " ").split()

        # Candidate name usually has 2-4 words
        if 2 <= len(words) <= 4:
            return line.title()

    # Fallback to spaCy
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return ""


# ---------------- SKILLS ----------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_FILE = BASE_DIR / "datasets" / "skills.txt"


def load_skills():
    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        return [skill.strip().lower() for skill in f]


skills_db = load_skills()


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill.title())

    return sorted(list(set(found)))


# ---------------- PARSER ----------------
def parse_resume(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }