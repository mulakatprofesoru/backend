from flask import Flask, jsonify
from api.user_connector import apiUsers
from api.question_connector import apiQuestion
from flask_cors import CORS
from flask import request

from database import createApp
from database.initialize_db import createDB

app = createApp()  
createDB()
CORS(app)

app.register_blueprint(apiUsers)
app.register_blueprint(apiQuestion)

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

