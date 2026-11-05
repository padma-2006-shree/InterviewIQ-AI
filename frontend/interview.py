import os
import re
import requests
import streamlit as st


def _parse_questions_to_list(questions_raw) -> list:
    """Parse raw string or dict questions into a clean list of individual questions."""
    if isinstance(questions_raw, list):
        return [str(q).strip() for q in questions_raw if str(q).strip()]

    if isinstance(questions_raw, dict):
        parsed = []
        for val in questions_raw.values():
            if isinstance(val, list):
                parsed.extend([str(item).strip() for item in val if str(item).strip()])
            elif isinstance(val, str):
                lines = [line.strip() for line in val.split("\n") if line.strip()]
                parsed.extend(lines)
        return parsed

    if isinstance(questions_raw, str):
        lines = [line.strip() for line in questions_raw.split("\n") if line.strip()]
        cleaned = []
        for line in lines:
            # Strip numbering like '1. ', 'Q1: ', '1) '
            match = re.match(r'^(?:(?:Q\d+[:.]?|\d+[.)])\s*)?(.*)$', line)
            cleaned_line = match.group(1).strip() if match else line
            if len(cleaned_line) > 10 and not cleaned_line.lower().startswith("here are"):
                cleaned.append(cleaned_line)
        return cleaned if cleaned else [questions_raw]

    return [str(questions_raw)]


def show_interview(extracted_skills: list, backend_url: str):
    st.subheader("🎙️ AI Technical Mock Interview")
    st.write(
        "Generate role-specific interview questions based on your resume skills, "
        "practice answering them, and receive immediate AI-powered scoring and feedback."
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🤖 Generate Personalized Interview Questions"):
            with st.spinner("Generating interview questions tailored to your skills..."):
                try:
                    response = requests.post(
                        f"{backend_url}/interview/questions",
                        json={"skills": extracted_skills if extracted_skills else ["Python", "Software Engineering"]},
                        timeout=45,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        raw_qs = data.get("questions", "")
                        q_list = _parse_questions_to_list(raw_qs)
                        st.session_state.questions_list = q_list
                        st.session_state.raw_questions = raw_qs
                        st.success(f"🎉 Generated {len(q_list)} technical interview questions!")
                    else:
                        st.error(f"Failed to generate questions. Server returned code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to backend at `{backend_url}`. Error: {e}")

    with col2:
        if "questions_list" in st.session_state and st.session_state.questions_list:
            st.metric("Questions Available", len(st.session_state.questions_list))

    # ---------------- INTERACTIVE PRACTICE & EVALUATION ----------------
    if "questions_list" in st.session_state and st.session_state.questions_list:
        st.divider()
        st.markdown("### 📝 Practice & Live AI Evaluation")

        questions = st.session_state.questions_list
        options = [f"Q{i+1}: {q[:80]}..." if len(q) > 80 else f"Q{i+1}: {q}" for i, q in enumerate(questions)]

        selected_idx = st.selectbox(
            "Select Question to Practice:",
            range(len(questions)),
            format_func=lambda idx: options[idx]
        )

        current_question = questions[selected_idx]

        st.markdown(f"**Full Question:**")
        st.info(f"💡 {current_question}")

        answer_key = f"answer_input_{selected_idx}"
        user_answer = st.text_area(
            "Your Answer:",
            key=answer_key,
            height=140,
            placeholder="Type your technical response here. Include concepts, practical trade-offs, and examples..."
        )

        if st.button("🚀 Submit Answer for AI Evaluation", key=f"submit_{selected_idx}"):
            if not user_answer or not user_answer.strip():
                st.warning("Please enter your answer before submitting for evaluation.")
            else:
                with st.spinner("Evaluating your response with AI..."):
                    try:
                        eval_resp = requests.post(
                            f"{backend_url}/evaluate/",
                            json={
                                "question": current_question,
                                "answer": user_answer
                            },
                            timeout=45
                        )
                        if eval_resp.status_code == 200:
                            eval_data = eval_resp.json()
                            evaluation_result = eval_data.get("evaluation", "")

                            # Initialize evaluation history if needed
                            if "evaluation_history" not in st.session_state:
                                st.session_state.evaluation_history = []

                            record = {
                                "question": current_question,
                                "answer": user_answer,
                                "evaluation": evaluation_result
                            }
                            st.session_state.evaluation_history.append(
                                f"Question: {current_question}\nAnswer: {user_answer}\n\nEvaluation:\n{evaluation_result}"
                            )

                            st.session_state[f"last_eval_{selected_idx}"] = evaluation_result
                            st.success("✅ Evaluation complete!")
                        else:
                            st.error(f"Evaluation failed. Backend returned code {eval_resp.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error to backend: {e}")

        # Display result for current question if evaluated
        if f"last_eval_{selected_idx}" in st.session_state:
            st.markdown("#### 🎯 AI Evaluation & Feedback")
            st.markdown(f'<div class="glass">{st.session_state[f"last_eval_{selected_idx}"]}</div>', unsafe_allow_html=True)

        # Show all practice questions reference
        with st.expander("👁️ View All Generated Questions"):
            for i, q in enumerate(questions, 1):
                st.markdown(f"**{i}.** {q}")
