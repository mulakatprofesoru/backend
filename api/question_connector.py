from flask import Flask, jsonify, Blueprint, request
from database.models import Question
import random

apiQuestion = Blueprint("apiQuestion", __name__, url_prefix="/api/questions")


@apiQuestion.route("/")
def questions():
    try:
        allQuestions = Question.get_all_questions()

        questions_list = []

        for question in allQuestions:
            questions_list.append(
                {
                    "question_id": question.question_id,
                    "question": question.question,
                    "answer_one": question.answer_one,
                    "answer_two": question.answer_two
                }
            )

        return jsonify({"succes": True, "data": questions_list, "count": len(questions_list)})

    except Exception as e:
        print("ERROR in questions: ", e)
        return jsonify({"success": False, "message": "There is an error..."})
    
@apiQuestion.route("/random/<question_type>", methods=["GET"])
def random_question(question_type):
    try:
        if question_type == "bilgisayar-muhendisligi":
            question_type_num = "1"
        else: #Genel Soru Tipi
            question_type_num = "0"

        questions = Question.get_questions_by_type(question_type_num)

        if questions:
            random_question = random.choice(questions)
            random_question_data = {
                    "question_id": random_question.question_id,
                    "question": random_question.question
            }
            return jsonify({"succes": True, "data": random_question_data})

        else:
            return jsonify({'message': "Cannot find this type of question"})

    except Exception as e:
        print("ERROR in selection of random question: ", e)
        return jsonify({"success": False, "message": "There is an error..."})

@apiQuestion.route("/addQuestion", methods=["POST"])
def addQuestion():
    try:
        question = request.form.get("question")
        answer_one = request.form.get("answer_one")
        answer_two = request.form.get("answer_two")

        if question == None or answer_one == None or answer_two == None:
            return jsonify({"success": False, "message": "Missing fields"})

        Question.add_question(question, answer_one, answer_two)

        return jsonify({"success": True, "message": "Question added successfully.."})
    except Exception as e:
        print("ERROR in addQuestion: ", e)
        return jsonify({"success": False, "message": "There is an error"})
