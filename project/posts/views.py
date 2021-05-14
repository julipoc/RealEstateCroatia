from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, session
from flask_login import login_required, current_user
from project.posts.forms import PostForm
from project.models import Posts
from project import db, basedir, app
import os
import secrets
from PIL import Image


posts = Blueprint("posts", __name__)


def save_picture(form_property_pics):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_property_pics.filename)
    picture_filename = random_hex + ext
    picture_path = os.path.join(basedir, "static/property_pictures/", picture_filename)
    picture_size = (800, 600)
    i = Image.open(form_property_pics)
    i.thumbnail(picture_size)
    i.save(picture_path)
    return picture_filename


@posts.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    session["images"] = []
    form = PostForm()
    if form.validate_on_submit():

        post = Posts(title=form.title.data,
                     text=form.text.data,
                     county=form.county.data,
                     quadrature=form.quadrature.data,
                     price=form.price.data,
                     property_type=form.property_type.data,
                     property_pictures=form.property_pics.data,
                     sale_rent=form.sale_rent.data,
                     user_id=current_user.id)

        if str(form.property_pics.data) == "[<FileStorage: '' ('application/octet-stream')>]":
            default = "default_prop.png"
            post.property_pictures = default
            session["images"].append(post.property_pictures)

        else:
            piclist = form.property_pics.data
            for pic in piclist:
                file_picture = save_picture(pic)
                post.property_pictures = file_picture
                session["images"].append(post.property_pictures)

        post.property_pictures = session["images"]
        post.property_pictures = ",".join(post.property_pictures)

        db.session.add(post)
        db.session.commit()
        flash("Your post is created!")

        return redirect(url_for("posts.read_post", post=post, post_id=post.id, images=session["images"]))
    picture_file = url_for("static", filename="profile_pictures/" + current_user.profile_picture)
    return render_template("create_post.html", form=form, picture_file=picture_file)


@posts.route("/post<int:post_id>", methods=["GET", "POST"])
def read_post(post_id):
    post = Posts.query.get_or_404(post_id)
    post_list = post.property_pictures.split(",")
    return render_template("read_post.html", post=post, post_list=post_list)


@posts.route("/update_post<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
    session["images"] = []
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.county = form.county.data
        post.quadrature = form.quadrature.data
        post.price = form.price.data
        post.property_type = form.property_type.data
        post.sale_rent = form.sale_rent.data

        if form.property_pics.data:
            if str(form.property_pics.data) == "[<FileStorage: '' ('application/octet-stream')>]":
                session["images"].append(post.property_pictures)

            else:
                piclist = form.property_pics.data
                for pic in piclist:
                    file_picture = save_picture(pic)
                    post.property_pictures = file_picture
                    session["images"].append(post.property_pictures)

        post.property_pictures = session["images"]
        post.property_pictures = ",".join(post.property_pictures)
        db.session.commit()
        flash("Your post has been updated!")
        return redirect(url_for("core.home", post_id=post.id, images=session["images"])) #, post_list2=post_list2

    elif request.method == "GET":
        form.title.data = post.title
        form.text.data = post.text
        form.county.data = post.county
        form.quadrature.data = post.quadrature
        form.price.data = post.price
        form.property_type.data = post.property_type
        form.property_pics.data = post.property_pictures
        form.sale_rent.data = post.sale_rent

    post_list = post.property_pictures.split(",")
    pic_prop = url_for("static", filename="property_pictures/" + post.property_pictures)
    return render_template("create_post.html", form=form, post_list=post_list, images=session["images"], pic_prop=pic_prop)


@posts.route("/delete_post<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("core.home"))
