import email
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from . import app, lm, mail
from .models import *
from .forms import *

@lm.user_loader
def load_user(user_id):
    return Author.query.get(user_id)

#auth views
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Author.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('profile', name=user.username))
    return render_template('login.html', form=form)

@app.route("/create-author", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = Author(form.username.data, form.email.data, form.password.data)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Reader views 
@app.route("/")
def index():
    posts = Post.query.filter_by(is_draft=False)
    return render_template('index.html', posts=posts)

@app.route("/post/<id>", methods=['GET', 'POST'])
def view_post(id):
    post = Post.query.get(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post.id, form.content.data)
        comment.save()
        msg = Message(
            'A new comment',
            recipients=[current_user.email],
            body='There is a new comment on your post'
        )
        # mail.send(msg)
        print("Message sent")
        return redirect(url_for('view_post', id=post.id))
    return render_template('post.html', post=post, form=form)

@app.route("/about")
def about():
    return "<h1>About me</h1>"

# Author Views
@app.route("/profile/<name>")
@login_required
def profile(name):
    posts = Post.query.filter_by(author_id=current_user.id)
    return render_template('me.html', posts=posts)

@app.route("/post/create/", methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(current_user.id, form.title.data, form.content.data)
        post.save()
        return redirect(url_for('profile', name=current_user))
    return render_template('create.html', form=form)

@app.route("/post/publish/<id>")
@login_required
def publish(id):
    post = Post.query.get(id)
    post.is_draft = not post.is_draft
    post.save()
    return redirect(url_for('profile', name=current_user))

@app.route("/post/update/<id>")
@login_required
def update(id):
    # TODO Get the profile
    return render_template('me.html')

