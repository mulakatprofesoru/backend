import secrets
from flask import Flask, jsonify
from api.user_connector import apiUsers
from api.question_connector import apiQuestion
from api.test_connector import apiTest
from api.chatgpt_connector import apiChatGPT
from flask_cors import CORS
from flask import request

from database import createApp
from database.init_question import fill_question_database
from database.init_test import fill_tests_database
from database.initialize_db import createDB
from database import db

app = createApp()  
createDB()
CORS(app)


secret_key = secrets.token_hex(16)
app.secret_key = secret_key

with app.app_context():
    fill_question_database(db)
    fill_tests_database(db)

app.register_blueprint(apiUsers)
app.register_blueprint(apiQuestion)
app.register_blueprint(apiTest)
app.register_blueprint(apiChatGPT)

@app.route("/")
def main_page():
    return jsonify({"succes": True, "message": "Main Page"})

if __name__ == "__main__":
    app.run(debug=True)