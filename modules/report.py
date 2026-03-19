import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def show_report():

    st.title("Generate Interview Report")

    if st.button("Generate PDF"):

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate("report.pdf")

        story = []

        story.append(Paragraph("AI Interview Report", styles['Title']))
        story.append(Spacer(1, 20))
        story.append(Paragraph("User: " + st.session_state.user, styles['Normal']))

        doc.build(story)

        st.success("Report Generated")