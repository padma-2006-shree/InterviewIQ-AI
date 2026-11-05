import re
from typing import Dict, Optional


def extract_years_of_experience(text: str) -> Optional[float]:
    """Extract mentioned years of experience from resume text."""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience',
        r'experience\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)',
        r'(\d+)\s*\+?\s*years?\s+in\s+[a-zA-Z]+'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                continue
    return None


def match_experience(resume_text: str, jd_text: str) -> Dict[str, any]:
    """Compare candidate experience against job requirements."""
    candidate_exp = extract_years_of_experience(resume_text)
    required_exp = extract_years_of_experience(jd_text)

    if required_exp is None:
        status = "No specific years of experience required in job description."
        meets_requirement = True
    elif candidate_exp is None:
        status = f"Job requires ~{required_exp} years; candidate years of experience not explicitly stated."
        meets_requirement = False
    elif candidate_exp >= required_exp:
        status = f"Meets experience requirement ({candidate_exp} yrs vs {required_exp} yrs required)."
        meets_requirement = True
    else:
        status = f"Below preferred experience ({candidate_exp} yrs vs {required_exp} yrs required)."
        meets_requirement = False

    return {
        "candidate_years": candidate_exp,
        "required_years": required_exp,
        "meets_requirement": meets_requirement,
        "status": status
    }
