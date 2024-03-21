from dataclasses import dataclass
from database import db
from datetime import datetime, timezone

@dataclass
class User(db.Model):
    __tablename__ = "user"
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    general_score = db.Column(db.Double)
    
    training_history = db.relationship("TrainingHistory", back_populates="user", cascade="all, delete-orphan")
    test_history = db.relationship("TestHistory", back_populates="user", cascade="all, delete-orphan")
    
    
    def __init__(self, user_id, username, email, password, general_score):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.general_score = general_score
    
    @classmethod
    def get_all_users(cls):  
        return cls.query.all()
    
    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def add_user(cls, username, email, password):  # Id'yi unique biz vericez.
        user = User(None, username, email, password, 0)
        db.session.add(user)
        db.session.commit()
        
    @classmethod
    def update_user(cls, user_id, username, email, password, general_score):
        user = cls.query.filter_by(user_id=user_id).first()
        user.username = username
        user.email = email
        user.password = password
        user.general_score = general_score
        db.session.commit()
        
    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        
    @classmethod
    def get_training_history_by_id(cls, user_id):  
        user = cls.query.filter_by(user_id=user_id).first()
        return user.training_history

    @classmethod
    def add_training_history_by_id(cls, user_id, question_id, answer):
        user = cls.query.filter_by(user_id=user_id).first()
        
        if len(user.training_history) >= 100:
            oldest_record = min(user.training_history, key=lambda x: x.timestamp)
            user.training_history.remove(oldest_record)
            db.session.delete(oldest_record)
            
        new_history = TrainingHistory(user_id=user_id, question_id=question_id, answer=answer)
        user.training_history.append(new_history)
        db.session.commit()
        
    @classmethod
    def get_test_history_by_id(cls, user_id):  
        user = cls.query.filter_by(user_id=user_id).first()
        return user.test_history
    
    @classmethod
    def add_test_history_by_id(cls, user_id, test_id):
        user = cls.query.filter_by(user_id=user_id).first()
        
        if len(user.test_history) >= 10:
            oldest_record = min(user.test_history, key=lambda x: x.timestamp)
            user.test_history.remove(oldest_record)
            
        new_history = TestHistory(user_id=user_id, test_id=test_id)
        user.test_history.append(new_history)
        db.session.commit()
        return new_history.test_history_id
        
    @classmethod
    def add_test_question_history_by_id(cls, user_id, test_history_id, question_id, answer):
        test_history = TestHistory.get_test_history_by_id(test_history_id)
        new_test_question_history = TestQuestionHistory(user_id=user_id, test_history_id=test_history.test_history_id, question_id=question_id, answer=answer)
        test_history.test_question_history.append(new_test_question_history)
        db.session.commit()


@dataclass
class Question(db.Model):
    __tablename__ = "questions"
    
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(3000), nullable = False)
    answer_one = db.Column(db.String(2000), nullable = False)
    answer_two = db.Column(db.String(2000), nullable = False)
    question_type = db.Column(db.String(200), nullable = False)
    
    training_history = db.relationship("TrainingHistory", back_populates="question", cascade="all, delete-orphan")
    test_question_history = db.relationship("TestQuestionHistory", back_populates="question", cascade="all, delete-orphan")
    
    def __init__(self, question, answer_one, answer_two, question_type):
        self.question = question
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.question_type = question_type
        
    
    @classmethod
    def get_all_questions(cls):  
        return cls.query.all()
    
    @classmethod
    def get_num_of_questions(cls):  
        return len(cls.query.all())
    
    @classmethod
    def get_questions_by_type(cls, question_type):
        return cls.query.filter_by(question_type = question_type).all()
    
    @classmethod
    def get_question_by_id(cls, question_id):
        return cls.query.filter_by(question_id=question_id).first()
    
    @classmethod
    def add_question(cls, question, answer_one, answer_two):
        new_question = Question(question, answer_one, answer_two)
        db.session.add(new_question)
        db.session.commit()
        
@dataclass
class TrainingHistory(db.Model):
    __tablename__ = "training_history"
    
    training_history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer = db.Column(db.String(2000), nullable=False)
    #score = db.Column(db.Float, nullable = False) SONRADAN EKLENECEK
    timestamp = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    
    user = db.relationship("User", back_populates="training_history")
    question = db.relationship("Question", back_populates="training_history")
    
    def __init__(self, user_id, question_id, answer):
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer
        
        
test_question_association = db.Table(
    'test_question',
    db.Column('test_id', db.Integer, db.ForeignKey('tests.test_id')),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.question_id'))
)

@dataclass
class Test(db.Model):
    __tablename__ = "tests"
    
    test_id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship("Question", secondary=test_question_association, backref="tests")
    test_history = db.relationship("TestHistory", back_populates="test", cascade="all, delete-orphan")
    
    def __init__(self, questions):
        self.questions = questions
        
    @classmethod
    def get_test_by_id(cls, test_id):
        return cls.query.filter_by(test_id=test_id).first()
    
    @classmethod
    def add_test(cls, questions):
        new_test = Test(questions)
        db.session.add(new_test)
        db.session.commit()
        
@dataclass
class TestHistory(db.Model):
    __tablename__ = "test_history"
    
    test_history_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.test_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    
    user = db.relationship("User", back_populates="test_history")
    test = db.relationship("Test", back_populates="test_history")
    test_question_history = db.relationship("TestQuestionHistory", back_populates="test_history", cascade="all, delete-orphan")

    
    def __init__(self, user_id, test_id):
        self.user_id = user_id
        self.test_id = test_id
        
    @classmethod
    def get_test_history_by_id(cls, test_history_id):
        return cls.query.filter_by(test_history_id=test_history_id).first()

@dataclass
class TestQuestionHistory(db.Model):
    __tablename__ = "test_question_history"
    
    test_question_history_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(2000), nullable=False)
    test_history_id = db.Column(db.Integer, db.ForeignKey('test_history.test_history_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    timestamp = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    
    question = db.relationship("Question", back_populates="test_question_history")
    test_history = db.relationship("TestHistory", back_populates="test_question_history")
    
    def __init__(self, user_id, test_history_id, question_id, answer):
        self.user_id = user_id
        self.test_history_id = test_history_id
        self.question_id = question_id
        self.answer = answer