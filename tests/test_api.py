import os
import sys
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.services.resume_parser import extract_skills, extract_email, extract_phone, parse_resume
from app.services.ats_scorer import calculate_ats_score

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "online"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_resume_parser():
    sample_text = """
    Jane Doe
    jane.doe@example.com
    +1 555-123-4567
    Experienced Software Engineer with proficiency in Python, FastAPI, Docker, and React.
    Strong understanding of SQL and REST APIs.
    """
    parsed = parse_resume(sample_text)
    assert parsed["email"] == "jane.doe@example.com"
    assert "Python" in parsed["skills"]
    assert "FastAPI" in parsed["skills"]
    assert "Docker" in parsed["skills"]


def test_ats_scorer():
    sample_resume = "Skilled in Python, FastAPI, Docker, and SQL."
    sample_jd = "Looking for a candidate with Python, FastAPI, React, and Kubernetes."

    result = calculate_ats_score(sample_resume, sample_jd)
    assert "score" in result
    assert "matched_skills" in result
    assert "missing_skills" in result
    assert "Python" in result["matched_skills"]
    assert "React" in result["missing_skills"]


def test_roadmap_endpoint():
    response = client.post(
        "/roadmap/generate",
        json={"missing_skills": ["Docker", "Kubernetes"], "target_role": "DevOps Engineer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "roadmap" in data
    assert len(data["roadmap"]) > 0


if __name__ == "__main__":
    print("Running tests...")
    test_home()
    test_health()
    test_resume_parser()
    test_ats_scorer()
    test_roadmap_endpoint()
    print("All tests passed successfully!")
