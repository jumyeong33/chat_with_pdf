from constant import reqeust_endpoint
from handler.requestHandler import RequestHelper as req

class Router:
    """Chatbot"""
    def get_chatbot_answer(json) : return req.get(req, endpoint=reqeust_endpoint["getChatbotAnswer"], json=json)

    """PDF"""
    def extract_pdf(file, data) : return req.post(req, endpoint=reqeust_endpoint["extractPdf"], files=file, data=data)
    def create_pdf(file, data) : return req.post(req, endpoint=reqeust_endpoint["createPdf"], files=file, data=data)

    """Feedback"""
    def create_feedback(json) : return req.post(req, endpoint=reqeust_endpoint["createFeedback"], json=json)
    def update_feedback(json) : return req.patch(req, endpoint=reqeust_endpoint["updateFeeback"], json=json)