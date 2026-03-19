import streamlit as st
import pandas as pd
import plotly.express as px

def show_analytics(conn, user):

    st.title("📊 Analytics")

    df = pd.read_sql_query(
        "SELECT * FROM results WHERE username=?",
        conn,
        params=(user,)
    )

    if not df.empty:

        fig = px.line(df, x="date", y="confidence")

        st.plotly_chart(fig)

    else:

        st.warning("No Data")