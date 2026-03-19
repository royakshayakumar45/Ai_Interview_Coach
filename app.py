import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import sqlite3
import hashlib
from database.database import init_db

# ===============================
# ✅ ADD THIS (CSS LOAD)
# ===============================
def load_css():
    try:
        with open("static/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ===============================
# ✅ PREMIUM UI (ADDED)
# ===============================
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* HERO SECTION */
.hero {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* CARDS */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(15px);
    transition: 0.3s;
}

div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
}

/* BUTTON */
button {
    border-radius: 12px !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white !important;
}

/* INPUT */
input, textarea {
    border-radius: 10px !important;
}

/* ANIMATION */
.block-container {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# ===============================
# IMPORT MODULES
# ===============================

from modules.dashboard import show_dashboard
from modules.interview_analysis import show_interview_analysis
from modules.emotion_detection import show_emotion
from modules.resume_analyzer import show_resume
from modules.voice_coach import show_voice
from modules.analytics import show_analytics
from modules.comparison import show_comparison
from modules.suggestions import show_suggestions
from modules.report import show_report
from modules.results import show_results
from modules.admin import show_admin
from modules.logout import do_logout

from auth.login import login
from auth.register import register_user

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="AI Interview Coach PRO MAX",
    layout="wide"
)

# ===============================
# DATABASE
# ===============================

conn = init_db()

# ===============================
# SESSION
# ===============================

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

# ===============================
# LOGIN / REGISTER PAGE
# ===============================

if st.session_state.user is None:

    st.markdown("""
    <div class="hero">
        <h1>🚀 AI Interview Coach PRO</h1>
        <p>Practice • Analyze • Get Hired Faster</p>
    </div>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Interview Coach")

    option = st.radio("Choose", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Register":

        if st.button("Register"):

            result = register_user(conn, email, password)

            if result:
                st.success("Account Created")
            else:
                st.error("User already exists")

    if option == "Login":

        if st.button("Login"):

            user = login(conn, email, password)

            if user:
                st.session_state.user = user["email"]
                st.session_state.role = user["role"]
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ===============================
# MAIN DASHBOARD AREA
# ===============================

else:

    st.markdown(f"""
    <div class="hero">
        <h1>Welcome {st.session_state.user} 👋</h1>
        <p>Your AI Interview Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("AI Interview Coach")

    # ✅ DARK MODE TOGGLE
    theme = st.sidebar.toggle("🌙 Dark Mode", value=True)

    if not theme:
        st.markdown("""
        <style>
        body { background: #f1f5f9 !important; color: black !important; }
        </style>
        """, unsafe_allow_html=True)

    menu = st.sidebar.selectbox("Navigation", [

        "Dashboard",
        "Interview Analysis",
        "Face Emotion Detection",
        "Resume ATS Analyzer",
        "Voice AI Coach",
        "Analytics Dashboard",
        "Performance Comparison",
        "AI Coach Suggestions",
        "Generate Report",
        "My Results",
        "Admin Panel",
        "Reset App",  
        "Logout"

    ])

# ===============================
# ROUTING TO MODULES
# ===============================

    if menu == "Dashboard":
        show_dashboard(conn, st.session_state.user)

    elif menu == "Interview Analysis":
        show_interview_analysis(conn, st.session_state.user)

    elif menu == "Face Emotion Detection":
        show_emotion()

    elif menu == "Resume ATS Analyzer":
        show_resume()

    elif menu == "Voice AI Coach":
        show_voice()

    elif menu == "Analytics Dashboard":
        show_analytics(conn, st.session_state.user)

    elif menu == "Performance Comparison":
        show_comparison(conn, st.session_state.user)

    elif menu == "AI Coach Suggestions":
        show_suggestions(conn, st.session_state.user)

    elif menu == "Generate Report":
        show_report()

    elif menu == "My Results":
        show_results(conn, st.session_state.user)

    elif menu == "Admin Panel":

        # ✅ ORIGINAL ADMIN
        show_admin(conn, st.session_state.role)

        # ===============================
        # 🔥 ADVANCED ADMIN CONTROL (ADDED)
        # ===============================

        if st.session_state.role == "admin":

            st.subheader("⚙️ Advanced Admin Controls")

            col1, col2 = st.columns(2)

            # DELETE ALL USERS
            if col1.button("🗑 Delete All Users"):
                try:
                    conn.execute("DELETE FROM users")
                    conn.commit()
                    st.success("All users deleted")
                except Exception as e:
                    st.error(e)

            # DELETE ALL RESULTS
            if col2.button("🧹 Clear All Results"):
                try:
                    conn.execute("DELETE FROM results")
                    conn.commit()
                    st.success("All results cleared")
                except Exception as e:
                    st.error(e)

            # SYSTEM STATS
            st.subheader("📊 System Stats")

            try:
                total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
                total_results = conn.execute("SELECT COUNT(*) FROM results").fetchone()[0]

                st.metric("Total Users", total_users)
                st.metric("Total Interviews", total_results)

            except:
                st.warning("Stats not available")

            # DOWNLOAD DATABASE
            st.subheader("⬇ Backup Database")

            try:
                with open("database.db", "rb") as f:
                    st.download_button("Download DB", f, file_name="backup.db")
            except:
                st.warning("Database file not found")

        else:
            st.error("Admin access required")

    elif menu == "Reset App":

        st.title("Reset Application")

        st.warning("This will delete ALL your data (Dashboard, Results, Analytics, etc.)")

        if st.button("Confirm Full Reset"):

            user = st.session_state.user

            try:
                conn.execute("DELETE FROM interview_analysis WHERE user_email=?", (user,))
                conn.execute("DELETE FROM analytics WHERE user_email=?", (user,))
                conn.execute("DELETE FROM results WHERE user_email=?", (user,))
                conn.execute("DELETE FROM suggestions WHERE user_email=?", (user,))
                conn.execute("DELETE FROM comparison WHERE user_email=?", (user,))

                conn.commit()

            except Exception as e:
                st.error(f"Database Error: {e}")

            st.session_state.clear()

            st.success("✅ Everything Reset Successfully!")

            st.rerun()

    elif menu == "Logout":
        do_logout()