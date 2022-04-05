from flask import Flask
from flask_restx import Api
from flask_jwt import JWT
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "my-secret"
app.debug = True

toolbar = DebugToolbarExtension(app)

from .auth import authenticate, identity

jwt = JWT(app, authenticate, identity)

from .resources import *

api.add_resource(ArticleList, "/articles")
api.add_resource(Article, "/article/<int:index>")
api.add_resource(HelloWorld, "/")
