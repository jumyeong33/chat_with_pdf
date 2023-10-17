from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("./firebaseKey.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    from .controller.chatbot import chatbotAPI
    from .controller.pdf import pdfAPI
    from .controller.feedback import feedbackAPI

    app.register_blueprint(chatbotAPI, url_prefix='/chatbot')
    app.register_blueprint(pdfAPI, url_prefix='/pdf')
    app.register_blueprint(feedbackAPI, url_prefix='/feedback')

    return app