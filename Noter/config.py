import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_TRACK_MODIFICATIONS = False
if os.environ.get("DATABASE_URL") is None:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "noter.db")
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
