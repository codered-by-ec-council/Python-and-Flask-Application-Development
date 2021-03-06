from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

app.debug = True

toolbar = DebugToolbarExtension(app)

from .views import *
