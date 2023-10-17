from flask import Blueprint, request, jsonify, abort
from ..service.chatbotService import ChatbotService

chatbotAPI = Blueprint('chatbot', __name__)

@chatbotAPI.route('/get', methods=['GET'])
def getAnswer():
    try :
        data = request.get_json()
        bm25_answer_list = ChatbotService.get_bm25_answers(question=data['question'], dataset=data['bm25_dataset'])
        qdrant_answer_list = ChatbotService.get_qdrant_answers(question=data['question'], dataset=data['qdrant_dataset'])
        qdrant_answer_list_obj = ChatbotService.doc_to_object(qdrant_answer_list, dataset=data['qdrant_dataset'])
        result = ChatbotService.chatWithLLM(bm25_answer_list, qdrant_answer_list, data["question"])
        return jsonify({
            "ok" : True,
            "data" : {
                "answer" : result.content,
                "bm25_result" : bm25_answer_list,
                "qdrant_result" : qdrant_answer_list_obj
                }
            })
    except Exception as e :
        print(e)
        abort(400, description='Get Answer Failed')