import json
import urllib
from instagram import InstagramAPI
import time

__author__ = 'alpankaraca'
from flask import Flask, session, current_app
from flask.ext.admin import Admin
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongomyadmin import MongoMyAdmin
from controller.Instagram import instagram
from controller.Main import main
from model.Follower import Follower, User
from flask.ext.admin.contrib.mongoengine import ModelView


app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = MongoEngine(app)
m = MongoMyAdmin(app)
app.session_interface = MongoEngineSessionInterface(db)



#User.objects.all().delete()

with app.app_context():

    while True:
        for um in User.objects.all():

            instagram_user = um

            api = InstagramAPI(access_token=um.access_token)
            followers = api.user_followed_by(um.details.get('id'))
            #print followers
            f_arr = []
            for u in followers[0]:
                f_arr.append(u)
            ff = f_arr


            values = {"access_token": instagram_user.access_token, "count": "10000000000000000",
                      'client_id': current_app.config.get('INSTAGRAM_CLIENT_ID'),
                      'client_secret': current_app.config.get('INSTAGRAM_CLIENT_SECRET')}
            data = urllib.urlencode(values)
            url = 'https://api.instagram.com/v1/users/' + um.details.get('id') + '/followed-by'
            callback = json.loads(urllib.urlopen(url + "?%s" % data).read())

            users = []

            users = callback[u'data']
            uurrll = callback[u'pagination'][u'next_url']

            while True:
                daataa = json.loads(urllib.urlopen(uurrll).read())
                try:
                    users += daataa[u'data']
                    uurrll = daataa[u'pagination'][u'next_url']
                    print uurrll

                except:
                    break

            print json.dumps(users)

            usernames =[]
            for user in users:
                usernames.append(user[u'username'])
                try:
                    uu = User.objects.get(access_token=um.access_token, followers__insta_id=user[u'id'])
                except:
                    uu = Follower()
                    uu.username = user[u'username']
                    uu.profile_picture = user[u'profile_picture']
                    uu.insta_id = user[u'id']
                    uu.full_name = user[u'full_name']
                    instagram_user.followers.append(uu)
                    instagram_user.save()

            from model.Follower import Follower

            unfollowed = []

            for f in instagram_user.followers:
                if f.username not in usernames:
                    unfollowed.append(f)
                    print f.username

                    f.following = False
                    instagram_user.save()

