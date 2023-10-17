from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

from api.utils.Document import Document
from konlpy.tag import Okt

import re
okt = Okt()

def extract_and_remove_pattern(text, pattern):
    matches = re.findall(pattern, text)
    new_text = re.sub(pattern, '', text)
    return matches, new_text

def remove_pattern(content):
    modified_content = content

    patterns = [
        r'MFDS/MaPP 5210.07B',
        r'첨단바이오의약품 시험방법 및 검증시험 검토 의뢰절차',
        r'(민 원 인 안 내 서)',
        r'Rev. 2'
    ]
    for p in patterns :
        _, new_test = extract_and_remove_pattern(modified_content, p)
        modified_content = new_test
    return modified_content

def create_doc_logic(content, documents, idx) :
    pattern_1 = r'-\s\d+\s-'
    pages, modified_content = extract_and_remove_pattern(content, pattern_1)

    if len(pages) > 0:
        page = ','.join(pages)
    else:
        if(idx == 0):
            page = idx
        else:
            ex_page = documents[idx -1].metadata['pages']
            page = idx if type(ex_page) is int else ex_page
    return modified_content, page

class Extract:
    def __init__(self) -> None:
        pass

    def extract_document_by_langchain(file):
        loader = PyPDFLoader(file)
        documents = loader.load()

        return documents

    def splicing(documents, idx):
        text = ""
        for d in documents[:idx]:
            text = text + d.page_content
        return text

    def normalize(texts):
        pattern = r'\s{2,}'
        pattern2 = r'\s+\.'
        for t in texts:
            t.page_content = t.page_content.replace("\n", " ")
            t.page_content = re.sub(pattern, " ", t.page_content)
            t.page_content = re.sub(pattern2, '.', t.page_content)

        return texts
    ## step 2 : split text document as openai embedding size(piece)

    def textSplitter(text):
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1200,
        chunk_overlap=0,
        )
        pieces = text_splitter.split_text(text)
        return pieces

    def docSplitter(doc):
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1800,
        chunk_overlap=0,
        )
        pieces = text_splitter.split_documents(doc)
        return pieces

    # slice unnecessary elements from docs
    def slice_docs(start_page, end_page, array) :
        leftover_array = array[:start_page - 1] + array[end_page:]
        return leftover_array


    def create_doc_instance(content, documents, idx, source):
        modified_content, page = create_doc_logic(content, documents, idx)

        return Document(
            page_content = modified_content,
            metadata = {'source' : source, 'pages' : page}
        )

    def over_under_docs(docs):
        under_docs = [doc for doc in docs if len(doc.page_content) <= 2000]
        over_docs = [doc for doc in docs if len(doc.page_content) > 2000]

        return over_docs, under_docs

    def tokenizer(sentence):
        res = okt.morphs(sentence, norm=False, stem=True)
        return res

    def make_pure_info(answer_from_bm25, answer_from_qdrant):
        search = ''
        search = answer_from_bm25[0]['content'] + '\n\n'
        for a in answer_from_qdrant:
            search = search + a[0].page_content + "\n\n"
        return search
