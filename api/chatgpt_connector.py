from flask import Flask, jsonify, Blueprint, request
from helper.chatgpt_connection_helper import ChatGPTHelper

apiChatGPT = Blueprint("apiChatGPT", __name__, url_prefix="/api/chatgpt")
__chatgpt_helper = ChatGPTHelper()


@apiChatGPT.route("/hint", methods=["POST"])
def get_hint():
    try:
        question = request.form.get("question")
        hint = __chatgpt_helper.get_hint_from_chatgpt(question=question)
        return jsonify({"success": True, "message": hint})

    except Exception as e:
        print("ERROR in questions: ", e)
        return jsonify({"success": False, "message": "There is an error..."})