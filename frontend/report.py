import os
import requests
import streamlit as st


def show_report(backend_url: str = None):
    if backend_url is None:
        backend_url = os.getenv("BACKEND_URL", "https://interviewiq-ai-1-of73.onrender.com").strip("[]()'\" ").rstrip("/")

    st.markdown("## 📑 AI Candidate Assessment Report")
    st.write(
        "Synthesize your mock interview practice session into a comprehensive HR-ready "
        "performance assessment report detailing scores, strengths, and recommendations."
    )

    if "evaluation_history" not in st.session_state or not st.session_state.evaluation_history:
        st.info("ℹ️ Complete and evaluate at least one question in the **Mock Interview** tab to generate your final assessment report.")
        return

    evaluation_count = len(st.session_state.evaluation_history)
    st.success(f"✅ Found {evaluation_count} evaluated question(s) ready for report compilation.")

    combined_evaluations = "\n\n---\n\n".join(st.session_state.evaluation_history)

    if st.button("📊 Compile & Generate Final Report"):
        with st.spinner("Compiling candidate performance report with AI..."):
            try:
                response = requests.post(
                    f"{backend_url}/report/",
                    json={"evaluation": combined_evaluations},
                    timeout=60
                )
                if response.status_code == 200:
                    report_text = response.json().get("report", "")
                    st.session_state.final_report = report_text
                    st.success("🎉 Report generated successfully!")
                else:
                    st.error(f"Failed to generate report. Server returned code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to backend at `{backend_url}`: {e}")

    if "final_report" in st.session_state and st.session_state.final_report:
        report_content = st.session_state.final_report

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(report_content)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Report (.md)",
                data=report_content,
                file_name="InterviewIQ_Candidate_Report.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📄 Download Report (.txt)",
                data=report_content,
                file_name="InterviewIQ_Candidate_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
