import streamlit as st
import pandas as pd
import plotly.express as px

def show_comparison(conn, user):

    st.title("📈 Performance Comparison")

    df = pd.read_sql_query(
        "SELECT * FROM results WHERE username=?",
        conn,
        params=(user,)
    )

    if len(df) >= 2:

        first_score = df.iloc[0]["confidence"]
        last_score = df.iloc[-1]["confidence"]

        improvement = last_score - first_score

        st.write("First Interview Score:", first_score)
        st.write("Latest Interview Score:", last_score)
        st.write("Improvement:", improvement)

        fig = px.bar(
            x=["First Interview", "Latest Interview"],
            y=[first_score, last_score],
            title="Confidence Growth"
        )

        st.plotly_chart(fig)

    else:
        st.warning("Need at least 2 interviews to compare.")