# -*- coding: utf-8 -*-
# ...
# available languages
import os
__author__ = 'cankemik'

LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'tr': 'Turkish'
}
BABEL_DEFAULT_LOCALE = "tr"
BABEL_DEFAULT_TIMEZONE = "GMT+2"
debug = True
DEBUG = True
MAIL_USER = "no-reply@idle.rocks"
MAIL_USER_TITLE = "IDLE"
MAIL_PASSWORD = "ra@e4znet1-*1"
INSTAGRAM_CLIENT_ID = "bfc0ce23818b4d1290298fa1e8a6aa12"
INSTAGRAM_CLIENT_SECRET = "9bbc4d9137254acd9fcd1470a4af2d65"
INSTAGRAM_ACCESS_TOKEN = "8087689.bfc0ce2.b50bccb7c1fc4c5bb9dc154ae21b6595"
INSTAGRAM_REDIRECT_URI = "http://localhost:5000/instagram/instagram_callback"
LOGIN_URL = "/login"
MONGODB_SETTINGS =  {"DB": "instagram"}
MONGOMYADMIN_DATABASES = {
    'local': 'mongodb://127.0.0.1:27017',
    #'remote_qa': 'mongodb://user@pass:mongo.example.com:27017',
}
APP_SECRET = "8d36c9374dd24abb9b878476167caf40"


UPLOAD_FOLDER = os.path.dirname(__file__) + "/static/uploads"
#UPLOAD_FOLDER = "/static/images/uploads"