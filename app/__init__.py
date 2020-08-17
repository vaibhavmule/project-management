from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.config['SECRET_KEY'] = 'some super secret key!'

mongo = PyMongo(app)

socketio = SocketIO(app, logger=True)

from app import routes

socketio.run(app)