from flask import Blueprint, render_template, jsonify
import json
import random
import os

# Register blueprint with a specific template folder
history_app = Blueprint('history_app',__name__, template_folder='templates', static_folder='static')
# Load questions from the JSON file
def load_questions():
    try:
        # Define the path to the sports_questions.json file in the 'json' folder
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'history_questions.json')
        print(f"Loading questions from: {json_file_path}")

        # Open and load the JSON data
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. Details: {e}")
        return []

# Route to serve the sports quiz page
@history_app.route('/')
def index():
    return render_template('history.html')

# API endpoint to get random questions
@history_app.route('/api/questions')
def questions():
    all_questions = load_questions()
    
    # Ensure the file has at least 10 questions
    if len(all_questions) < 10:
        return jsonify({"error": "Not enough questions in the JSON file"}), 400

    random_questions = random.sample(all_questions, 10)  # Select 10 random questions
    print(f"Returning questions: {random_questions}")  # Debug log
    return jsonify(random_questions)
