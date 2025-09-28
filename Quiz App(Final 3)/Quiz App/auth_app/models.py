from extensions import db
from flask_login import UserMixin
from datetime import datetime
class User(db.Model, UserMixin):  # Inherit UserMixin to work with Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Flask-Login requires this method to retrieve the user ID
    def get_id(self):
        return str(self.id)  # Return as string, as expected by Flask-Login

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    
    user = db.relationship('User', backref='results')
    def __repr__(self):
        return f'<QuizResult {self.category}: {self.score}/10 by {self.user.username if self.user else "Guest"}>'