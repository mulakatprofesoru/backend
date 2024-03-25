import csv
from database.models import Question, Test
from flask import current_app

def fill_tests_database(db):
    existing_questions = Test.query.all()
    if existing_questions:
        return
    
    first = True
    with current_app.app_context():
        with open('database\\data\\Tests.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if first:
                    first = False
                    continue
                
                questions = []
                questions.append(Question.get_question_by_id(row[0]))
                questions.append(Question.get_question_by_id(row[1]))
                questions.append(Question.get_question_by_id(row[2]))
                questions.append(Question.get_question_by_id(row[3]))
                questions.append(Question.get_question_by_id(row[4]))
                questions.append(Question.get_question_by_id(row[5]))
                questions.append(Question.get_question_by_id(row[6]))
                questions.append(Question.get_question_by_id(row[7]))
                questions.append(Question.get_question_by_id(row[8]))
                questions.append(Question.get_question_by_id(row[9]))

                new_test = Test(questions)
                db.session.add(new_test)
        db.session.commit()