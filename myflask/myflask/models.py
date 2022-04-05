from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class Author(db.Model, UserMixin):
    """Manages the Authors in the application"""
    __tablename__ = "authors"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    active = db.Column(db.Boolean, default=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
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


class Post(db.Model):
    """Manages the posts"""
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    is_draft = db.Column(db.Boolean, default=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    
    def __init__(self, id, title, content):
        self.author_id = id
        self.title = title
        self.content = content
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    """Manages the comments"""
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    moderated = db.Column(db.Boolean, default=True)
    
    def __init__(self, id, content):
        self.post_id = id
        self.content = content
    
    def save(self):
        db.session.add(self)
        db.session.commit()