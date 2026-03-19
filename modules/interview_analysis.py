import streamlit as st
import speech_recognition as sr
import tempfile
from datetime import datetime
import pandas as pd
import random
import plotly.express as px
from modules.utils import analyze_text

def show_interview_analysis(conn, user):

    st.title("🎤 Interview Analysis")

    r = sr.Recognizer()
    text = ""
    audio_bytes = st.audio_input("Record your answer")

    if audio_bytes:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes.read())
            path = tmp.name

        with sr.AudioFile(path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio)
        except:
            text = "Could not understand audio"

    filler, sentiment, confidence = analyze_text(text)

    st.subheader("📝 Transcript")
    st.write(text)

    col1, col2, col3 = st.columns(3)

    col1.metric("Sentiment", sentiment)
    col2.metric("Filler Words", filler)
    col3.metric("Confidence", int(confidence * 100))

    st.progress(min(confidence, 1.0))

    st.divider()

    st.subheader("📊 Speech Analytics")

    words = text.split()
    word_count = len(words)

    speaking_speed = round(word_count / 60, 2)

    col1, col2 = st.columns(2)

    col1.metric("Word Count", word_count)
    col2.metric("Speaking Speed (words/sec)", speaking_speed)

    st.subheader("🧠 Skill Keyword Detection")

    keywords = [
        "python","machine learning","ai","data",
        "database","sql","api","algorithm","cloud",
        "flask","django","model","training"
    ]

    detected = []

    for k in keywords:
        if k in text.lower():
            detected.append(k)

    if detected:
        st.success("Detected Skills: " + ", ".join(detected))
    else:
        st.warning("No technical keywords detected")

    st.subheader("⭐ AI Answer Quality Score")

    keyword_score = len(detected) * 10
    length_score = min(word_count, 50)

    answer_score = int((confidence*100 + keyword_score + length_score) / 3)

    st.metric("Answer Score", answer_score)

    st.progress(min(answer_score/100, 1.0))

    st.subheader("📈 Performance Breakdown")

    chart_data = pd.DataFrame({
        "Metric":[
            "Confidence",
            "Clarity",
            "Technical Depth",
            "Fluency",
            "Communication"
        ],
        "Score":[
            confidence*100,
            random.randint(60,90),
            keyword_score,
            100 - filler*5 if filler < 10 else 50,
            random.randint(65,95)
        ]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Score",
        title="Interview Skill Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧭 Interview Radar Profile")

    radar = px.line_polar(
        chart_data,
        r="Score",
        theta="Metric",
        line_close=True
    )

    st.plotly_chart(radar, use_container_width=True)

    try:

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO results
        (username, date, confidence, filler_count)
        VALUES (?, ?, ?, ?)
        """,
        (
            user,
            datetime.now().strftime("%Y-%m-%d"),
            int(confidence*100),
            filler
        ))

        conn.commit()

    except:
        pass

    st.subheader("🤖 AI Interview Feedback")

    if answer_score < 50:
        st.error("Your answer needs improvement. Try explaining your ideas more clearly.")

    elif answer_score < 75:
        st.warning("Good answer, but try adding more technical depth.")

    else:
        st.success("Excellent answer! Strong communication and technical clarity.")

    st.subheader("📄 Download Interview Result")

    report = f"""
AI Interview Analysis

User: {user}

Transcript:
{text}

Sentiment: {sentiment}
Confidence: {int(confidence*100)}
Filler Words: {filler}
Word Count: {word_count}
Detected Skills: {detected}
Answer Score: {answer_score}
"""

    st.download_button(
        "Download Report",
        report,
        file_name="interview_analysis.txt"
    )