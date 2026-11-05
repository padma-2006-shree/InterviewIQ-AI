import os
import requests
import streamlit as st

from styles import load_css
from dashboard import show_dashboard
from interview import show_interview
from roadmap import show_roadmap
from report import show_report

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="InterviewIQ AI - Resume Analyzer & Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom styles
load_css()

# Default Job Description template
DEFAULT_JOB_DESCRIPTION = """
Python
Machine Learning
FastAPI
SQL
Git
React
REST API
Docker
PostgreSQL
Data Structures & Algorithms
"""

# -------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # Backend Connection Selector
    env_backend = os.getenv("BACKEND_URL", "https://interviewiq-ai-1-of73.onrender.com").strip("[]()'\" ").rstrip("/")
    backend_mode = st.radio(
        "Backend Server Environment:",
        ["Cloud Deployment (Render)", "Local Server (127.0.0.1:8000)", "Custom URL"],
        index=0
    )

    if backend_mode == "Cloud Deployment (Render)":
        backend_url = env_backend
    elif backend_mode == "Local Server (127.0.0.1:8000)":
        backend_url = "http://127.0.0.1:8000"
    else:
        backend_url = st.text_input("Enter Custom Backend URL:", value="http://127.0.0.1:8000").rstrip("/")

    # Live Backend Health Indicator
    try:
        health_resp = requests.get(f"{backend_url}/health", timeout=3)
        if health_resp.status_code == 200:
            st.success("🟢 Backend Connected & Healthy")
        else:
            st.warning(f"🟡 Backend Responded with Code: {health_resp.status_code}")
    except Exception:
        st.error("🔴 Backend Unreachable (Check connection)")

    st.divider()

    # Target Job Description Input
    st.markdown("### 📋 Target Job Description")
    st.caption("Paste the requirements of the job you are targeting to compute your tailored ATS score.")
    job_description = st.text_area(
        "Job Description Keywords / Text:",
        value=st.session_state.get("custom_jd", DEFAULT_JOB_DESCRIPTION.strip()),
        height=180
    )
    if st.button("Reset to Default JD"):
        st.session_state.custom_jd = DEFAULT_JOB_DESCRIPTION.strip()
        st.rerun()

    st.divider()
    st.caption("InterviewIQ AI v1.0.0 • AI-driven career prep")

# -------------------------------------------------------
# Header & Hero
# -------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">
        Know your fit, <span class="highlight">before you apply.</span>
    </div>
    <div class="hero-sub">
        AI-Powered Resume Analysis, ATS Scoring, Personalized Interview Simulation & Career Roadmaps.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# File Uploader
# -------------------------------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF, DOCX, TXT):",
    type=["pdf", "docx", "doc", "txt"],
    help="Upload your latest resume to analyze ATS keyword match and generate technical interview practice."
)

if uploaded_file:
    # Check if a new file was uploaded
    if "current_filename" not in st.session_state or st.session_state.current_filename != uploaded_file.name:
        st.session_state.current_filename = uploaded_file.name
        st.session_state.resume_data = None
        st.session_state.ats_data = None
        st.session_state.evaluation_history = []
        st.session_state.questions_list = []
        st.session_state.roadmap_content = None
        st.session_state.final_report = None

    if st.session_state.get("resume_data") is None:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream"
            )
        }

        with st.spinner("🔍 Parsing and analyzing your resume..."):
            try:
                response = requests.post(
                    f"{backend_url}/resume/upload",
                    files=files,
                    timeout=60
                )

                if response.status_code == 200:
                    st.session_state.resume_data = response.json()
                    st.success("✅ Resume processed and extracted successfully!")
                else:
                    st.error(f"Failed to process resume. Backend returned code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to backend server at `{backend_url}`: {e}")

    # Calculate ATS score if resume data is available
    if st.session_state.get("resume_data") and st.session_state.get("ats_data") is None:
        resume_text = st.session_state.resume_data.get("resume_text", "")
        with st.spinner("📊 Calculating ATS compatibility score..."):
            try:
                ats_resp = requests.post(
                    f"{backend_url}/ats/score",
                    json={
                        "resume_text": resume_text,
                        "job_description": job_description
                    },
                    timeout=30
                )
                if ats_resp.status_code == 200:
                    st.session_state.ats_data = ats_resp.json()
                else:
                    st.warning("Could not calculate ATS score from backend.")
            except Exception as e:
                st.warning(f"Error requesting ATS calculation: {e}")

# -------------------------------------------------------
# Render Dashboard & Interactive Modules
# -------------------------------------------------------
if st.session_state.get("resume_data") and st.session_state.get("ats_data"):
    resume_data = st.session_state.resume_data
    ats_data = st.session_state.ats_data
    extracted_skills = resume_data.get("resume", {}).get("skills", [])
    missing_skills = ats_data.get("missing_skills", [])

    st.markdown("---")

    tab_dash, tab_interview, tab_roadmap, tab_report = st.tabs([
        "📊 Candidate & ATS Dashboard",
        "🎙️ AI Mock Interview",
        "🗺️ Skill Gap Roadmap",
        "📑 HR Assessment Report"
    ])

    with tab_dash:
        show_dashboard(resume_data, ats_data)

    with tab_interview:
        show_interview(extracted_skills, backend_url)

    with tab_roadmap:
        show_roadmap(missing_skills, backend_url)

    with tab_report:
        show_report(backend_url)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.markdown("""
<div class="footer">
    <p>🚀 <strong>InterviewIQ AI</strong> — Built with ❤️ using FastAPI • Streamlit • OpenRouter • NLP</p>
</div>
""", unsafe_allow_html=True)
