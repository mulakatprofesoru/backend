from flask import Flask, jsonify, Blueprint, request
from database.models import Question, Test

apiTest = Blueprint("apiTest", __name__, url_prefix="/api/tests")

@apiTest.route("/<int:id>", methods=["GET"])
def getTest(id):
    try:
        test = Test.get_test_by_id(id)
        
        if test is None:
            return jsonify({"success": False, "message": "Test not found"})
        
        questions = []
        
        for question in test.questions:
            questions.append({
                "questionId": question.question_id,
                "question": question.question
            })

        return jsonify({"succes": True, "data": questions})

    except Exception as e:
        print("ERROR in getTest: ", e)
        return jsonify({"success": False, "message": "There is an error..."})
    
@apiTest.route("/addTest", methods=["POST"])
def addTest():
    try:
        questions = []
        questions.append(Question.get_question_by_id(request.form.get("q1")))
        questions.append(Question.get_question_by_id(request.form.get("q2")))
        questions.append(Question.get_question_by_id(request.form.get("q3")))
        questions.append(Question.get_question_by_id(request.form.get("q4")))
        questions.append(Question.get_question_by_id(request.form.get("q5")))
        questions.append(Question.get_question_by_id(request.form.get("q6")))
        questions.append(Question.get_question_by_id(request.form.get("q7")))
        questions.append(Question.get_question_by_id(request.form.get("q8")))
        questions.append(Question.get_question_by_id(request.form.get("q9")))
        questions.append(Question.get_question_by_id(request.form.get("q10")))

        if questions == None:
            return jsonify({"success": False, "message": "Missing fields"})

        Test.add_test(questions)

        return jsonify({"success": True, "message": "Test added successfully.."})

    except Exception as e:
        print("ERROR in addTest: ", e)
        return jsonify({"success": False, "message": "There is an error..."})