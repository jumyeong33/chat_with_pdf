import uuid
from flask import Blueprint, request, jsonify, abort
from firebase_admin import firestore

db = firestore.client()
feedback_ref = db.collection('feedback')

feedbackAPI = Blueprint('feedbackAPI', __name__)

@feedbackAPI.route('/', methods=['POST'])
def create():
    try:
        id = uuid.uuid4()
        json = request.json
        feedback_ref.document(id.hex).set(json)
        return jsonify({"ok": True, "data": {"id" : id.hex}})
    except Exception as e:
        return jsonify({"ok": False, "error" : str(e)})

@feedbackAPI.route('/update', methods=['PATCH'])
def update():
    try:
        data = request.get_json()
        doc_ref = db.collection('feedback').document(data["id"])
        doc_ref.update({ "quality": data["quality"] })

        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})