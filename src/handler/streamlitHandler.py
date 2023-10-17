import streamlit as st

def submit_disable():
    st.session_state.disabled = True

def submit_enable():
    if "disabled" in st.session_state and st.session_state.disabled == True:
        st.session_state.disabled = False
        st.experimental_rerun()

def set_state():
    if "accessOk" not in st.session_state:
        st.session_state["accessOk"] = False
    if "checked" not in st.session_state:
        st.session_state["checked"] = False
    if "disabled" not in st.session_state:
        st.session_state["disabled"] = False