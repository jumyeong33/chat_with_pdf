import streamlit as st
from router import Router as r

def feedback_checkbox():
    cols = st.empty()

    col1, col2, col3 = cols.columns(3)
    with col1:
        st.write("Please feedback to chatbot!")
    with col2:
        check_good = st.checkbox(":smile: Good")
    with col3:
        check_bad = st.checkbox(":angry: Bad")
    try:
        if check_good :
            st.session_state.feedback = "Good"
            r.update_feedback({"id": st.session_state.feedbackID, "quality" : st.session_state.feedback})
            cols.empty()
        if check_bad :
            st.session_state.feedback = "Bad"
            r.update_feedback({"id": st.session_state.feedbackID, "quality" : st.session_state.feedback})
            cols.empty()
    except Exception as e:
        print(e)
        st.error("Feedback upadte Failed..")