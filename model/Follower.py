from flask.ext.mongoengine import MongoEngine

__author__ = 'alpankaraca'

db = MongoEngine()


class Follower(db.Document):
    username = db.StringField()
    profile_picture = db.StringField()
    insta_id = db.StringField()
    full_name = db.StringField()
    following = db.BooleanField(default=True)