from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required as flask_login_required
from functools import wraps
from extensions import db
from auth_app.models import User

auth_app = Blueprint('auth_app', __name__, template_folder='templates', static_folder='static')

# Custom decorator for session-based auth (keep as backup)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to take the quiz.', 'warning')
            return redirect(url_for('auth_app.login'))
        return f(*args, **kwargs)
    return decorated_function

# Signup route
@auth_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('signup.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return render_template('signup.html')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth_app.login'))

    return render_template('signup.html')

# Login route - FIXED to work with Flask-Login
@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # IMPORTANT: Use Flask-Login's login_user()
            login_user(user)
            
            # Also set session data as backup
            session['username'] = user.username
            session['user_id'] = user.id  # Add user_id to session
            
            print(f"🔍 User {user.username} logged in with ID: {user.id}")
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')

    return render_template('login.html')

# Logout route - FIXED to work with Flask-Login
@auth_app.route('/logout')
def logout():
    logout_user()  # Flask-Login logout
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Quiz routes - you can use either decorator now
@auth_app.route('/quiz/science', methods=['GET', 'POST'])
@flask_login_required  # Use Flask-Login's decorator
def science_quiz():
    return render_template('science_quiz.html')

@auth_app.route('/quiz/history', methods=['GET', 'POST'])
@flask_login_required
def history_quiz():
    return render_template('history_quiz.html')

@auth_app.route('/quiz/movies', methods=['GET', 'POST'])
@flask_login_required
def movies_quiz():
    return render_template('movies_quiz.html')

@auth_app.route('/quiz/sports', methods=['GET', 'POST'])
@flask_login_required
def sports_quiz():
    return render_template('sports_quiz.html')