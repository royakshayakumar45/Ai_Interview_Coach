import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# ===============================
# HELPER FUNCTIONS
# ===============================

def generate_skill_feedback(conf, filler):
    feedback = []

    if conf < 50:
        feedback.append("Your confidence is low. Practice speaking daily and record yourself.")
    elif conf < 75:
        feedback.append("Your confidence is moderate. Improve clarity and structure.")
    else:
        feedback.append("Excellent confidence. Maintain consistency.")

    if filler > 5:
        feedback.append("High filler word usage detected. Practice pausing instead of using fillers.")
    else:
        feedback.append("Good control over filler words.")

    return feedback


def generate_improvement_plan(conf, filler):
    plan = []

    if conf < 60:
        plan.append("Practice mock interviews daily (10–15 mins)")
        plan.append("Record and review your answers")
        plan.append("Focus on speaking slowly")

    if filler > 5:
        plan.append("Avoid words like 'um', 'uh', 'like'")
        plan.append("Take pauses instead of fillers")

    plan.append("Use STAR method for HR questions")
    plan.append("Prepare 2–3 strong project explanations")

    return plan


def detect_strengths(df):
    strengths = []

    if df["confidence"].mean() > 75:
        strengths.append("Strong communication skills")

    if df["filler_count"].mean() < 3:
        strengths.append("Minimal filler word usage")

    if "technical_score" in df.columns:
        if df["technical_score"].mean() > 70:
            strengths.append("Good technical knowledge")

    return strengths


def detect_weaknesses(df):
    weaknesses = []

    if df["confidence"].mean() < 60:
        weaknesses.append("Low confidence")

    if df["filler_count"].mean() > 5:
        weaknesses.append("High filler word usage")

    if "technical_score" in df.columns:
        if df["technical_score"].mean() < 60:
            weaknesses.append("Weak technical knowledge")

    return weaknesses


def generate_daily_tasks():
    tasks = [
        "Practice 3 interview questions",
        "Record 1 answer and analyze it",
        "Revise 1 technical concept",
        "Practice speaking without fillers",
        "Explain one project clearly",
        "Mock interview with friend or AI",
        "Improve body language in mirror"
    ]
    return random.sample(tasks, 3)


# ===============================
# MAIN FUNCTION
# ===============================

def show_suggestions(conn, user):

    st.title("🤖 AI Coach Suggestions (Advanced)")

    # ===============================
    # LOAD DATA
    # ===============================

    df = pd.read_sql_query(
        "SELECT * FROM results WHERE username=?",
        conn,
        params=(user,)
    )

    # ===============================
    # NO DATA CASE
    # ===============================

    if df.empty:
        st.warning("No interview data available.")
        return

    # ===============================
    # BASIC METRICS
    # ===============================

    avg_conf = df["confidence"].mean()
    avg_filler = df["filler_count"].mean()

    col1, col2 = st.columns(2)

    col1.metric("Average Confidence", round(avg_conf, 2))
    col2.metric("Average Filler Words", round(avg_filler, 2))

    # ===============================
    # VISUAL ANALYTICS
    # ===============================

    st.subheader("📊 Performance Trends")

    if "date" in df.columns:
        df_sorted = df.sort_values("date")

        st.line_chart(df_sorted["confidence"])
        st.line_chart(df_sorted["filler_count"])

    # ===============================
    # FEEDBACK SECTION
    # ===============================

    st.subheader("🧠 AI Feedback")

    feedback = generate_skill_feedback(avg_conf, avg_filler)

    for f in feedback:
        st.info(f)

    # ===============================
    # STRENGTHS & WEAKNESSES
    # ===============================

    st.subheader("💪 Strengths & Weaknesses")

    strengths = detect_strengths(df)
    weaknesses = detect_weaknesses(df)

    col1, col2 = st.columns(2)

    with col1:
        st.success("Strengths")
        if strengths:
            for s in strengths:
                st.write("✔️ " + s)
        else:
            st.write("No strong strengths detected yet.")

    with col2:
        st.error("Weaknesses")
        if weaknesses:
            for w in weaknesses:
                st.write("❌ " + w)
        else:
            st.write("No major weaknesses.")

    # ===============================
    # IMPROVEMENT PLAN
    # ===============================

    st.subheader("🚀 Improvement Plan")

    plan = generate_improvement_plan(avg_conf, avg_filler)

    for p in plan:
        st.write("👉 " + p)

    # ===============================
    # DAILY TASK GENERATOR
    # ===============================

    st.subheader("📅 Daily Practice Tasks")

    if st.button("Generate Today's Tasks"):
        tasks = generate_daily_tasks()
        for t in tasks:
            st.write("✅ " + t)

    # ===============================
    # PERFORMANCE CATEGORY
    # ===============================

    st.subheader("📊 Performance Level")

    if avg_conf < 50:
        st.error("Beginner Level - Needs strong improvement")
    elif avg_conf < 75:
        st.warning("Intermediate Level - Keep improving")
    else:
        st.success("Advanced Level - Job Ready!")

    # ===============================
    # AI SMART INSIGHTS
    # ===============================

    st.subheader("🤖 Smart AI Insights")

    insights = []

    if avg_conf < 60:
        insights.append("You hesitate while speaking. Practice confidence-building exercises.")

    if avg_filler > 5:
        insights.append("Filler words indicate nervousness. Try pausing instead.")

    if "technical_score" in df.columns:
        if df["technical_score"].mean() < 60:
            insights.append("Revise core technical subjects.")

    insights.append("Use structured answers for better clarity.")
    insights.append("Give real-life examples to impress interviewers.")

    for i in insights:
        st.info(i)

    # ===============================
    # COMPARISON WITH IDEAL
    # ===============================

    st.subheader("📈 Comparison with Ideal Candidate")

    ideal_conf = 85
    ideal_filler = 2

    st.write(f"Your Confidence: {round(avg_conf,2)} / Ideal: {ideal_conf}")
    st.write(f"Your Filler Words: {round(avg_filler,2)} / Ideal: {ideal_filler}")

    # ===============================
    # PROGRESS BAR
    # ===============================

    st.subheader("📊 Overall Readiness")

    readiness = int((avg_conf / 100) * 70 + (max(0, (10 - avg_filler)) / 10) * 30)

    st.progress(readiness / 100)
    st.write(f"Readiness Score: {readiness}/100")

    # ===============================
    # EXPORT SUGGESTIONS
    # ===============================

    st.subheader("📄 Download Suggestions Report")

    report = "AI Suggestions Report\n\n"
    report += f"Confidence: {avg_conf}\n"
    report += f"Filler Words: {avg_filler}\n\n"

    report += "Improvement Plan:\n"
    for p in plan:
        report += "- " + p + "\n"

    st.download_button(
        "Download Report",
        report,
        file_name="suggestions_report.txt"
    )

    # ===============================
    # RESET MODULE DATA
    # ===============================

    st.subheader("🔄 Reset Suggestions Data")

    if st.button("Clear Suggestions Data"):

        try:
            conn.execute("DELETE FROM results WHERE username=?", (user,))
            conn.commit()
            st.success("Suggestions data cleared!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")