# Chat with PDF

This project is prototype of chatting with PDF. Using `gpt-3.5-turbo ` from openAI to induce an answer. Currently data is based on **Ministry of Food and Drug Safety guideline**.

## Tech Stack

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white"> <img src="https://img.shields.io/badge/Qdrant-E40000?style=for-the-badge&logo=logoColor=white"> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white"> <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=Firebase&logoColor=white"> <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=OpenAI&logoColor=white">

## What this app can do?

### Question to PDF

<img src="https://github.com/jumyeong33/bm25_chatbot/assets/57386602/196e74ac-7392-4077-b1b5-ea5fff5036af" width="500" height="250">

Also saved qeustion/answer/satisfaction at firebase.

### Upload PDF to vectorstore

As mentioned, This project is based on Minnnistry of Food and Drug Safety Guideline that nomarized text is a bit customized it. Please check `./library/extract.py`

<img src="https://github.com/jumyeong33/bm25_chatbot/assets/57386602/cf6e5658-a854-4c9e-a962-c2140f2ad990" width="500" height="250">

## Tree

```sh
chatbot_with_pdf/
┣ .streamlit/
┃ ┗ config.toml
┣ api/                               --> Server
┃ ┣ controller/                      --> each API endpoint
┃ ┃ ┣ chatbot.py
┃ ┃ ┣ feedback.py
┃ ┃ ┗ pdf.py
┃ ┣ service/                         --> service logics
┃ ┃ ┣ chatbotService.py
┃ ┃ ┗ pdfService.py
┃ ┣ utils/                           --> useful function for service
┃ ┃ ┣ Document.py
┃ ┃ ┣ llm.py
┃ ┃ ┣ prompt.py
┃ ┃ ┗ search.py
┃ ┗ __init__.py                      --> create server app
┣ assets/
┃ ┣ CTD_bm25.pkl                     --> dataset by bm25
┣ library/                           --> for pdf handling
┃ ┣ embedding.py
┃ ┣ extract.py
┃ ┣ fileHandler.py
┃ ┗ transformText.py                 --> pdf spliting logic
┣ src/
┃ ┣ component/
┃ ┃ ┣ FeedbackCheckbox.py
┃ ┃ ┣ SearchDataTable.py
┃ ┃ ┗ SideBar.py
┃ ┣ handler/
┃ ┃ ┣ requestHandler.py
┃ ┃ ┗ streamlitHandler.py
┃ ┣ constant.py
┃ ┣ index.py                         --> for deploying (only main branch)
┃ ┣ local.py                         --> main script for running app(locally)
┃ ┗ router.py                        --> call API
┣ .env
┣ .gitignore
┣ README.md
┣ config.py                          --> vector database config
┣ packages.txt                       --> avoid an error from okt with streamlit
┣ requirements.txt
┗ server.py                          --> run server app
```

## Flow

![alt text](https://github.com/jumyeong33/bm25_chatbot/assets/57386602/8d4806b9-0805-4293-bf0a-c0f042eb73e0)

1. Splicing all texts of page as one string, then cut in 1000 ~ 1200 charater when a sentence ends. (If cannot find sentence end point, just cut at 1200)

2. Vectorize(OpenAI embedding model) each piece and save to vectorStore(Qdrant)

3. From user question, Use cosine similarity search get result as Top 2 and Top 1 result from bm25(TF-IDF).

4. LLM model makes answer by prompt based on result data.

## Run the app

before runninng the app make sure to set credential key and env file.

- make filebaseKey.json at root
- fill in .env file
- change path for using bm25 dataset

```python
# ./library/embdding.py
def bm25(documents):
        file_path = 'your_path/CTD_bm25.pkl'
```

Server

- install requiremennts from txt file then,

```sh
$ python3 run server.py
```

Streamlit app

```sh
$ cd src/
$ streamlit run local.py
```

## Usage

### Make this project as your taste

${\color{Red}NOTIFY}$

Currently only offer to making dataset at qdrant. Is not made bm25 dataset by uploading client side.

- Create your own vectordatabase collection.
  [How to create collection](https://colab.research.google.com/drive/1XzIg1Sup6C09T6CE-WwKd1sbJYffEboe?usp=sharing)
- Modify constant value which mapping to the collectionn

```python
# ./src/constant.py
qdrantDatasetMapping = {
    'Page' : 'your_collection',
    'Character' : 'your_collection'
}
```

- Delete exist CTD_bm25.pkl & Create BM25 dataset using `library/extract.py` and `embedding.py`

- Modify Prompt template

```python
# ./api/utils/prompt.py
def create_prompt_template():
    system_template = """ make your own bot """
    human_template = """ human side template """
```

## Reference

- [파동이봇 by Hongbi-kim](https://github.com/Hongbi-Kim/KAERI_BOT_beta)
- [Ask a Book Qustion](https://bennycheung.github.io/ask-a-book-questions-with-langchain-openai)
