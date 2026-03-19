import streamlit as st
from PyPDF2 import PdfReader
from ml_models.resume_model import resume_score
import plotly.express as px

def show_resume():

    st.title("📄 Resume Analyzer")

    file = st.file_uploader("Upload Resume", type=["pdf"])

    if file:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        # ❌ Removed Resume Score display (as instructed)

        words = text.split()
        word_count = len(words)

        st.subheader("📊 Resume Statistics")

        col1, col2 = st.columns(2)

        col1.metric("Total Words", word_count)
        col2.metric("Estimated Pages", round(word_count / 250, 2))

        # -------------------- SKILL DETECTION --------------------

        skills = [
            "python","java","machine learning","deep learning",
            "ai","data science","sql","excel","power bi",
            "tensorflow","pytorch","flask","django"
        ]

        detected_skills = []

        for skill in skills:
            if skill in text.lower():
                detected_skills.append(skill)

        st.subheader("🧠 Detected Skills")

        if detected_skills:
            st.success(", ".join(detected_skills))
        else:
            st.warning("No major skills detected")

        # -------------------- ATS SCORE --------------------

        ats_keywords = [
            "project","experience","internship",
            "leadership","team","communication",
            "analysis","problem solving"
        ]

        ats_count = 0

        for word in ats_keywords:
            if word in text.lower():
                ats_count += 1

        ats_score = int((ats_count / len(ats_keywords)) * 100)

        st.subheader("🎯 ATS Match Score")

        st.metric("ATS Score", ats_score)
        st.progress(min(ats_score/100,1.0))

        # -------------------- KEYWORD DENSITY --------------------

        st.subheader("📈 Keyword Density Analysis")

        keyword_freq = {}

        for word in words:
            word = word.lower()
            if word in skills:
                keyword_freq[word] = keyword_freq.get(word, 0) + 1

        if keyword_freq:
            fig = px.bar(
                x=list(keyword_freq.keys()),
                y=list(keyword_freq.values()),
                title="Skill Frequency in Resume"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No keyword frequency data available")

        # -------------------- EXPERIENCE LEVEL ESTIMATION --------------------

        st.subheader("🧑‍💼 Experience Level Estimation")

        if "intern" in text.lower():
            level = "Fresher / Intern"
        elif "project" in text.lower() and "experience" not in text.lower():
            level = "Entry Level"
        elif "experience" in text.lower():
            level = "Experienced"
        else:
            level = "Unknown"

        st.success(f"Detected Level: {level}")

        # -------------------- AI SUGGESTIONS --------------------

        st.subheader("🤖 AI Resume Suggestions")

        suggestions = []

        if word_count < 200:
            suggestions.append("Increase resume content. Add more projects and details.")

        if not detected_skills:
            suggestions.append("Add technical skills to improve ATS performance.")

        if ats_score < 50:
            suggestions.append("Use more ATS-friendly keywords like project, leadership, communication.")

        if "objective" not in text.lower():
            suggestions.append("Add a career objective section.")

        if "project" not in text.lower():
            suggestions.append("Include project experience.")

        if suggestions:
            for s in suggestions:
                st.warning(s)
        else:
            st.success("Your resume looks strong!")

        # -------------------- SECTION CHECK --------------------

        st.subheader("📂 Resume Section Check")

        sections = ["education", "experience", "skills", "projects", "certification"]

        found_sections = []

        for sec in sections:
            if sec in text.lower():
                found_sections.append(sec)

        st.write("Sections Found:", ", ".join(found_sections) if found_sections else "None")

        missing_sections = list(set(sections) - set(found_sections))

        if missing_sections:
            st.error("Missing Sections: " + ", ".join(missing_sections))
        else:
            st.success("All important sections are present ✅")

        # -------------------- DOWNLOAD REPORT --------------------

        st.subheader("📄 Download Report")

        report = f"""
Resume Analysis Report

Word Count: {word_count}
ATS Score: {ats_score}
Detected Skills: {detected_skills}
Experience Level: {level}
Missing Sections: {missing_sections}
Suggestions: {suggestions}
"""

        st.download_button(
            "Download Report",
            report,
            file_name="resume_analysis.txt"
        )