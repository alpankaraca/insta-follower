
__author__ = 'cankemik'
from flask import Blueprint, render_template, abort, current_app, request, session, redirect

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def welcome():
    print session['instagram_access_token']
    return "instagram api"