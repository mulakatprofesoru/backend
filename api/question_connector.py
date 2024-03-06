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
    

@apiQuestion.route("/random", methods=["GET"])
def random_question():
    try:
        total_questions_number = Question.get_num_of_questions()

        random_id = random.randint(1, total_questions_number)
        random_question_whole_entity = Question.get_question_by_id(question_id=random_id)

        random_question = {
                    "question_id": random_question_whole_entity.question_id,
                    "question": random_question_whole_entity.question
                }
        
        #data = {'question': 'Bizi neden tercih ettiniz?'}
        #return jsonify(data)

        return jsonify({"succes": True, "data": random_question})

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
