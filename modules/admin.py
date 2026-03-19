import streamlit as st
import pandas as pd
import plotly.express as px

def show_admin(conn, role):

    if role == "admin":

        st.markdown("## 👑 Admin Dashboard (PRO)")

        # ===============================
        # LOAD DATA
        # ===============================
        users_df = pd.read_sql_query("SELECT * FROM users", conn)
        results_df = pd.read_sql_query("SELECT * FROM results", conn)

        # ===============================
        # KPI METRICS
        # ===============================
        st.subheader("📊 Platform Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("👥 Total Users", len(users_df))
        col2.metric("🎤 Total Interviews", len(results_df))

        if not results_df.empty:
            avg_conf = round(results_df["confidence"].mean(), 2)
        else:
            avg_conf = 0

        col3.metric("🔥 Avg Confidence", avg_conf)

        st.markdown("---")

        # ===============================
        # USER SEARCH / FILTER
        # ===============================
        st.subheader("🔍 Search Users")

        search = st.text_input("Search by Email")

        if search:
            filtered_users = users_df[users_df["email"].str.contains(search, case=False)]
        else:
            filtered_users = users_df

        st.dataframe(filtered_users, use_container_width=True)

        # ===============================
        # DELETE USER
        # ===============================
        st.subheader("❌ Delete User")

        if not users_df.empty:
            selected_user = st.selectbox("Select User", users_df["email"])

            if st.button("Delete User"):
                try:
                    conn.execute("DELETE FROM users WHERE email=?", (selected_user,))
                    conn.commit()
                    st.success("User Deleted Successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")

        # ===============================
        # INTERVIEW RECORDS
        # ===============================
        st.subheader("📋 Interview Records")

        st.dataframe(results_df, use_container_width=True)

        # ===============================
        # DOWNLOAD DATA
        # ===============================
        st.subheader("⬇️ Download Reports")

        csv_users = users_df.to_csv(index=False).encode("utf-8")
        csv_results = results_df.to_csv(index=False).encode("utf-8")

        col1, col2 = st.columns(2)

        col1.download_button(
            "Download Users CSV",
            csv_users,
            "users.csv",
            "text/csv"
        )

        col2.download_button(
            "Download Results CSV",
            csv_results,
            "results.csv",
            "text/csv"
        )

        st.markdown("---")

        # ===============================
        # CHART ANALYTICS
        # ===============================
        st.subheader("📈 Analytics Dashboard")

        if not results_df.empty:

            # Confidence Trend
            fig1 = px.histogram(
                results_df,
                x="confidence",
                title="Confidence Distribution"
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Filler Words Chart
            fig2 = px.bar(
                results_df,
                x="username",
                y="filler_count",
                title="Filler Words by User"
            )
            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("No analytics data available")

        st.markdown("---")

        # ===============================
        # USER ACTIVITY INSIGHTS
        # ===============================
        st.subheader("🧠 Insights")

        if not results_df.empty:

            high_performers = results_df[results_df["confidence"] > 80]

            st.success(f"High Performers: {len(high_performers)} users")

            low_performers = results_df[results_df["confidence"] < 50]

            st.warning(f"Needs Improvement: {len(low_performers)} users")

        else:
            st.info("No insights available")

        st.markdown("---")

        # ===============================
        # ADMIN CONTROL PANEL
        # ===============================
        st.subheader("⚙️ Admin Controls")

        if st.button("🧹 Clear All Interview Data"):

            try:
                conn.execute("DELETE FROM results")
                conn.commit()
                st.success("All Interview Data Cleared")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🧹 Clear All Users"):

            try:
                conn.execute("DELETE FROM users")
                conn.commit()
                st.success("All Users Deleted")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    else:

        st.error("🚫 Access Denied! Admin Only.")