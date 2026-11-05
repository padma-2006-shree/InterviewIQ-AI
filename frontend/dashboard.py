import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def show_dashboard(data, ats):
    score = ats.get("score", 0)
    matched = ats.get("matched_skills", [])
    missing = ats.get("missing_skills", [])
    suggestions = ats.get("suggestions", [])
    resume_info = data.get("resume", {})

    # ---------------- PROFILE + ATS GAUGE ----------------
    left, right = st.columns([1.6, 1.4])

    with left:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("👤 Candidate Profile")
        
        name = resume_info.get("name") or "Not detected"
        email = resume_info.get("email") or "Not detected"
        phone = resume_info.get("phone") or "Not detected"

        st.markdown(f"**Name:** `{name}`")
        st.markdown(f"**Email:** `{email}`")
        st.markdown(f"**Phone:** `{phone}`")
        st.markdown(f"**Filename:** `{data.get('filename', 'resume')}`")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📈 ATS Match Score")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "ATS Compatibility (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#3B82F6"},
                "steps": [
                    {"range": [0, 50], "color": "rgba(239, 68, 68, 0.25)"},
                    {"range": [50, 75], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [75, 100], "color": "rgba(16, 185, 129, 0.25)"}
                ]
            }
        ))

        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            height=200,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(gauge, use_container_width=True)

        if score >= 75:
            st.success("🌟 Excellent ATS match! Strong alignment with job requirements.")
        elif score >= 50:
            st.warning("👍 Good match, but some target skills are missing.")
        else:
            st.error("⚠️ Low ATS score. Review missing skills and recommendations below.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SKILLS BREAKDOWN ----------------
    col_matched, col_missing = st.columns(2)

    with col_matched:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader(f"✅ Matched Skills ({len(matched)})")
        if matched:
            badges = "".join([f'<span class="badge-matched">{s}</span>' for s in matched])
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No matching skills detected between resume and job description.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_missing:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader(f"⚠️ Missing Skills ({len(missing)})")
        if missing:
            badges = "".join([f'<span class="badge-missing">{s}</span>' for s in missing])
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.success("🎉 All required skills detected in your resume!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ALL EXTRACTED SKILLS & CHART ----------------
    skills = resume_info.get("skills", [])
    if skills:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader(f"🛠️ All Extracted Skills ({len(skills)})")
        badges = "".join([f'<span class="badge">{s}</span>' for s in skills])
        st.markdown(badges, unsafe_allow_html=True)

        chart_data = {
            "Skill": skills[:15],
            "Frequency": [1] * len(skills[:15])
        }
        fig = px.bar(
            chart_data,
            x="Skill",
            y="Frequency",
            color="Skill",
            title="Top Skills Detected from Resume"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=False,
            height=280
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ACTIONABLE RECOMMENDATIONS ----------------
    if suggestions:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("💡 ATS Optimization Suggestions")
        for tip in suggestions:
            st.markdown(f"- {tip}")
        st.markdown("</div>", unsafe_allow_html=True)
