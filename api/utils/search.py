from rank_bm25 import BM25Okapi
import numpy as np
from library.embedding import Embedding as e

class Search:
    def tf_idf(question_token, tokens):

        bm25 = BM25Okapi(tokens)
        score = bm25.get_scores(question_token)

        top_idx = np.argsort(score)[::-1][:1]
        return top_idx, score

    def similaritySearch(dataset, question):
        vectorstore = e.get_vectorstore(dataset)
        return vectorstore.similarity_search_with_score(query=question, k=2)