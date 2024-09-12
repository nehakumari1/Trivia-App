import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import initialize_db, QuizItem, QuizCategory


class QuizTestCase(unittest.TestCase):
    """This class represents the quiz app's test case"""

    def setUp(self):
        """Define test variables and initialize the app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_NAME = os.getenv('DB_NAME', 'quiz_test_db')
        self.DB_USER = os.getenv('DB_USER', 'your_user')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.database_path = f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
        initialize_db(self.app, self.database_path)

        # Bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Task:
    Write at least one test for each endpoint to validate successful operations and expected errors.
    """

    def test_retrieve_paginated_questions(self):
        """Test the endpoint for getting paginated questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test 404 for out-of-range page number"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource not found")

    def test_retrieve_categories(self):
        """Test the endpoint for fetching categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))

    def test_405_if_categories_deletion_attempted(self):
        """Test method not allowed for categories deletion"""
        res = self.client().delete('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data["success"])

    def test_delete_question(self):
        """Test the endpoint for deleting a question"""
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_if_question_to_delete_does_not_exist(self):
        """Test deletion for a non-existent question"""
        res = self.client().delete('/questions/9999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource not found")

    def test_create_new_question(self):
        """Test the question creation endpoint"""
        new_question = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'difficulty': 2,
            'category': 3
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_search_question(self):
        """Test
