# init_db.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db
from auth_app.models import User
from main_app import app  # Import the app object to use its context

with app.app_context():
    db.create_all()  # Create tables defined in models
    print("Database initialized with 'user' table.")
