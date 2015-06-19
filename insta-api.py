from flask import Flask
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
admin = Admin(app)
admin.add_view(ModelView(User, "User"))
admin.add_view(ModelView(Follower, "Follower"))

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(instagram, url_prefix="/instagram")


if __name__ == '__main__':
    app.run()
