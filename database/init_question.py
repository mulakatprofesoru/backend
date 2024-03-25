import csv
from database.models import Question
from flask import current_app

def fill_question_database(db):
    existing_questions = Question.query.all()
    if existing_questions:
        return
    
    first = True
    with current_app.app_context():
        with open('database\\data\\QuestionAnswerData.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if first:
                    first = False
                    continue
                
                question = row[0]
                answer1 = row[1]
                answer2 = row[2]
                question_type = row[3]
                new_question = Question(question=question, answer_one=answer1, answer_two=answer2, question_type=question_type)
                db.session.add(new_question)
        db.session.commit()