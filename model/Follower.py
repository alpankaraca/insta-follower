from flask.ext.mongoengine import MongoEngine

__author__ = 'alpankaraca'

db = MongoEngine()


class Follower(db.EmbeddedDocument):
    username = db.StringField()
    profile_picture = db.StringField()
    insta_id = db.StringField()
    full_name = db.StringField()
    following = db.BooleanField(default=True)
    user = db.StringField()


class User(db.Document):
    details = db.DictField()
    access_token = db.StringField()
    followers = db.ListField(db.EmbeddedDocumentField(Follower))