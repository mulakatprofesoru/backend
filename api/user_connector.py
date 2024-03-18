from flask import jsonify, Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User

apiUsers = Blueprint("apiUser", __name__, url_prefix="/api/users")


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
        
        print("Email: " + email)
        session["email"] = email
        
        print("login",session["email"])
        return jsonify({"success": True, "message": "Successfully logged in"})
        
    except Exception as e:
        print("ERROR in login: ", e)
        
        return jsonify({"success": False, "message": "There is an error"})
    
    
@apiUsers.route("/logout", methods=["POST"])
def logout():
    try:      
        if "email" in session:
            email = session["email"]
            print("Logout email: " + email)
            session.pop("email", None)
        return jsonify({"success": True, "message": "Successfully logged in"})       
        
    except Exception as e:
        print("ERROR in logout: ", e)
        return jsonify({"success": False, "message": "There is an error"})

@apiUsers.route("/<int:id>/addTrainingHistory", methods=["POST"])
def addTrainingHistory(id):
    try:
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})

        question_id = request.form.get("question_id")
        answer = request.form.get("answer")
        
        if question_id == None or answer == None:
            return jsonify({"success": False, "message": "Missing fields"})

        User.add_history_by_id(id, question_id, answer)

        return jsonify({"success": True, "message": "History added successfully.."})
        
    except Exception as e:
        print("ERROR in addTrainingHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})
    
@apiUsers.route("/<int:id>/getTrainingHistory", methods=["GET"])
def getTrainingHistory(id):
    try:
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"success": False, "message": "User not found"})
              
        history = user.training_history
        
        if history is None:
            return jsonify({"success": False, "message": "Training history not found"})
        
        historyObj = []
        for record in history:
            historyObj.append({
                "User_id": record.user_id,
                "Question_id": record.question_id,
                "Answer" : record.answer
            })

        return jsonify({"success": True, "data": historyObj, "count": len(historyObj)})
        
    except Exception as e:
        print("ERROR in getTrainingHistory: ", e)
        return jsonify({"success": False, "message": "There is an error"})