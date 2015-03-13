__author__ = 'cankemik'
from functools import wraps
from flask import request,render_template , current_app, make_response , session , abort as sendAbort , redirect
from libs.XMLD import dict2xml
import os , datetime , hashlib
from libs.MongoAuth import user
from bson import json_util
from bson.json_util import ObjectId
from flask import Response as fResponsex
from model.API import Apps , Tokens
from types import *
import bson


def fResponse(*args, **kwargs):
    resp = make_response(fResponsex(*args, **kwargs))
    h = resp.headers
    h['Access-Control-Allow-Origin'] = "*"
    h['Access-Control-Allow-Methods'] = "*"
    return resp

def some_random_string():

    return hashlib.md5(str(datetime.datetime.now())+"ASD"+"_"+request.remote_addr).hexdigest()

def replaceListToDict(data):
        newList = []
        for i in data:
            if type(i) is dict:
                newList.append(replaceKeys(i))
            elif type(i) is list :
                newList.append(replaceListToDict(i))
            else:
                newList.append(i)
        return newList

def replaceKeys(data):
    newen = {}
    #print type(data)

    if type(data) is dict:
        for v,k in data.items():
            #print "'"+str(type(k))+"'" , "veee"
            ez = str(type(data))
            #print ez , "ez"
            #print ez.split("'")[1]
            if type(k) is ObjectId:
                k = str(k)

            if v == "id":
                k = str(k)
            try:
                if v == "_id":
                    k = k["$oid"]
                    v = "id"
            except:
                k = k
                v = "id"
                pass
            if v == "id" and type(k) is dict:
                if k.get("$oid"):
                    k = k.get("$oid")
            if type(k) is dict:
                #print "dict",type(k)
                if k.get("$oid"):
                    k = k.get("$oid")
            if type(k) is list:
                newList = replaceListToDict(k)

                k  = newList
            elif type(k) is dict:
                k = replaceKeys(k)


            newen.update({v:k})
    elif type(data) is list:
        newen = replaceListToDict(data)

    return newen





def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        abort = 0
        try:
            import json
            data = json.loads(request.data)
            #print data
            if data.get("_csrf_token"):
                if not token or token != data.get('_csrf_token'):
                    abort = 1
            else:
                abort = 1
        except Exception as e:
            #print e

            #print token , request.form.get('_csrf_token')
            if token is not None:
                if not token or token != request.form.get('_csrf_token'):
                    abort = 1
        if abort:
            sendAbort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']



def loginreq(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
    return decorated_function


def render_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rv = f(*args, **kwargs)
        try:
            if rv.get("data") is None:
                rv.update({"data":{}})
        except:
            from werkzeug.wrappers import Response
            if  type(rv) is Response:
                return rv
        if type(rv.get("data")) is list:
            rv = {"data":{"results":rv.get("data")}}
        csrf_protect()


        if type(rv) is str:
            rv = {"data":{}}
        print rv
        rv["data"].update({"csrf_token":generate_csrf_token()})

        path = os.path.dirname(__file__) + "/../static/app/"
        path =  os.path.abspath(path)

        jslist = []
        jsmodules = []
        for i in os.listdir(path):
            if os.path.isdir(path+"/"+i):

                for z in os.listdir(os.path.abspath(path+"/"+i)):
                    if z.find(".js") > -1:
                        jslist.append(i+"/"+z)
                        if z == "app.js":
                            data_app = open(path+"/"+i+"/"+z).read().split('angular.module("')[1].split('"')[0]
                            jsmodules.append(data_app)
        jslist.sort();
        rv["data"].update({"jspaths":jslist,"jsmodules":jsmodules})

        if request.args.get("wt"):
            del rv["data"]["jspaths"]
            del rv["data"]["jsmodules"]
            if request.args.get("wt") == "json":



                return fResponse(json_util.dumps(replaceKeys(rv.get("data"))),mimetype="text/json")
            if request.args.get("wt") == "xml":
                xml = dict2xml({"response":replaceKeys(rv.get("data"))})
                return xml.display()
        else:
            if rv.get("redirect"):
                return redirect(rv.get("redirect"))
            if rv.get("template"):
                return render_template(rv.get("template"),**rv["data"])
            else:
                #print "json"
                del rv["data"]["jspaths"]
                del rv["data"]["jsmodules"]
                return fResponse(json_util.dumps(replaceKeys(rv.get("data"))),mimetype="text/json")



    return decorated_function
