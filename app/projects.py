import datetime

from app import db

from .auth import User


class Comment(db.EmbeddedDocument):
    text = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now())
    by = db.ReferenceField(User)


class Project(db.Document):
	title = db.StringField()
	comments = db.ListField(db.EmbeddedDocumentField(Comment))
	engineers = db.ListField(db.ReferenceField(User))
