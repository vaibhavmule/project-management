import datetime
from functools import wraps

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask import abort

from flask_login import UserMixin, current_user

from app import db


class User(db.Document, UserMixin):
    meta = {
        'collection': 'users'
    }

    username = db.StringField()
    password = db.StringField()
    role = db.StringField()

    created_at = db.DateTimeField(default=datetime.datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


def permission_required(role):

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if current_user.role == role:
                return func(*args, **kwargs)
            abort(403)

        return wrapped

    return wrapper