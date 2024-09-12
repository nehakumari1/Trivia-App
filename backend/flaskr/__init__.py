import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import initialize_db, QuizItem, QuizCategory

QUESTIONS_PER_PAGE = 10

# Function to paginate questions retrieved from the database
def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start_idx = (page - 1) * QUESTIONS_PER_PAGE
    end_idx = start_idx + QUESTIONS_PER_PAGE
    items = [item.serialize() for item in selection]
    return items[start_idx:end_idx]

# Function to create and configure the Flask application
def create_app(test_config=None):
    app = Flask(__name__)
    initialize_db(app)

    '''
    Set up CORS to allow all origins.
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    Add CORS headers after every request.
    '''
    @app.after_request
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Handle GET requests for retrieving all categories
    @app.route("/categories", methods=['GET'])
    def retrieve_categories():
        categories = QuizCategory.query.all()
        category_dict = {category.category_id: category.category_name for category in categories}

        return jsonify({
            'success': True,
            'categories': category_dict
        })

    # GET questions with pagination
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        try:
            # Fetch all quiz items
            items = QuizItem.query.order_by(QuizItem.item_id).all()
            paginated_items = paginate_items(request, items)

            # Return 404 if no questions are found for the page
            if len(paginated_items) == 0:
                abort(404)

            # Fetch all categories
            categories = QuizCategory.query.all()
            category_dict = {category.category_id: category.category_name for category in categories}

            return jsonify({
                'success': True,
                'questions': paginated_items,
                'total_questions': len(items),
                'categories': category_dict
            })
        except Exception as e:
            print(e)
            abort(400)

    # DELETE question by ID
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def remove_question(id):
        try:
            item = QuizItem.query.filter_by(item_id=id).one_or_none()

            if item is None:
                abort(404)

            item.remove()
            # Fetch the updated list of questions
            items = QuizItem.query.order_by(QuizItem.item_id).all()
            paginated_items = paginate_items(request, items)

            return jsonify({
                'success': True,
                'questions': paginated_items,
                'total_questions': len(items)
            })
        except Exception as e:
            print(e)
            abort(404)

    # POST a new question
    @app.route("/questions", methods=['POST'])
    def add_new_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            item = QuizItem(
                question_text=new_question, 
                correct_response=new_answer,
                category_type=new_category, 
                difficulty_level=new_difficulty
            )
            item.save()

            items = QuizItem.query.order_by(QuizItem.item_id).all()
            paginated_items = paginate_items(request, items)

            return jsonify({
                'success': True,
                'created': item.item_id,
                'questions': paginated_items,
                'total_questions': len(items)
            })

        except Exception as e:
            print(e)
            abort(422)

    # Search questions based on a search term
    @app.route("/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', '')
        search_results = QuizItem.query.filter(QuizItem.question_text.ilike(f'%{search_term}%')).all()

        if search_results:
            paginated_results = paginate_items(request, search_results)
            return jsonify({
                'success': True,
                'questions': paginated_results,
                'total_questions': len(search_results)
            })
        else:
            abort(404)

    # GET questions in a specific category
    @app.route("/categories/<int:id>/questions", methods=['GET'])
    def get_questions_by_category(id):
        category = QuizCategory.query.filter_by(category_id=id).one_or_none()

        if category:
            items_in_category = QuizItem.query.filter_by(category_type=str(id)).all()
            paginated_items = paginate_items(request, items_in_category)

            return jsonify({
                'success': True,
                'questions': paginated_items,
                'total_questions': len(items_in_category),
                'current_category': category.category_name
            })
        else:
            abort(404)

    # POST to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions', [])

        try:
            if quiz_category['id'] == 0:
                available_questions = QuizItem.query.all()
            else:
                available_questions = QuizItem.query.filter_by(category_type=quiz_category['id']).all()

            random_question = random.choice([q for q in available_questions if q.item_id not in previous_questions])

            return jsonify({
                'success': True,
                'question': random_question.serialize(),
                'previousQuestions': previous_questions
            })

        except Exception as e:
            print(e)
            abort(404)

    ########## Error handlers ##########

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def handle_unprocessable(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method not allowed"
        }), 405

    return app
