bm25DatasetMapping = {
    'Page' : 'CTD_bm25.pkl',
    'Character' : 'CTD_bm25.pkl'
}
qdrantDatasetMapping = {
    'Page' : 'ctd_paged',
    'Character' : 'ctd_test'
}

base_url = "http://localhost:5000"

reqeust_endpoint = {
    # Chatbot
    "getChatbotAnswer" : '/chatbot/get',

    # PDF
    "extractPdf" : '/pdf/extract',
    "createPdf" : '/pdf/create',

    #Feedback
    "createFeedback" :'/feedback',
    "updateFeeback" : '/feedback/update',
}