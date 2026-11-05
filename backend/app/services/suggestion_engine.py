import re
from typing import Dict, List


def generate_resume_suggestions(resume_text: str, missing_skills: List[str], ats_score: float) -> List[str]:
    """Generate intelligent suggestions for optimizing the resume based on ATS analysis."""
    suggestions = []

    # Missing skills suggestions
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append(
            f"Add key missing technologies to your Skills section or project descriptions: {', '.join(top_missing)}."
        )

    # Action verbs check
    action_verbs = [
        "built", "developed", "architected", "engineered", "designed",
        "implemented", "led", "optimized", "reduced", "scaled", "deployed"
    ]
    lower_text = resume_text.lower()
    found_verbs = [v for v in action_verbs if v in lower_text]
    if len(found_verbs) < 3:
        suggestions.append(
            "Use strong action verbs (e.g., 'Architected', 'Engineered', 'Optimized', 'Deployed') at the beginning of bullet points."
        )

    # Metrics and numbers check
    metrics = re.findall(r'(\d+%\s*|\$\d+|\d+\s*x|\d+\s*users|\d+\s*ms|\d+\s*k)', lower_text)
    if len(metrics) < 2:
        suggestions.append(
            "Quantify your achievements with concrete metrics (e.g., 'Improved API latency by 35%', 'Scaled platform to 10k users')."
        )

    # Word count check
    words = resume_text.split()
    if len(words) < 200:
        suggestions.append(
            "Your resume is relatively short. Add more details about your project responsibilities and technical accomplishments."
        )
    elif len(words) > 1000:
        suggestions.append(
            "Your resume is quite lengthy. Consider condensing content to 1-2 focused pages for better readability."
        )

    # ATS score-specific advice
    if ats_score < 60:
        suggestions.append(
            "Align your terminology directly with the job description keywords to increase keyword frequency."
        )

    if not suggestions:
        suggestions.append("Great job! Your resume is well-structured and aligns closely with the target role.")

    return suggestions
