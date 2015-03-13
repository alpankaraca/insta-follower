__author__ = 'cankemik'


from flask.ext.mongoengine import MongoEngine
from libs.MongoAuth import User
db = MongoEngine()


class Apps(db.Document):
    app_id = db.StringField()
    app_secret = db.StringField()
    app_name = db.StringField()
    app_status = db.IntField(default=1)
    app_admin = db.ReferenceField(User)


class Tokens(db.Document):

    access_token = db.StringField()
    expires = db.StringField()
    connect_type = db.IntField()
    app = db.ReferenceField(Apps)
    user = db.ReferenceField(User)


class Devices(db.Document):
    device_id = db.StringField()
    device_os = db.StringField()
    device_os_version = db.StringField()
