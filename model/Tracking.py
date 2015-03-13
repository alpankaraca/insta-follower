__author__ = 'cankemik'
from flask.ext.mongoengine import MongoEngine
from libs.MongoAuth import User
db = MongoEngine()

class Tracker(db.Document):
    ip = db.StringField()
    tags = db.StringField()
