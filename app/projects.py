from app import db


class Comment(db.EmbeddedDocument):
    text = db.StringField()


class Project(db.Document):
	title = db.StringField()
	comments = db.ListField(db.EmbeddedDocumentField(Comment))
