import os
import requests
import streamlit as st

# Setup dynamic backend URL with fallback and character sanitization
BACKEND_URL = os.getenv("BACKEND_URL", "https://interviewiq-ai-1-of73.onrender.com")
BACKEND_URL = BACKEND_URL.strip("[]()'\" ").rstrip("/")


def show_interview(extracted_skills):
    st.subheader("🎯 AI Interview Questions")
    st.write(
        "Click below to generate personalized interview questions based on your extracted skills."
    )

    if st.button("🤖 Generate AI Questions"):
        with st.spinner("Generating interview questions..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/interview/questions",
                    json={"skills": extracted_skills},
                    timeout=45,
                )

                if response.status_code == 200:
                    questions_data = response.json()
                    st.session_state.questions = questions_data
                    st.success("🎉 Questions generated successfully!")
                else:
                    st.error(
                        f"Failed to generate questions. Server returned status code: {response.status_code}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(
                    f"Could not connect to backend at `{BACKEND_URL}`. Error: {e}"
                )

    # Display saved questions from Streamlit session state
    if "questions" in st.session_state:
        st.divider()
        st.markdown("### 📝 Practice Questions")
        questions = st.session_state.questions

        if isinstance(questions, list):
            for idx, q in enumerate(questions, 1):
                st.markdown(f"**Q{idx}:** {q}")
        elif isinstance(questions, dict):
            for category, q_list in questions.items():
                st.markdown(f"#### {category.capitalize()}")
                if isinstance(q_list, list):
                    for q in q_list:
                        st.markdown(f"- {q}")
                else:
                    st.write(q_list)
        else:
            st.write(questions)