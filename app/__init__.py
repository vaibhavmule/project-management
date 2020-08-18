from flask import Flask, session, flash, redirect, url_for
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from functools import wraps

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/project_management"
app.config['SECRET_KEY'] = 'some super secret key!'

socketio = SocketIO(app, logger=True)

db = MongoEngine(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

from app import routes