import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# Database configurations using environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'manal')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123456m')
DB_NAME = os.getenv('DB_NAME', 'trivia')
db_url = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy()

'''
initialize_db(app)
    This function links a Flask app to the SQLAlchemy service
'''

def initialize_db(app, db_url=db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
QuizItem
    Represents the questions in the quiz game
'''

class QuizItem(db.Model):
    __tablename__ = 'quiz_items'

    item_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    correct_response = Column(String)
    category_type = Column(String)
    difficulty_level = Column(Integer)

    def __init__(self, question_text, correct_response, category_type, difficulty_level):
        self.question_text = question_text
        self.correct_response = correct_response
        self.category_type = category_type
        self.difficulty_level = difficulty_level

    # Method to insert a new quiz item into the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Method to update the existing quiz item details
    def apply_update(self):
        db.session.commit()

    # Method to delete the quiz item from the database
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    # Format the quiz item data for easier consumption in APIs
    def serialize(self):
        return {
            'item_id': self.item_id,
            'question_text': self.question_text,
            'correct_response': self.correct_response,
            'category_type': self.category_type,
            'difficulty_level': self.difficulty_level
        }

'''
QuizCategory
    Represents the category of quiz questions
'''

class QuizCategory(db.Model):
    __tablename__ = 'quiz_categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)

    def __init__(self, category_name):
        self.category_name = category_name

    # Format the quiz category data for easier consumption in APIs
    def serialize(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name
        }
