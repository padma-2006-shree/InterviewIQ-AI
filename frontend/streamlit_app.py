import os
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard import show_dashboard
from interview import show_interview
from report import show_report

# -------------------------------------------------------
# Environment Setup & Base Config
# -------------------------------------------------------

BACKEND_URL = os.getenv("BACKEND_URL", "https://interviewiq-ai-1-of73.onrender.com")
# Strip unwanted brackets, quotes, spaces, or trailing slashes
BACKEND_URL = BACKEND_URL.strip("[]()'\" ").rstrip("/")

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="InterviewIQ AI",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#F5F7FB;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Title */

h1{
    color:#2563EB;
    text-align:center;
}

h2,h3{
    color:#1E3A8A;
}

/* Button */

.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:10px;
    border:none;
    padding:12px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

/* Upload Box */

[data-testid="stFileUploader"]{
    border:2px dashed #2563EB;
    border-radius:15px;
    padding:20px;
    background:white;
}

/* Metric */

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,.08);
}

/* Cards */

.stAlert{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown("# 🤖 InterviewIQ AI")
st.markdown("### AI Resume Analyzer & Interview Assistant")

st.divider()

# -------------------------------------------------------
# Upload File Component
# -------------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your Resume",
    type=["pdf", "docx"]
)

# -------------------------------------------------------
# Resume Upload Processing
# -------------------------------------------------------

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response_data = None

    with st.spinner("🔍 Analyzing Resume..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/resume/upload",
                files=files,
                timeout=60
            )

            if response.status_code == 200:
                response_data = response.json()
                st.session_state.resume_data = response_data
                st.success("✅ Resume Uploaded Successfully!")
            else:
                st.error(f"Failed to analyze resume. Server returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend server at `{BACKEND_URL}`. Error details: {e}")

    if response_data:
        data = response_data

        # ---------------------------------------------------
        # ATS Score Calculation
        # ---------------------------------------------------

        job_description = """
Python
Machine Learning
FastAPI
SQL
Git
React
REST API
"""

        score = 0
        matched = []
        missing = []

        with st.spinner("📈 Calculating ATS Score..."):
            try:
                ats_response = requests.post(
                    f"{BACKEND_URL}/ats/score",
                    json={
                        "resume_text": data.get("resume_text", ""),
                        "job_description": job_description
                    },
                    timeout=30
                )

                if ats_response.status_code == 200:
                    ats = ats_response.json()
                    score = ats.get("score", 0)
                    matched = ats.get("matched_skills", [])
                    missing = ats.get("missing_skills", [])
                else:
                    st.error("Failed to calculate ATS Score from server.")

            except requests.exceptions.RequestException:
                st.error("Unable to calculate ATS Score due to a connection error.")

        # ---------------------------------------------------
        # Candidate Profile & ATS Score Gauges
        # ---------------------------------------------------

        left, right = st.columns([2, 1])

        with left:
            st.subheader("👤 Candidate Profile")
            resume_info = data.get("resume", {})
            st.info(f"👤 **Name:** {resume_info.get('name', 'N/A')}")
            st.info(f"📧 **Email:** {resume_info.get('email', 'N/A')}")
            st.info(f"📱 **Phone:** {resume_info.get('phone', 'N/A')}")

        with right:
            st.subheader("📊 ATS Score")

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "ATS Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 50], "color": "#ffcccc"},
                        {"range": [50, 80], "color": "#fff4cc"},
                        {"range": [80, 100], "color": "#d4edda"}
                    ]
                }
            ))

            st.plotly_chart(gauge, use_container_width=True)
            st.progress(score / 100)

            if score >= 80:
                st.success("🌟 Excellent Resume")
            elif score >= 60:
                st.warning("👍 Good Resume")
            else:
                st.error("⚠ Needs Improvement")

        st.divider()

        # ---------------------------------------------------
        # Extracted Skills Grid
        # ---------------------------------------------------

        st.subheader("💻 Extracted Skills")
        extracted_skills = resume_info.get("skills", [])

        if extracted_skills:
            cols = st.columns(4)
            for i, skill in enumerate(extracted_skills):
                cols[i % 4].success(skill)
        else:
            st.info("No skills detected in resume.")

        st.divider()

        # ---------------------------------------------------
        # Skill Chart
        # ---------------------------------------------------

        if extracted_skills:
            st.subheader("📊 Resume Skill Distribution")

            chart_data = {
                "Skill": extracted_skills,
                "Count": [1] * len(extracted_skills)
            }

            fig = px.bar(
                chart_data,
                x="Skill",
                y="Count",
                color="Skill",
                title="Skills Extracted From Resume"
            )

            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

        # ---------------------------------------------------
        # Matched & Missing Skills
        # ---------------------------------------------------

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("✅ Matched Skills")
            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.info("No Matched Skills")

        with c2:
            st.subheader("❌ Missing Skills")
            if missing:
                for skill in missing:
                    st.warning(skill)
            else:
                st.success("No Missing Skills 🎉")

        st.divider()

        # ---------------------------------------------------
        # Interactive Interview Section
        # ---------------------------------------------------

        show_interview(extracted_skills)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown(
    """
    <center>
    <h4 style='color:#2563EB'>🚀 InterviewIQ AI</h4>
    Built with ❤️ using FastAPI • Streamlit • OpenRouter • NLP
    </center>
    """,
    unsafe_allow_html=True
)