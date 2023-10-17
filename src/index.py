from konlpy.tag import Okt
from rank_bm25 import BM25Okapi
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import streamlit as st
import qdrant_client
import numpy as np
import json
import pandas as pd
import time
import os
import pickle

qdrantDatasetMapping = {
    'Page' : 'ctd_paged',
    'Character' : 'ctd_test'
}

bm25DatasetMapping = {
    'Page' : 'CTD_bm25.pkl',
    'Character' : 'CTD_bm25.pkl'
}

okt = Okt()
#get vector database
embeddings = OpenAIEmbeddings()

client = qdrant_client.QdrantClient(
    st.secrets["QDRANT_HOST"],
    api_key=st.secrets["QDRANT_API_KEY"]
    )

def getVectorstore(client, index_name):
    vectorstore = Qdrant(
    client=client,
    collection_name=index_name,
    embeddings=embeddings
    )
    st.session_state.vectorstore = vectorstore

#Create LLM instance
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"])

def tokenizer(sentence):
    res = okt.morphs(sentence, norm=False, stem=True)
    return res

def get_answer_object(question, file_name): 
    file_path = f'./assets/{file_name}'
    with open(file_path, 'rb') as pkl_file:
        list_of_dicts = pickle.load(pkl_file)
    tokens = [d['normalized'] for d in list_of_dicts]

    bm25 = BM25Okapi(tokens)
    score = bm25.get_scores(tokenizer(question))

    top_n = np.argsort(score)[::-1][:1]
    answer_list = [{'content': list_of_dicts[idx]['content'], 'source': list_of_dicts[idx]['source'], 'score': score[idx], 'pages': list_of_dicts[idx]['pages']} for idx in top_n]
    return answer_list

def similaritySearch(question):
    return st.session_state.vectorstore.similarity_search_with_score(query=question, k=2)

def make_pure_info(answer_from_bm25, answer_from_qdrant):
    search = ''
    search = answer_from_bm25[0]['content'] + '\n\n'
    for a in answer_from_qdrant:
        search = search + a[0].page_content + "\n\n"
    return search

def create_answer(question, info):
    system_template = """
    You are a helpful and kind AI model trained to assist with answering in Korean according to Ministry of Food and Drug Safety guideline and you must following rule :
    1. if you cannot find answer based on information from prompt that given by human, Just apologize. DO NOT TRY TO MAKE ANSWER.
    2. you must answer as Korean and markdown format.
    3. End the message with a random kind note
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "This is information :``` {information} ``` \n\n Based on the information, fully answer the following question : {question}'"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    res = llm(chat_prompt.format_prompt(information= info, question= question).to_messages())
    return res

def main():
    st.set_page_config(page_title="🤖 Quickstart App")
    st.title('🤖 BM25 & Qdrant App')

    with st.form('user_form'):
        dataset = st.selectbox(
        'select Dataset',
        ('Page', 'Character'))
        st.session_state.selectedDataset = dataset

        question = st.text_area('Ask Question:', placeholder= '⚠ It requires cost every question')
        submitted = st.form_submit_button('Submit')
    if submitted:
        if st.session_state.selectedDataset is None :
            return st.error('Select dataset')
        if len(question) < 1 :
            st.error('Required question!')
        with st.spinner("Processing.."):
            index_name = qdrantDatasetMapping[st.session_state.selectedDataset]
            json_file_name = bm25DatasetMapping[st.session_state.selectedDataset]
            getVectorstore(client, index_name)
            start_time = time.time()
            answer_from_bm25 = get_answer_object(question, json_file_name)
            answer_from_qdrant = similaritySearch(question)

            info = make_pure_info(answer_from_bm25, answer_from_qdrant)
            res = create_answer(question, info)

            st.info(res.content, icon="🤖")
            st.write('BM25')
            st.write(pd.DataFrame({
                'contents': [a['content'] for a in answer_from_bm25],
                'source': [a['source'] for a in answer_from_bm25],
                'score' : [a['score'] for a in answer_from_bm25],
                'pages' : [a['pages'] for a in answer_from_bm25]
            }))
            st.write('Qdrant')
            st.write(pd.DataFrame({
                '내용': [data[0].page_content.replace('\n', ' ') for data in answer_from_qdrant],
                '파일': [data[0].metadata['source'].split('/')[-1] for data in answer_from_qdrant],
                '페이지' : [str(data[0].metadata['page']) if index_name == 'ctd_paged' else str(data[0].metadata['pages']) for data in answer_from_qdrant],
                '점수' : [str(data[1]) for data in answer_from_qdrant]
            }))
            end_time = time.time()
            elapsed_time = end_time - start_time
        st.write(f"Process completed in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()
