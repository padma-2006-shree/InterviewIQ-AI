import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def show_dashboard(data, ats):

    score = ats["score"]
    matched = ats["matched_skills"]
    missing = ats["missing_skills"]

    # ---------------- HERO ----------------

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    Know your fit,<br>
    before you <span class="highlight">apply.</span>
    </div>

    <div class="hero-sub">
    AI-powered Resume Analysis with ATS scoring,
    skill matching and interview preparation.
    </div>

    </div>
    """, unsafe_allow_html=True)

    # ---------------- PROFILE + ATS ----------------

    left, right = st.columns([2, 1])

    with left:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("👤 Candidate Profile")

        st.write(f"**Name:** {data['resume']['name']}")
        st.write(f"**Email:** {data['resume']['email']}")
        st.write(f"**Phone:** {data['resume']['phone']}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "ATS Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#3B82F6"},

                "steps": [

                    {"range": [0, 40], "color": "#3b1d1d"},

                    {"range": [40, 70], "color": "#4b4314"},

                    {"range": [70, 100], "color": "#12391f"}

                ]

            }

        ))

        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}
        )

        st.plotly_chart(gauge, use_container_width=True)

        st.progress(score / 100)

        if score >= 80:
            st.success("Excellent Resume")

        elif score >= 60:
            st.warning("Good Resume")

        else:
            st.error("Needs Improvement")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SKILLS ----------------

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("💻 Extracted Skills")

    badges = ""

    for skill in data["resume"]["skills"]:
        badges += f'<span class="badge">{skill}</span>'

    st.markdown(badges, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CHART ----------------

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.subheader("📊 Resume Skills")

    chart = {

        "Skill": data["resume"]["skills"],

        "Count": [1] * len(data["resume"]["skills"])

    }

    fig = px.bar(

        chart,

        x="Skill",

        y="Count",

        color="Skill"

    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font_color="white",

        showlegend=False

    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- MATCHED ----------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("✅ Matched Skills")

        if matched:

            for skill in matched:
                st.success(skill)

        else:

            st.info("No matched skills.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("❌ Missing Skills")

        if missing:

            for skill in missing:
                st.warning(skill)

        else:

            st.success("No missing skills 🎉")

        st.markdown("</div>", unsafe_allow_html=True)