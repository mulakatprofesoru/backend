from flask import Flask, jsonify, Blueprint, request
from werkzeug.security import generate_password_hash
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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        print("USERNAME: ", username)
        print("EMAIL: ", email)
        print("PASSWORD: ", password)

        if username == None or email == None or password == None:
            return jsonify({"success": False, "message": "Missing fields"})

        hashed_password = generate_password_hash(password)

        print("Hashed password: ", hashed_password)

        User.add_user(username, email, hashed_password)

        return jsonify({"success": True, "message": "User added successfully.."})
    except Exception as e:
        print("ERROR in addUser: ", e)
        return jsonify({"success": False, "message": "There is an error"})