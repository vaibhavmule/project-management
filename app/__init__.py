from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/project_management"
app.config['SECRET_KEY'] = 'some super secret key!'

socketio = SocketIO(app, logger=True)

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	from .auth import User
	return User.objects(pk=user_id).first()

from app import routes