from langchain.vectorstores import Qdrant
from config import qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from konlpy.tag import Okt
from dotenv import load_dotenv
from library.fileHandler import Pickle

import os

okt = Okt()
class Embedding:

    def __init__(self) -> None:
        pass

    def get_vectorstore(index_name):
        load_dotenv()
        embeddings = OpenAIEmbeddings()
        client = qdrant()
        vectorstore = Qdrant(
            client=client,
            collection_name=index_name,
            embeddings=embeddings,
        )
        return vectorstore

    def bm25(documents):
        file_path = '/Users/user/Python/normalize/assets/CTD_bm25.pkl'
        p = Pickle(file_path)
        # Read existing file
        pkl_file = p.read_pkl()
        # Add new document to existing file
        pkl_file.extend(documents)
        # Write to existing file
        p.write_pkl(pkl_file)