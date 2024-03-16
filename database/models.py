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
    def get_history_by_id(cls, user_id):  
        user = cls.query.filter_by(user_id=user_id).first()
        return user.training_history

    @classmethod
    def add_history_by_id(cls, user_id, question_id, answer):
        user = cls.query.filter_by(user_id=user_id).first()
        
        if len(user.training_history) >= 100:
            oldest_record = min(user.training_history, key=lambda x: x.timestamp)
            user.training_history.remove(oldest_record)
            db.session.delete(oldest_record)
            
        new_history = TrainingHistory(user_id=user_id, question_id=question_id, answer=answer)
        user.training_history.append(new_history)
        db.session.commit()

@dataclass
class Test(db.Model):
    __tablename__ = "test"
    
    test_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    score = db.Column(db.Double)

    def __init__(self, test_id, user_id, score):
        self.test_id = test_id
        self.user_id = user_id
        self.score = score



@dataclass
class Question(db.Model):
    __tablename__ = "questions"
    
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(3000), nullable = False)
    answer_one = db.Column(db.String(2000), nullable = False)
    answer_two = db.Column(db.String(2000), nullable = False)
    
    training_history = db.relationship("TrainingHistory", back_populates="question", cascade="all, delete-orphan")
    
    def __init__(self, question, answer_one, answer_two):
        self.question = question
        self.answer_one = answer_one
        self.answer_two = answer_two
        
    
    @classmethod
    def get_all_questions(cls):  
        return cls.query.all()
    
    @classmethod
    def get_num_of_questions(cls):  
        return len(cls.query.all())
    
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