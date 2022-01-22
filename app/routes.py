from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {"username": "Ilya"}
    posts = [
        {
            "author": {"username": "Alexey"},
            "body": "Beautiful day in Domodedovo!",
        },
        {
            "author": {"username": "Grigory"},
            "body": "The Green Elephant movie was so cool!",
        },
    ]
    return render_template(
        "index.html",
        title="Home",
        user=user,
        posts=posts
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("index")

        return redirect(next)

    return render_template(
        "login.html",
        title="Sign In",
        form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
