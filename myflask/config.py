import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'this-is-some-wild-key'

SQLALCHEMY_TRACK_MODIFICATIONS = False
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'myflask.db')
else:
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
     
MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USERNAME = "achim"
MAIL_PASSWORD = "testpassword"