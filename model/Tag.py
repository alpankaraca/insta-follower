__author__ = 'cankemik'
from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

class User(db.EmbeddedDocument):
    name = db.StringField()
    order = db.IntField()
    images = db.ListField(db.StringField())


class Tag(db.Document):
    users = db.ListField(db.EmbeddedDocumentField(User))
    name = db.StringField()
