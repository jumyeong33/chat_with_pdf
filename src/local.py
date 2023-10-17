
import streamlit as st
import time

import os
from component.SideBar import sideBar
from component.SearchDataTable import TableMaker
from component.FeedbackCheckbox import feedback_checkbox
from router import Router as r
from constant import bm25DatasetMapping, qdrantDatasetMapping
from handler.streamlitHandler import set_state, submit_disable, submit_enable

def main():
    st.set_page_config(page_title="🤖 Quickstart App")
    st.title('🤖 bm25 App')

    set_state()
    sideBar()
    with st.form('user_form'):
        dataset = st.selectbox(
        'select Dataset',
        ('Page', 'Character'))
        st.session_state.selectedDataset = dataset

        question = st.text_area('Ask Question:', placeholder= '⚠ It requires cost every question')
        submitted = st.form_submit_button('Submit', on_click=submit_disable, disabled=st.session_state.disabled)
    if submitted:
        if len(question) < 1 :
            submit_enable()
            return
        if st.session_state.selectedDataset is None :
            return st.error('Select dataset')
        
        with st.spinner("Processing.."):
            bm25_dataset = bm25DatasetMapping[st.session_state.selectedDataset]
            qdrant_dataset = qdrantDatasetMapping[st.session_state.selectedDataset]
            start_time = time.time()

            st.session_state.result = r.get_chatbot_answer({"question" : question, "bm25_dataset" : bm25_dataset, "qdrant_dataset" : qdrant_dataset})
            end_time = time.time()
            st.session_state.elapsed_time = end_time - start_time
            feedback_return = r.create_feedback({"question" : question, "answer": st.session_state.result["data"]["answer"]})
            st.session_state.feedbackID = feedback_return["data"]["id"]
    submit_enable()
    if "feedbackID" in st.session_state:
        feedback_checkbox()
    if 'result' in st.session_state :
        st.info(st.session_state.result["data"]["answer"], icon="🤖")
        st.write("BM25")

        TableMaker.bm25_table(st.session_state.result["data"]["bm25_result"])
        st.write("QDRANT")
        TableMaker.qdrant_table(st.session_state.result["data"]["qdrant_result"])

        st.write(f"Process completed in {st.session_state.elapsed_time:.2f} seconds.")
    
if __name__ == '__main__':
    main()
