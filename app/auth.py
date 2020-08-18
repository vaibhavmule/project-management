
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
    roles = db.ListField()

    created_at = db.DateTimeField(default=datetime.datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

      
class Permission(db.Document):
    meta = {
        'collection': 'permissions'
    }

    role = db.ReferenceField('Role')
    action = db.StringField()


class Role(db.Document):
    meta = {
        'collection': 'roles'
    }

    name = db.StringField()
    permissions = db.ListField()

    def has_permission(self, role, action):
        return any(
            [
                role == perm.role.name and action == perm.action
                for perm in self.permissions
            ]
        )

def permission_required(permissions):
    """
    Check if a user has permission to a resource.
    :param permissions: List of permissions consistent with tuples. E.g.
    [('user', 'read'), ('admin', 'create')]
    :return: a function or raise 403
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            roles = Permission.objects.distinct('role')
            if hasattr(current_user, 'roles'):
                if set(current_user.roles) & set(roles):
                    for role, action in permissions:
                        for user_role in current_user.roles:
                            if user_role.has_permission(role, action):
                                return func(*args, **kwargs)
            abort(403)

        return wrapped

    return wrapper