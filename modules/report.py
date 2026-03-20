import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def show_report():

    st.title("📄 Generate Final Interview Report")

    if st.button("Generate Full PDF Report"):

        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate("final_report.pdf")

        story = []

        # -------------------- TITLE --------------------
        story.append(Paragraph("AI Interview Full Report", styles['Title']))
        story.append(Spacer(1, 20))

        user = st.session_state.get("user", "Unknown User")
        story.append(Paragraph(f"User: {user}", styles['Normal']))
        story.append(Spacer(1, 20))

        # ===============================
        # INTERVIEW ANALYSIS DATA
        # ===============================
        interview = st.session_state.get("interview_result", None)

        if interview:
            story.append(Paragraph("Interview Analysis", styles['Heading2']))
            story.append(Spacer(1, 10))

            story.append(Paragraph(f"Transcript: {interview.get('text','')}", styles['Normal']))
            story.append(Paragraph(f"Sentiment: {interview.get('sentiment','')}", styles['Normal']))
            story.append(Paragraph(f"Confidence: {interview.get('confidence','')}", styles['Normal']))
            story.append(Paragraph(f"Filler Words: {interview.get('filler','')}", styles['Normal']))
            story.append(Paragraph(f"Answer Score: {interview.get('score','')}", styles['Normal']))

            story.append(Spacer(1, 20))

        # ===============================
        # RESUME DATA
        # ===============================
        resume = st.session_state.get("resume_result", None)

        if resume:
            story.append(Paragraph("Resume Analysis", styles['Heading2']))
            story.append(Spacer(1, 10))

            story.append(Paragraph(f"Word Count: {resume.get('word_count','')}", styles['Normal']))
            story.append(Paragraph(f"ATS Score: {resume.get('ats_score','')}", styles['Normal']))
            story.append(Paragraph(f"Skills: {resume.get('skills','')}", styles['Normal']))
            story.append(Paragraph(f"Experience Level: {resume.get('level','')}", styles['Normal']))
            story.append(Paragraph(f"Missing Sections: {resume.get('missing_sections','')}", styles['Normal']))

            story.append(Spacer(1, 20))

        # ===============================
        # BUILD PDF
        # ===============================
        doc.build(story)

        # -------------------- DOWNLOAD --------------------
        with open("final_report.pdf", "rb") as f:
            st.download_button(
                "📥 Download Full Report",
                f,
                file_name="AI_Interview_Report.pdf"
            )

        st.success("✅ Full Report Generated Successfully!")
