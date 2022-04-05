from flask import render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import app, lm
from .models import *
from .forms import *


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.save()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id)
        return render_template("index.html", notes=notes)
    return render_template("index.html")


@login_required
@app.route("/note/create", methods=["GET", "POST"])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            id=current_user.id, title=form.title.data, content=form.content.data
        )
        note.save()
        return redirect(url_for("index"))
    return render_template("create-note.html", form=form)


@login_required
@app.route("/note/<id>")
def note(id):
    note = Note.query.get(int(id))
    return render_template("note.html", note=note)


@login_required
@app.route("/list/create/<id>", methods=["GET", "POST"])
def create_list(id):
    form = ListForm()
    if form.validate_on_submit():
        list = List(id=id, title=form.title.data, content=form.content.data)
        list.save()
        return redirect(url_for("note", id=id))
    return render_template("create-list.html", form=form, id=id)


@login_required
@app.route("/item/create/<id>", methods=["GET", "POST"])
def create_item(id):
    form = ListItemForm()
    if form.validate_on_submit():
        item = ListItem(id=id, content=form.content.data)
        item.save()
        return redirect(url_for("index"))
    return render_template("create-item.html", form=form, id=id)
