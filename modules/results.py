import streamlit as st
import pandas as pd

def show_results(conn, user):

    st.title("📄 My Interview History")

    df = pd.read_sql_query(
        "SELECT * FROM results WHERE username=?",
        conn,
        params=(user,)
    )

    if not df.empty:

        st.dataframe(df)

    else:

        st.warning("No interview history found.")