from konlpy.tag import Okt
from ..utils.search import Search
from library.fileHandler import Pickle
from library.extract import Extract

from ..utils.llm import Chain
from ..utils.prompt import create_prompt_template
okt = Okt()

class ChatbotService:
    def __init__(self) -> None:
        pass

    def get_bm25_answers(question, dataset):
        file_path = f'/Users/user/Python/bm25_bot/assets/{dataset}'
        p = Pickle(file_path)
        pkl_file = p.read_pkl()
        tokens = [v['normalized'] for v in pkl_file]

        question_token = Extract.tokenizer(question)

        top_idx, score = Search.tf_idf(question_token, tokens)
        answer_list = [{'content': pkl_file[idx]['content'], 'source': pkl_file[idx]['source'], 'score': score[idx], 'pages': pkl_file[idx]['pages']} for idx in top_idx]

        return answer_list

    def get_qdrant_answers(dataset, question):
        return Search.similaritySearch(dataset, question)

    def doc_to_object(docs, dataset):
        arr = []
        for doc in docs:
            arr.append({
                "content" : doc[0].page_content.replace('\n', ' '),
                "source" : doc[0].metadata['source'].split('/')[-1],
                "pages" : str(doc[0].metadata['page']) if dataset == 'ctd_paged' else str(doc[0].metadata['pages']),
                "score" : str(doc[1])
            })
        return arr

    def chatWithLLM(bm25_answer_list, qdrant_answer_list, question):
        try:
            chat_prompt = create_prompt_template()
            info = Extract.make_pure_info(bm25_answer_list, qdrant_answer_list)

            return Chain.create(chat_prompt, info, question)
        except Exception as e:
            raise e