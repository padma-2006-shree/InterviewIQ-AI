import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def show_interview(skills):

    st.markdown("## 🎯 AI Interview Practice")
    st.write("Generate personalized interview questions based on your resume skills.")

    # -------------------------
    # Generate Questions
    # -------------------------

    if st.button("🚀 Generate Questions"):

        with st.spinner("Generating interview questions..."):

            response = requests.post(
                f"{BACKEND_URL}/interview/questions",
                json={
                    "skills": skills
                }
            )

        if response.status_code == 200:

            questions = response.json()["questions"]

            # Convert string response into list
            if isinstance(questions, str):

                questions = [
                    q.strip()
                    for q in questions.split("\n")
                    if q.strip()
                ]

            st.session_state.questions = questions
            st.session_state.current_question = 0

        else:

            st.error(response.text)

    # -------------------------
    # Stop if no questions
    # -------------------------

    if "questions" not in st.session_state:
        return

    questions = st.session_state.questions
    index = st.session_state.current_question

    if index >= len(questions):

        st.success("🎉 Interview Completed!")

        return

    question = questions[index]

    # -------------------------
    # Current Question
    # -------------------------

    st.progress((index + 1) / len(questions))

    st.subheader(f"Question {index + 1} of {len(questions)}")

    st.info(question)

    answer = st.text_area(
        "Your Answer",
        key=f"answer_{index}",
        height=180
    )

    # -------------------------
    # Submit Answer
    # -------------------------

    if st.button("✅ Submit Answer"):

        if answer.strip() == "":

            st.warning("Please enter your answer before submitting.")

        else:

            with st.spinner("AI is evaluating your answer..."):

                evaluation = requests.post(
                    f"{BACKEND_URL}/evaluate/",
                    json={
                        "question": question,
                        "answer": answer
                    }
                )

            if evaluation.status_code == 200:

                result = evaluation.json()["evaluation"]

                if "evaluation_history" not in st.session_state:
                    st.session_state.evaluation_history = []

                st.session_state.evaluation_history.append(result)

                st.success("✅ Evaluation Completed")

                st.markdown(result)

            else:

                st.error(evaluation.text)

    # -------------------------
    # Next Button
    # -------------------------

    col1, col2 = st.columns([4, 1])

    with col2:

        if st.button("➡ Next"):

            st.session_state.current_question += 1

            st.rerun()