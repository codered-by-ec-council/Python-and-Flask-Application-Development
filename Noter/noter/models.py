from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model, UserMixin):
    """Manages the Users in the application"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    active = db.Column(db.Boolean, default=True)
    notes = db.relationship("Note", backref="user", lazy="dynamic")

    def __str__(self):
        return self.username

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()


class Note(db.Model):
    """Manages the notes"""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    lists = db.relationship("List", backref="note", lazy="dynamic")

    def __init__(self, id, title, content):
        self.user_id = id
        self.title = title
        self.content = content

    def save(self):
        db.session.add(self)
        db.session.commit()


class List(db.Model):
    """Manages the Lists"""

    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    title = db.Column(db.String(255), nullable=False)
    list_description = db.Column(db.Text, nullable=False)
    items = db.relationship("ListItem", backref="list", lazy="dynamic")
    created_on = db.Column(db.DateTime, default=func.now())

    def __init__(self, id, title, content):
        self.note_id = id
        self.title = title
        self.list_description = content

    def save(self):
        db.session.add(self)
        db.session.commit()


class ListItem(db.Model):
    """Manages the List Items"""

    __tablename__ = "list_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"))
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())

    def __init__(self, id, content):
        self.list_id = id
        self.content = content

    def save(self):
        db.session.add(self)
        db.session.commit()
