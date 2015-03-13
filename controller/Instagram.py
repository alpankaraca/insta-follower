import json
import urllib
import urllib2
from libs.crossdomain import crossdomain
from model.Tag import Tag
from model.Tracking import Tracker

__author__ = 'cankemik'
from flask import Blueprint, render_template, abort, current_app, request, session, redirect, jsonify
from instagram import InstagramAPI

instagram = Blueprint('instagram', __name__, template_folder='templates')


@instagram.route("/")
def user_photos():
    if 'instagram_access_token' in session and 'instagram_user' in session:
        userAPI = InstagramAPI(access_token=session['instagram_access_token'])
        recent_media, next = userAPI.user_recent_media(user_id=session['instagram_user'].get('id'))
        photos = []
        for media in recent_media:
            photos.append(media.images['standard_resolution'].url)
        return json.dumps(photos)
    else:
        return redirect('/instagram/connect')


@instagram.route('/connect')
def main():
    instaConfig = {
        'client_id': current_app.config.get('INSTAGRAM_CLIENT_ID'),
        'client_secret': current_app.config.get('INSTAGRAM_CLIENT_SECRET'),
        'redirect_uri': current_app.config.get('INSTAGRAM_REDIRECT_URI')
    }
    api = InstagramAPI(**instaConfig)
    url = api.get_authorize_url(scope=["likes", "comments"])
    return "<a href='" + url + "'>url</a>"


@instagram.route('/instagram_callback')
def instagram_callback():
    instaConfig = {
        'client_id': current_app.config.get('INSTAGRAM_CLIENT_ID'),
        'client_secret': current_app.config.get('INSTAGRAM_CLIENT_SECRET'),
        'redirect_uri': current_app.config.get('INSTAGRAM_REDIRECT_URI')
    }
    api = InstagramAPI(**instaConfig)
    code = request.args.get('code')
    if code:
        access_token, user = api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        session['instagram_access_token'] = access_token
        session['instagram_user'] = user

        return "<script type='text/javascript'>window.close();</script>"

    else:
        return "Uhoh no code provided"


@instagram.route('/searchbytag', methods=["POST", "PUT", "GET"])
def searchbytag():
    img_array = []
    pdata = request.args.get("tag").split(",")
    if request.method == "POST":
        pdata = json.loads(request.data)
    values = {"access_token": current_app.config.get('INSTAGRAM_ACCESS_TOKEN'), "count": "10000000000000000",
              'client_id': current_app.config.get('INSTAGRAM_CLIENT_ID'),
              'client_secret': current_app.config.get('INSTAGRAM_CLIENT_SECRET')}
    data = urllib.urlencode(values)
    if pdata != "":
        t = Tracker()
        t.ip = request.remote_addr
        t.tags = ', '.join([str(x) for x in pdata])
        t.save()
        old_next_urls = []
        new_next_urls = []
        img_array = []
        for i in pdata:
            url = "https://api.instagram.com/v1/tags/" + i + "/media/recent"
            callback = json.loads(urllib.urlopen(url + "?%s" % data).read())
            print callback
            old_next_urls.append(callback[u'pagination'][u'next_url'])
            for j in callback[u'data']:
                if j[u'likes'][u'count'] > 5:
                    img_array.append(j[u'images'][u'standard_resolution'][u'url'])
                    if len(img_array) > 15:
                        return json.dumps(img_array)
        while len(img_array) < 300:
            for i in old_next_urls:
                callback = json.loads(urllib.urlopen(i).read())
                new_next_urls.append(callback[u'pagination'][u'next_url'])
                for j in callback[u'data']:
                    if j[u'likes'][u'count'] > 5:
                        img_array.append(j[u'images'][u'standard_resolution'][u'url'])
                        print j[u'images'][u'standard_resolution'][u'url']
                        if len(img_array) > 15:
                            return json.dumps(img_array)
            old_next_urls = new_next_urls
            new_next_urls = []
            print len(img_array)
    return json.dumps(img_array)


@instagram.route('/get-tags', methods=["POST", "PUT", "GET"])
@crossdomain(origin='*', headers="*", methods="*")
def get_tags():
    try:
        t =Tag.objects.get(name=request.args.get("tag")).users
        images = []
        for i in t:
            if len(i.images) > 0:
                print "high"
            else:
                api = InstagramAPI(access_token=current_app.config.get('INSTAGRAM_ACCESS_TOKEN'))
                api.user_search("cankemik")
                print "low"
    except Exception as e:
        print e
        return json.dumps({"err": "sorry tag not found :("})
    return "ok"


@instagram.route('/get-followers', methods=["POST", "GET"])
def get_followers():
    api = InstagramAPI(access_token=current_app.config.get('INSTAGRAM_ACCESS_TOKEN'))
    user = api.user_search("alpan")[0]
    print dir(user)
    print user
    followers = api.user_followed_by(user.id)
    print followers
    f_arr = []
    print len(followers[0])
    for u in followers[0]:
        f_arr.append(u)
    ff = f_arr

    values = {"access_token": current_app.config.get('INSTAGRAM_ACCESS_TOKEN'), "count": "10000000000000000",
              'client_id': current_app.config.get('INSTAGRAM_CLIENT_ID'),
              'client_secret': current_app.config.get('INSTAGRAM_CLIENT_SECRET')}
    data = urllib.urlencode(values)
    url = 'https://api.instagram.com/v1/users/' + user.id + '/followed-by'
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
    for uu in users:
        usernames.append(uu[u'username'])

    from model.Follower import Follower

    unfollowed = []

    for f in Follower.objects.all():
        if f.username not in usernames:
            unfollowed.append(f)
            f.following = False
            f.save()

    for user in users:
        try:
            u = Follower.objects.get(username=user[u'username'])
        except:
            u = Follower()
            u.username = user[u'username']
            u.profile_picture = user[u'profile_picture']
            u.insta_id = user[u'id']
            u.full_name = user[u'full_name']
            u.save()


    return render_template('followers.html', ff=users, unf=unfollowed)




















