import os
import requests
import streamlit as st


def show_roadmap(missing_skills: list, backend_url: str):
    st.subheader("🗺️ Personalized Learning Roadmap")
    st.write(
        "Bridge your skill gaps with a customized, week-by-week technical learning plan "
        "designed specifically around the competencies you need to master."
    )

    if not missing_skills:
        st.success("🎉 You have no missing skills for this job description! Keep refining your interview skills.")
        return

    st.markdown(f"**Identified Missing Skills:** {', '.join(missing_skills)}")

    target_role = st.text_input(
        "Target Role Title:",
        value="Software Engineer",
        help="Specify the target job title to customize roadmap focus."
    )

    if st.button("🚀 Generate 4-Week Learning Roadmap"):
        with st.spinner("Building your customized learning plan..."):
            try:
                response = requests.post(
                    f"{backend_url}/roadmap/generate",
                    json={
                        "missing_skills": missing_skills,
                        "target_role": target_role
                    },
                    timeout=45
                )
                if response.status_code == 200:
                    roadmap_text = response.json().get("roadmap", "")
                    st.session_state.roadmap_content = roadmap_text
                    st.success("✅ Roadmap generated successfully!")
                else:
                    st.error(f"Failed to generate roadmap. Backend returned code {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error to backend: {e}")

    if "roadmap_content" in st.session_state and st.session_state.roadmap_content:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(st.session_state.roadmap_content)
        st.markdown("</div>", unsafe_allow_html=True)
