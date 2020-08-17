from flask import Flask, session, flash, redirect, url_for
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from functools import wraps

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config['SECRET_KEY'] = 'some super secret key!'

mongo = PyMongo(app)
db = mongo.db

socketio = SocketIO(app, logger=True)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

from app import routes

socketio.run(app)