from flask import Flask, render_template
from flask_login import LoginManager
from auth_app.app import auth_app
from science_app.app import science_app
from history_app.app import history_app
from movies_app.app import movies_app
from sports_app.app import sports_app
from results_app.app import results_app
from extensions import db
from auth_app.models import User   

# Initialize the Flask app
app = Flask(__name__)

# Configuration for the app
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# ----------- Flask-Login -----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_app.login'   
#-----------------------------------

with app.app_context():
    db.create_all()

# ----------- user_loader -----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#-----------------------------------

# Register blueprints
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(science_app, url_prefix='/science')
app.register_blueprint(history_app, url_prefix='/history')
app.register_blueprint(movies_app, url_prefix='/movies')
app.register_blueprint(sports_app, url_prefix='/sports')
app.register_blueprint(results_app, url_prefix='/results')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
