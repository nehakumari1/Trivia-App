import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# pagination for the questions


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins. 
  '''
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # handle GET requests for all available categories.
    @app.route("/categories")
    def get_all_categories():
        # get all categories
        categories = Category.query.all()
        # categories dict for holding the retrives categories
        categoriesDict = {}

        # adding all categories to the dict
        for category in categories:
            categoriesDict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categoriesDict
        })


# GET requests for questions including pagination (every 10 questions).
# This endpoint returns a list of questions, number of total questions, current category, categories.
    @app.route('/questions')
    def get_questions():
        try:
            # get all questions
            selection = Question.query.order_by(Question.id).all()
            # get the total num of questions
            totalQuestions = len(selection)
            # get current questions in a page (10q)
            currentQuestions = paginate_questions(request, selection)

            # if the page number is not found
            if (len(currentQuestions) == 0):
                abort(404)

            # get all categories
            categories = Category.query.all()
            categoriesDict = {}
            for category in categories:
                categoriesDict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': totalQuestions,
                'categories': categoriesDict
            })
        except Exception as e:
            print(e)
            abort(400)


# DELETE question using a question ID.
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            # if the question is not found
            if question is None:
                abort(404)

            question.delete()
            # send back the current books, to update front end
            selection = Question.query.order_by(Question.id).all()
            currentQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                # 'questions': currentQuestions,
                # 'total_questions': len(selection)
            })

        except Exception as e:
            print(e)
            abort(404)


# POST a new question, which will require the question and answer text, category, and difficulty score.
    @app.route("/questions", methods=['POST'])
    def add_question():
        # get the body from requist
        body = request.get_json()

        # get new data, none if not enterd
        newQuestion = body.get('question', None)
        newAnswer = body.get('answer', None)
        newCategory = body.get('category', None)
        newDifficulty = body.get('difficulty', None)

        try:
            # add ..
            question = Question(question=newQuestion, answer=newAnswer,
                                category=newCategory, difficulty=newDifficulty)
            question.insert()

            # send back the current questions, to update front end
            selection = Question.query.order_by(Question.id).all()
            currentQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': currentQuestions,
                'total_questions': len(selection)
            })

        except Exception as e:
            print(e)
            abort(422)


# POST endpoint to get questions based on a search term
    @app.route("/search", methods=['POST'])
    def search():
        body = request.get_json()
        search = body.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike('%'+search+'%')).all()

        if questions:
            currentQuestions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questions)
            })
        else:
            abort(404)


# GET questions based on category.
    @app.route("/categories/<int:id>/questions")
    def questions_in_category(id):
        # retrive the category by given id
        category = Category.query.filter_by(id=id).one_or_none()
        if category:
            # retrive all questions in a category
            questionsInCat = Question.query.filter_by(category=str(id)).all()
            currentQuestions = paginate_questions(request, questionsInCat)

            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questionsInCat),
                'current_category': category.type
            })
        # if category not founs
        else:
            abort(404)


# POST endpoint to get questions to play the quiz, This endpoint takes category and previous question parameters and returns a random question within the given category if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        # get the qestion category an the previous question
        body = request.get_json()
        quizCategory = body.get('quiz_category')
        previousQuestion = body.get('previous_questions')

        try:
            if (quizCategory['id'] == 0):
                questionsQuery = Question.query.all()
            else:
                questionsQuery = Question.query.filter_by(
                    category=quizCategory['id']).all()

            randomIndex = random.randint(0, len(questionsQuery)-1)
            nextQuestion = questionsQuery[randomIndex]

            stillQuestions = True
            while nextQuestion.id not in previousQuestion:
                nextQuestion = questionsQuery[randomIndex]
                return jsonify({
                    'success': True,
                    'question': {
                        "answer": nextQuestion.answer,
                        "category": nextQuestion.category,
                        "difficulty": nextQuestion.difficulty,
                        "id": nextQuestion.id,
                        "question": nextQuestion.question
                    },
                    'previousQuestion': previousQuestion
                })

        except Exception as e:
            print(e)
            abort(404)

############# Error handlers #############

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_recource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable recource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method!"
        }), 405

    return app
