from model.Follower import Follower

__author__ = 'cankemik'
from flask import Blueprint, render_template, abort, current_app, request, session, redirect, url_for

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def welcome():
    #print session['instagram_user']
    #print session['instagram_access_token']
    return "<a href='/instagram/connect'>Connect</a>"
