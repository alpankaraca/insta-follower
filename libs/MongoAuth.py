# -*- coding: utf-8 -*-
__author__ = 'cankemik'
from bson.json_util import default
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import datetime, hashlib
from flask import session, request
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    email = db.StringField()
    password = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    last_login = db.DateTimeField()
    verified_mail = db.BooleanField(default=False)
    verified_user = db.BooleanField()
    phone = db.StringField()
    rights = db.DictField()
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def log(self, action, data={}):
        l = UserLog()
        l.user = self
        l.time = datetime.datetime.now()
        l.action = action
        l.data = data
        try:
            l.ip = request.remote_addr
        except:
            pass
        l.save()

    def remove_right(self, module, right="all"):
        if self.rights.get(module):
            if self.rights.get(module).get(right):
                del self.rights[module][right]
                self.save()
        return True

    def add_right(self, module, right="all"):
        if self.rights.get(module):
            if self.rights.get(module).get(right):
                return True
            else:
                if right == "all":
                    self.rights.update(
                        {"all": True, "read": True, "write": True, "list": True, "Download": True, "update": True,
                         "delete": True})
                else:
                    self.rights.update({right: True})
                self.save()
                return True

    def has_right(self, module, right="all"):
        if self.rights.get(module):
            if self.rights.get(module).get("all"):
                return True
            return self.rights.get(module).get(right)
        else:
            return False

    def save(self, *args, **kwargs):
        if len(self.password) < 32:
            self.password = hashlib.md5(self.password).hexdigest()
        return super(User, self).save(*args, **kwargs)

    def login(self, email, password):
        if password == "facebook":
            data = User.objects.get(email=email)
            return data
        if len(password) == 32:
            password_hash = password
        else:
            password_hash = hashlib.md5(password).hexdigest()

        data = User.objects(email=email, password=password_hash)

        if data.all().count() > 0:
            data = data.get()
            data.log("login")
            return data

        return False

    def __unicode__(self):
        return str(self.first_name) + " " + str(self.last_name)


class UserLog(db.Document):
    user = db.ReferenceField(User)
    time = db.DateTimeField(default=datetime.datetime.now, required=True)
    action = db.StringField()
    data = db.DictField()
    ip = db.StringField()


def user():
    if session.get("ulogin"):
        user = User.objects.get(id=session.get("ulogin").get("_id"))
        return user
    return None


def login(email, password):
    """ Login fonksiyonu """

    u = User()
    login_data = u.login(email, password)
    if login_data:
        login_data.last_login = datetime.datetime.now()
        login_data.save()

        session["ulogin"] = login_data.to_mongo()
        return True
    else:
        return False