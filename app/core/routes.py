from datetime import datetime

from flask import (current_app, flash, g, jsonify, redirect, render_template,
                   request, url_for)
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from langdetect import LangDetectException, detect

from app import db
from app.core import core_bp
from app.core.forms import EditProfileForm, EmptyForm, PostForm
from app.models import Post, User
from app.translate import translate


@core_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())


@core_bp.route("/", methods=["GET", "POST"])
@core_bp.route("/index", methods=["GET", "POST"])
@login_required
def index() -> str:
    """Route for displaying index page and sending posts.

    GET request allows to see paginated index page.
    POST request allows to create a post and send it to database.

    Returns:
        str: HTML template
    """

    form = PostForm()

    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ""

        post = Post(body=form.post.data, author=current_user, language=language)

        db.session.add(post)
        db.session.commit()

        flash(_("Your post is now live!"))
        return redirect(url_for("index"))

    page = request.args.get("page", default=1, type=int)

    posts = current_user.followed_posts().paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )

    return render_template(
        "index.html",
        title=_("Home"),
        form=form,
        posts=posts.items,
        next_url=url_for("index", page=posts.next_num) if posts.has_next else None,
        prev_url=url_for("index", page=posts.prev_num) if posts.has_prev else None,
    )


@core_bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )

    return render_template(
        "index.html",
        title=_("Explore"),
        posts=posts.items,
        next_url=url_for("explore", page=posts.next_num) if posts.has_next else None,
        prev_url=url_for("explore", page=posts.prev_num) if posts.has_prev else None,
    )


@core_bp.route("/user/<username>")
@login_required
def user(username: str) -> str:
    """Route for displaying user profile.

    Args:
        username (str)

    Returns:
        str: HTML template
    """

    page = request.args.get("page", default=1, type=int)

    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False
    )

    form = EmptyForm()

    next_url = (
        url_for("user", username=user.username, page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for("user", username=user.username, page=posts.prev_num)
        if posts.has_prev
        else None
    )

    return render_template(
        "user.html",
        form=form,
        posts=posts.items,
        user=user,
        next_url=next_url,
        prev_url=prev_url,
    )


@core_bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        db.session.commit()

        flash(_("Your changes have been saved."))
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title=_("Edit Profile"), form=form)


@core_bp.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("index"))

        if user == current_user:
            flash(_("You can't follow yourself!"))
            return redirect(url_for("user", username=username))

        current_user.follow(user)
        db.session.commit()

        flash(_("You are now following %(username)s!", username=username))
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("index"))


@core_bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("index"))

        if user == current_user:
            flash(_("You can't unfollow yourself!"))
            return redirect(url_for("user", username=username))

        current_user.unfollow(user)
        db.session.commit()

        flash(_("You are now not following %(username)s.", username=username))
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("index"))


@core_bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    return jsonify(
        {
            "text": translate(
                request.form["text"],
                request.form["source_language"],
                request.form["target_language"],
            )
        }
    )
