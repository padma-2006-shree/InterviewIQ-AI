import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def show_report():

    st.markdown("## 📄 AI Interview Report")

    if "evaluation_history" not in st.session_state:

        st.info("Complete at least one interview question to generate a report.")

        return

    evaluation = "\n\n".join(st.session_state.evaluation_history)

    if st.button("📊 Generate Final Report"):

        with st.spinner("Generating report..."):

            response = requests.post(

                f"{BACKEND_URL}/report/",

                json={

                    "evaluation": evaluation

                }

            )

        if response.status_code == 200:

            report = response.json()["report"]

            st.success("Report Generated Successfully")

            st.markdown(report)

            st.download_button(

                "⬇ Download Report",

                report,

                file_name="Interview_Report.txt",

                mime="text/plain"

            )

        else:

            st.error(response.text)