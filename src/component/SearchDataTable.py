import streamlit as st
import pandas as pd

class TableMaker:
    def bm25_table(answer_list):
        st.write(pd.DataFrame({
            'contents': [a['content'] for a in answer_list],
            'source': [a['source'] for a in answer_list],
            'score' : [a['score'] for a in answer_list],
            'pages' : [a['pages'] for a in answer_list]
        }))

    def qdrant_table(answer_list):
        st.write(pd.DataFrame({
            '내용': [data["content"] for data in answer_list],
            '파일': [data['source'] for data in answer_list],
            '페이지' : [data["pages"] for data in answer_list],
            '점수' : [data["score"] for data in answer_list]
        }))
