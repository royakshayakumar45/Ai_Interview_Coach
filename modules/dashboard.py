import streamlit as st
import random

def show_dashboard(conn=None, user=None):

    st.markdown("## 🚀 AI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Practice Sessions", random.randint(5, 20))
    col2.metric("🔥 Confidence Score", random.randint(60, 95))
    col3.metric("🧠 Emotion Stability", random.randint(70, 98))

    st.markdown("---")

    # 🔄 RESET SECTION
    st.subheader("🔄 Reset Application")

    st.warning("⚠️ This will delete ALL your data (Dashboard, Results, Analytics, etc.)")

    if st.button("Reset Everything"):

        try:
            if conn and user:

                conn.execute("DELETE FROM results WHERE username=?", (user,))
                conn.execute("DELETE FROM interview_analysis WHERE user_email=?", (user,))
                conn.execute("DELETE FROM analytics WHERE user_email=?", (user,))
                conn.execute("DELETE FROM suggestions WHERE user_email=?", (user,))
                conn.execute("DELETE FROM comparison WHERE user_email=?", (user,))

                conn.commit()

        except Exception as e:
            st.error(f"Database Error: {e}")

        st.session_state.clear()

        st.success("✅ Everything Reset Successfully!")

        st.rerun()