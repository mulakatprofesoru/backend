import secrets
from flask import Flask, jsonify
from api.user_connector import apiUsers
from api.question_connector import apiQuestion
from api.test_connector import apiTest
from flask_cors import CORS
from flask import request

from database import createApp
from database.init_question import fill_question_database
from database.initialize_db import createDB
from database import db

app = createApp()  
createDB()
CORS(app)


secret_key = secrets.token_hex(16)
app.secret_key = secret_key

with app.app_context():
    fill_question_database(db)

app.register_blueprint(apiUsers)
app.register_blueprint(apiQuestion)
app.register_blueprint(apiTest)

# Mert Buraya Bir bak
# @app.route("/api/data")  
# def main_page():
#     return jsonify({"succes": True, "message": "Main Page"})

@app.route("/")
def main_page():
    return jsonify({"succes": True, "message": "Main Page"})

#Bu kisim question_connector icine tasinacak.
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print('Received data from React:', data)

    return jsonify({'message': 'Data received successfully'})

if __name__ == "__main__":
    app.run(debug=True)