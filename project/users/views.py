from flask import Blueprint, render_template, redirect, url_for, flash, request
from project.users.forms import RegisterForm, LoginForm, ProfileForm
from project.models import Users, Posts
from project import db, basedir
from flask_login import login_user, login_required, logout_user, current_user
import secrets, os
from PIL import Image


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in!")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("core.home", user=user))
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + ext
    picture_path = os.path.join(basedir, "static/profile_pictures", picture_filename)
    picture_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(picture_size)
    i.save(picture_path)
    return picture_filename


@users.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            file_picture = save_picture(form.picture.data)
            current_user.profile_picture = file_picture

        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash("Your info has been updated!")
        return redirect(url_for("users.profile"))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username

    picture_file = url_for("static", filename="profile_pictures/" + current_user.profile_picture)
    page = request.args.get("page", 1, type=int)
    post = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=6)
    return render_template("profile.html", form=form, picture_file=picture_file, page=page, post=post)


@users.route("/<username>posts", methods=["GET", "POST"])
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    post = Posts.query.filter_by(author=user).order_by(Posts.date.desc()).paginate(page=page, per_page=6)
    picture_file = url_for("static", filename="profile_pictures/" + user.profile_picture)
    return render_template("user_posts.html", post=post, user=user, picture_file=picture_file)
