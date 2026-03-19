import streamlit as st
import random
import time
import speech_recognition as sr
import pyttsx3

# ===============================
# AI RESPONSE (Fallback Logic)
# ===============================

def basic_ai_feedback(text):
    feedback = []

    if len(text.split()) < 20:
        feedback.append("Answer is too short. Try to elaborate more.")

    if "um" in text.lower() or "uh" in text.lower():
        feedback.append("Avoid filler words like 'um', 'uh'.")

    if "project" not in text.lower():
        feedback.append("Try to include real project examples.")

    if not feedback:
        feedback.append("Good answer! Keep improving structure.")

    return "\n".join(feedback)

# ===============================
# TEXT TO SPEECH
# ===============================

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ===============================
# SPEECH TO TEXT
# ===============================

def listen_voice():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
    except:
        return ""

# ===============================
# CONFIDENCE SCORING
# ===============================

def calculate_score(answer):
    score = 50

    if len(answer.split()) > 30:
        score += 20

    if any(word in answer.lower() for word in ["project", "experience", "team"]):
        score += 15

    if any(word in answer.lower() for word in ["python", "ai", "ml", "data"]):
        score += 10

    if "um" in answer.lower():
        score -= 10

    return max(0, min(score, 100))

# ===============================
# KEYWORD ANALYSIS
# ===============================

def keyword_analysis(answer):
    keywords = [
        "python", "ai", "ml", "data", "project",
        "team", "api", "cloud", "database", "algorithm"
    ]

    found = [k for k in keywords if k in answer.lower()]
    return found

# ===============================
# MAIN FUNCTION
# ===============================

def show_voice():

    st.title("🎤 Voice AI Coach (Advanced)")

    # ===============================
    # SESSION INIT
    # ===============================

    if "voice_history" not in st.session_state:
        st.session_state.voice_history = []

    if "voice_scores" not in st.session_state:
        st.session_state.voice_scores = []

    # ===============================
    # TIPS SECTION
    # ===============================

    tips = [
        "Speak slowly and clearly",
        "Avoid filler words like um/uh",
        "Use structured answers (Intro, Skills, Example)",
        "Explain projects with clarity",
        "Maintain confidence and eye contact",
        "Use technical keywords",
        "Keep answers concise but informative"
    ]

    st.info("💡 Tip: " + random.choice(tips))

    # ===============================
    # INPUT OPTIONS
    # ===============================

    col1, col2 = st.columns(2)

    voice_btn = col1.button("🎤 Start Speaking")
    text_input = col2.text_input("Or type your answer")

    user_answer = ""

    # ===============================
    # VOICE INPUT
    # ===============================

    if voice_btn:
        user_answer = listen_voice()
        if user_answer:
            st.success(f"You said: {user_answer}")

    # ===============================
    # TEXT INPUT
    # ===============================

    if text_input:
        user_answer = text_input

    # ===============================
    # PROCESS ANSWER
    # ===============================

    if user_answer:

        with st.spinner("Analyzing your answer..."):
            time.sleep(1)

        # Store history
        st.session_state.voice_history.append(user_answer)

        # ===============================
        # AI FEEDBACK
        # ===============================

        st.subheader("🤖 AI Feedback")

        feedback = basic_ai_feedback(user_answer)
        st.write(feedback)

        # ===============================
        # SCORE
        # ===============================

        score = calculate_score(user_answer)
        st.session_state.voice_scores.append(score)

        st.subheader("📊 Performance Score")
        st.metric("Score", score)
        st.progress(score / 100)

        if score < 60:
            st.error("Low confidence. Improve clarity and structure.")
        elif score < 80:
            st.warning("Good, but can improve with examples.")
        else:
            st.success("Excellent answer!")

        # ===============================
        # KEYWORD ANALYSIS
        # ===============================

        st.subheader("🧠 Keyword Analysis")

        found_keywords = keyword_analysis(user_answer)

        if found_keywords:
            st.success("Keywords Used: " + ", ".join(found_keywords))
        else:
            st.warning("No strong keywords detected")

        # ===============================
        # SPEAK FEEDBACK
        # ===============================

        if st.button("🔊 Hear Feedback"):
            speak_text(feedback)

    # ===============================
    # HISTORY
    # ===============================

    st.subheader("📝 Answer History")

    for i, ans in enumerate(st.session_state.voice_history[::-1]):
        st.markdown(f"**{i+1}.** {ans}")

    # ===============================
    # CONFIDENCE TRACKING
    # ===============================

    st.subheader("📈 Confidence Tracking")

    if st.session_state.voice_scores:
        avg_score = sum(st.session_state.voice_scores) / len(st.session_state.voice_scores)

        st.metric("Average Score", int(avg_score))

        if avg_score < 60:
            st.error("Overall performance is low")
        elif avg_score < 80:
            st.warning("Moderate performance")
        else:
            st.success("High confidence level!")

    # ===============================
    # MOCK QUESTIONS
    # ===============================

    st.subheader("🎯 Practice Questions")

    questions = [
        "Tell me about yourself",
        "Why should we hire you?",
        "Explain your project",
        "What are your strengths?",
        "Describe a challenge you faced"
    ]

    if st.button("Get Question"):
        q = random.choice(questions)
        st.info(q)

    # ===============================
    # RESET SECTION
    # ===============================

    st.subheader("🔄 Reset Voice Data")

    if st.button("Reset Voice Coach"):
        st.session_state.voice_history = []
        st.session_state.voice_scores = []
        st.success("Voice data reset successfully!")