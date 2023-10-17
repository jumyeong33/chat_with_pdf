from flask import Blueprint, request, jsonify
from ..service.pdfService import PdfService

pdfAPI = Blueprint('pdf', __name__)

@pdfAPI.route('/extract', methods=['POST'])
def extract():

    pdf = request.files['file_pdf']
    source = request.form['source']

    pieces = PdfService.extract_text(pdf)
    documents = PdfService.create_vectorstore_instances(pieces, source)
    result = PdfService.view_document(documents)

    return jsonify({"ok" : True, "extracted_text" : result})

@pdfAPI.route('/create', methods=['POST'])
def create():
    pdf = request.files['file_pdf']
    source = request.form['source']
    index_name = request.form['index_name']
    try:
        pieces = PdfService.extract_text(pdf)
        documents = PdfService.create_vectorstore_instances(pieces, source)
        test = PdfService.add_to_vectorstore(documents, index_name)

        return jsonify({"ok" : True})
    except Exception as e:
        return jsonify({"ok" : False, "error" : str(e)})


