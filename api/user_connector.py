from flask import jsonify, Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import Question, User
import json

apiUsers = Blueprint("apiUser", __name__, url_prefix="/api/users")
__globalEmail = None

@apiUsers.route("/")
def users():
    try:
        allUsers = User.get_all_users()

        users = []

        for user in allUsers:
            users.append(
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "general_score": user.general_score
                }
            )

        return jsonify({"succes": True, "data": users, "count": len(users)})

    except Exception as e:
        print("ERROR in users: ", e)
        return jsonify({"success": False, "message": "There is an error..."})


@apiUsers.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def user(id):
    try:
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        if request.method == "GET":
            userObj = {
                "user id": user.user_id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "user general score": user.general_score
            }
            return jsonify({"success": True, "data": userObj})
        # ----------------------------------------------------------------------
        elif request.method == "DELETE":
            User.delete_user(id)
            return jsonify({"success": True, "message": "User deleted"})
        # ----------------------------------------------------------------------
        elif request.method == "PUT":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            general_score = request.form.get("general_score")

            if username == None:
                username = user.username

            if email == None:
                email = user.email

            if password == None:
                    password = user.password
                    
            if general_score == None:
                    general_score = user.general_score

            hashed_password = generate_password_hash(password)

            User.update_user(id, username, email, hashed_password, general_score)

            return jsonify({"success": True, "message": "User updated"})
        # ----------------------------------------------------------------------
    except Exception as e:
        return jsonify({"success": False, "message": "There is an error..."})


@apiUsers.route("/addUser", methods=["POST"])
def addUser():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        
        index = email.index('@')
        username = email[:index]

        if username == None or email == None or password == None:
            return jsonify({"success": False, "message": "Missing fields"})

        hashed_password = generate_password_hash(password)

        User.add_user(username, email, hashed_password)

        return jsonify({"success": True, "message": "User added successfully.."})
    except Exception as e:
        print("ERROR in addUser: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/isUserExist", methods=["POST"])
def isUserExist():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email == None or password == None:
            return jsonify({"success": False, "message": "Missing fields"})
        
        user = User.get_user_by_email(email)
        
        hashed_password = user.password
        
        if check_password_hash(hashed_password, password):
            return jsonify({"success": True, "message": "Successfully logged in"})
        else:
            return jsonify({"success": False, "message": "Wrong password or email."})
        
        
    except Exception as e:
        print("ERROR in isUserExist: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/login", methods=["POST"])
def login():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email == None or password == None:
            return jsonify({"success": False, "message": "Missing fields"})
        
        global __globalEmail
        __globalEmail = email
        
        return jsonify({"success": True, "message": "Successfully logged in"})
        
    except Exception as e:
        print("ERROR in login: ", e)
        
        return jsonify({"success": False, "message": "There is an error"})
    
    
@apiUsers.route("/logout", methods=["POST"])
def logout():
    try:      
        global __globalEmail
        if __globalEmail == None:
            return jsonify({"success": False, "message": "Not logged in"})
        
        __globalEmail = None   
        return jsonify({"success": True, "message": "Successfully logged out"})       
        
    except Exception as e:
        print("ERROR in logout: ", e)
        return jsonify({"success": False, "message": "There is an error"})

@apiUsers.route("/addTrainingHistory", methods=["POST"])
def addTrainingHistory():
    try:
        global __globalEmail
        if __globalEmail == None:
            return jsonify({"success": False, "message": "Not logged in"})
        
        user = User.get_user_by_email(__globalEmail)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        question_id = request.form.get("question_id")
        answer = request.form.get("answer")
        
        if question_id == None or answer == None:
            return jsonify({"success": False, "message": "Missing fields"})

        User.add_training_history_by_id(user.user_id, question_id, answer)

        return jsonify({"success": True, "message": "History added successfully.."})
        
    except Exception as e:
        print("ERROR in addTrainingHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/getTrainingHistory", methods=["GET"])
def getTrainingHistory():
    try:
        global __globalEmail
        if __globalEmail == None:
            return jsonify({"success": False, "message": "Not logged in"})
        
        user = User.get_user_by_email(__globalEmail)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})
              
        history = User.get_training_history_by_id(user.user_id)
        
        if history is None:
            return jsonify({"success": False, "message": "Training history not found"})
        
        historyObj = []
        for record in history:
            question = Question.get_question_by_id(record.question_id)
            historyObj.append({
                "user_id": record.user_id,
                "question": question.question,
                "user_answer" : record.answer,
                "correct_answer": question.answer_one
            })

        return jsonify({"success": True, "data": historyObj, "count": len(historyObj)})
        
    except Exception as e:
        print("ERROR in getTrainingHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/addTestHistory", methods=["POST"])
def addTestHistory():
    try:
        global __globalEmail
        if __globalEmail == None:
            return jsonify({"success": False, "message": "Not logged in"})
        
        user = User.get_user_by_email(__globalEmail)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        test_id = request.form.get("test_id")
        
        if test_id == None:
            return jsonify({"success": False, "message": "Missing fields"})

        test_history_id = User.add_test_history_by_id(user.user_id, test_id)

        questionAnswer = request.form.get("question_answer")
        questionAnswer = json.loads(questionAnswer)

        for answer in questionAnswer:
            User.add_test_question_history_by_id(user_id = user.user_id, test_history_id = test_history_id, question_id = answer["question_id"], answer=answer["answer"])

        return jsonify({"success": True, "message": "History added successfully.."})
        
    except Exception as e:
        print("ERROR in addTestHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/getTestHistory", methods=["GET"])
def getTestHistory():
    try:
        global __globalEmail
        if __globalEmail == None:
            return jsonify({"success": False, "message": "Not logged in"})
        
        user = User.get_user_by_email(__globalEmail)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})
              
        history = User.get_test_history_by_id(user.user_id)
        
        if history is None:
            return jsonify({"success": False, "message": "Test history not found"})
        
        historyObj = []
        for record in history:
            testQuestionHistory = record.test_question_history
            questions = []
            for testQuestionRecord in testQuestionHistory:
                question = Question.get_question_by_id(testQuestionRecord.question_id)
                questions.append({
                    "question": question.question,
                    "user_answer" : testQuestionRecord.answer,
                    "correct_answer": question.answer_one
                })
            historyObj.append({
                    "user_id": record.user_id,
                    "test_id": record.test_id,
                    "questions": questions
            })

        return jsonify({"success": True, "data": historyObj, "count": len(historyObj)})
        
    except Exception as e:
        print("ERROR in getTestHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})