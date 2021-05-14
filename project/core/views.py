from flask import Blueprint, render_template, request, session, redirect, url_for
from project.models import Posts
from project.core.forms import FilterForm

core = Blueprint("core", __name__)


@core.route("/", methods=["GET", "POST"])
def home():
    form = FilterForm()
    page = request.args.get("page", 1, type=int)
    post = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=6)
    all_posts = Posts.query.all()
    return render_template("home.html", form=form, page=page, post=post, all_posts=all_posts)


@core.route("/about")
def about():
    return render_template("about.html")