import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from dashboard import show_dashboard
from interview import show_interview
from report import show_report

BACKEND_URL = "http://127.0.0.1:8000"

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
# Upload
# -------------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your Resume",
    type=["pdf", "docx"]
)

# -------------------------------------------------------
# Resume Upload
# -------------------------------------------------------

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            uploaded_file.type
        )
    }

    with st.spinner("🔍 Analyzing Resume..."):

        response = requests.post(
            f"{BACKEND_URL}/resume/upload",
            files=files
        )

    if response.status_code == 200:

        data = response.json()
        st.session_state.resume_data = data
        st.success("✅ Resume Uploaded Successfully!")
        
        # ---------------------------------------------------
        # ATS Score API
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

        with st.spinner("📈 Calculating ATS Score..."):

            ats_response = requests.post(
                f"{BACKEND_URL}/ats/score",
                json={
                    "resume_text": data["resume_text"],
                    "job_description": job_description
                }
            )

        if ats_response.status_code == 200:

            ats = ats_response.json()

            score = ats["score"]
            matched = ats["matched_skills"]
            missing = ats["missing_skills"]

        else:

            score = 0
            matched = []
            missing = []

            st.error("Failed to calculate ATS Score")

        # ---------------------------------------------------
        # Dashboard
        # ---------------------------------------------------

        left, right = st.columns([2,1])

        with left:

            st.subheader("👤 Candidate Profile")

            st.info(f"👤 **Name:** {data['resume']['name']}")
            st.info(f"📧 **Email:** {data['resume']['email']}")
            st.info(f"📱 **Phone:** {data['resume']['phone']}")

        with right:

            st.subheader("📊 ATS Score")

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text":"ATS Score"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"green"},
                    "steps":[
                        {"range":[0,50],"color":"#ffcccc"},
                        {"range":[50,80],"color":"#fff4cc"},
                        {"range":[80,100],"color":"#d4edda"}
                    ]
                }
            ))

            st.plotly_chart(gauge, use_container_width=True)

            st.progress(score/100)

            if score >= 80:
                st.success("🌟 Excellent Resume")

            elif score >= 60:
                st.warning("👍 Good Resume")

            else:
                st.error("⚠ Needs Improvement")

        st.divider()

        # ---------------------------------------------------
        # Skills
        # ---------------------------------------------------

        st.subheader("💻 Extracted Skills")

        cols = st.columns(4)

        for i, skill in enumerate(data["resume"]["skills"]):
            cols[i % 4].success(skill)

        st.divider()

        # ---------------------------------------------------
        # Skill Chart
        # ---------------------------------------------------

        st.subheader("📊 Resume Skill Distribution")

        chart = {
            "Skill": data["resume"]["skills"],
            "Count": [1]*len(data["resume"]["skills"])
        }

        fig = px.bar(
            chart,
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
        show_interview(data["resume"]["skills"])


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown(
    """
    <center>

    <h4 style='color:#2563EB'>
    🚀 InterviewIQ AI
    </h4>

    Built with ❤️ using FastAPI • Streamlit • OpenRouter • NLP

    </center>
    """,
    unsafe_allow_html=True
)