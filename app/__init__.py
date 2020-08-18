import os
from os.path import join, dirname

from flask import Flask
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

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