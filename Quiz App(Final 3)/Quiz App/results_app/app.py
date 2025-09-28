from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from datetime import datetime
import sys
import os
from flask_login import current_user


# Add the parent directory to Python path to find models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Register blueprint with a specific template folder
results_app = Blueprint('results_app', __name__, template_folder='templates')
@results_app.route('/check-auth')
def check_auth():
    from flask import jsonify
    from flask_login import current_user
    
    auth_info = {
        "current_user_authenticated": current_user.is_authenticated,
        "current_user_type": str(type(current_user)),
        "session_data": dict(session),
        "session_keys": list(session.keys()),
    }
    
    if current_user.is_authenticated:
        auth_info.update({
            "current_user_id": current_user.id,
            "current_user_username": current_user.username,
        })
    
    return jsonify(auth_info)
@results_app.route('/')
def index():
    return render_template('results.html')

@results_app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    from auth_app.models import QuizResult

    if request.method == 'POST':
        raw_category = request.form.get('category', '').lower()
        score_value = request.form.get('score')

        # Standardize category names
        category_mapping = {
            'science': 'Science',
            'history': 'History',
            'sports': 'Sports', 
            'movies and tv': 'Movies and TV',
            'movies_and_tv': 'Movies and TV'
        }
        
        category = category_mapping.get(raw_category, raw_category.title())

        try:
            score = int(score_value) if score_value else 0
        except ValueError:
            score = 0

        # Get user_id using multiple methods
        user_id = None
        username = None
        
        print(f"🔍 === AUTHENTICATION DEBUG ===")
        print(f"🔍 Flask-Login authenticated: {current_user.is_authenticated}")
        print(f"🔍 Session data: {dict(session)}")
        
        # Method 1: Flask-Login
        if current_user.is_authenticated:
            user_id = current_user.id
            username = current_user.username
            print(f"🔍 ✅ Flask-Login: user_id={user_id}, username={username}")
        
        # Method 2: Session data (your current system)
        elif session.get('user_id'):
            user_id = int(session.get('user_id'))
            username = session.get('username')
            print(f"🔍 ✅ Session: user_id={user_id}, username={username}")
        
        # Method 3: Look up by username in session
        elif session.get('username'):
            try:
                from auth_app.models import User
                user = User.query.filter_by(username=session['username']).first()
                if user:
                    user_id = user.id
                    username = user.username
                    print(f"🔍 ✅ Username lookup: user_id={user_id}, username={username}")
            except Exception as e:
                print(f"🔍 ❌ Error looking up user: {e}")
        
        print(f"🔍 Final: user_id={user_id}, category={category}, score={score}")

        # Save the result
        new_result = QuizResult(
            category=category,
            score=score,
            user_id=user_id
        )

        db.session.add(new_result)
        db.session.commit()
        
        print(f"🔍 ✅ Saved result ID {new_result.id} with user_id: {new_result.user_id}")

        return redirect(url_for('results_app.results'))

    return render_template('quiz.html')

@results_app.route('/results')
def results():
    # Import inside function to avoid import issues
    try:
        from auth_app.models import QuizResult
    except ImportError:
        try:
            from models import QuizResult
        except ImportError:
            # Create a temporary model if none exists
            class QuizResult(db.Model):
                id = db.Column(db.Integer, primary_key=True)
                category = db.Column(db.String(100), nullable=False)
                score = db.Column(db.Integer, nullable=False)
                username = db.Column(db.String(100), nullable=True)
                date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Get current user's ID using multiple methods
    user_id = None
    
    print(f"🔍 === RESULTS PAGE DEBUG ===")
    print(f"🔍 Flask-Login authenticated: {current_user.is_authenticated}")
    print(f"🔍 Session data: {dict(session)}")
    
    # Method 1: Flask-Login
    if current_user.is_authenticated:
        user_id = current_user.id
        print(f"🔍 ✅ Flask-Login: user_id={user_id}")
    
    # Method 2: Session data
    elif session.get('user_id'):
        user_id = int(session.get('user_id'))
        print(f"🔍 ✅ Session: user_id={user_id}")
    
    # Method 3: Look up by username in session
    elif session.get('username'):
        try:
            from auth_app.models import User
            user = User.query.filter_by(username=session['username']).first()
            if user:
                user_id = user.id
                print(f"🔍 ✅ Username lookup: user_id={user_id}")
        except Exception as e:
            print(f"🔍 ❌ Error looking up user: {e}")
    
    # If no user is found, redirect to login or show empty results
    if user_id is None:
        print(f"🔍 ❌ No user authenticated - redirecting to login")
        # Option 1: Redirect to login
        # return redirect(url_for('auth_app.login'))
        
        # Option 2: Show empty results with message
        return render_template('results.html', history=[], error_message="Please log in to view your results.")
    
    # Retrieve ONLY the current user's quiz results from the database
    history = QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.date.desc()).all()
    
    print(f"🔍 ✅ Found {len(history)} results for user {user_id}")
    
    return render_template('results.html', history=history)

@results_app.route('/leaderboard')
def leaderboard():
    from auth_app.models import QuizResult
    from sqlalchemy import func
    
    # Define categories with proper capitalization for display
    categories = {
        'Science': ['science', 'Science'],
        'History': ['history', 'History'], 
        'Sports': ['sports', 'Sports'],
        'Movies and TV': ['movies and tv', 'Movies and TV', 'movies_and_tv']
    }
    
    leaderboard_data = {}
    
    # Debug: Check all categories in database
    all_categories = db.session.query(QuizResult.category.distinct()).all()
    print(f"🔍 All categories in database: {[cat[0] for cat in all_categories]}")
    
    for display_name, possible_names in categories.items():
        # Query using case-insensitive search for all possible variations
        top_scores = QuizResult.query.filter(
            func.lower(QuizResult.category).in_([name.lower() for name in possible_names])
        ).order_by(QuizResult.score.desc(), QuizResult.date.asc()).limit(10).all()
        
        print(f"🔍 Category {display_name} found {len(top_scores)} results")
        
        # Process results
        processed_scores = []
        for result in top_scores:
            username = "Anonymous"  # Default
            
            if result.user_id and result.user:
                username = result.user.username
                print(f"🔍 Found user: {username}")
            else:
                print(f"🔍 No user found for result {result.id}")
            
            # Create a simple object that the template can use
            class ScoreData:
                def __init__(self, category, score, username, date):
                    self.category = display_name  # Use display name
                    self.score = score
                    self.username = username
                    self.date = date
            
            score_obj = ScoreData(display_name, result.score, username, result.date)
            processed_scores.append(score_obj)
        
        leaderboard_data[display_name] = processed_scores
    
    # Overall leaderboard (all categories)
    overall_top = QuizResult.query.order_by(QuizResult.score.desc(), QuizResult.date.asc()).limit(10).all()
    
    processed_overall = []
    for result in overall_top:
        username = "Anonymous"
        
        if result.user_id and result.user:
            username = result.user.username
        
        class ScoreData:
            def __init__(self, category, score, username, date):
                self.category = result.category.title()  # Capitalize first letter
                self.score = score
                self.username = username
                self.date = date
        
        score_obj = ScoreData(result.category.title(), result.score, username, result.date)
        processed_overall.append(score_obj)
    
    leaderboard_data['Overall'] = processed_overall
    
    print(f"🔍 Final leaderboard data:")
    for key, scores in leaderboard_data.items():
        print(f"🔍 {key}: {len(scores)} scores")
        if scores:
            print(f"🔍 First score username: {scores[0].username}")
    
    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)