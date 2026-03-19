import streamlit as st

def do_logout():

    st.session_state.user = None
    st.session_state.role = None
    st.rerun()