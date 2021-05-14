from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from project import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(124), unique=True, nullable=False)
    username = db.Column(db.String(124), unique=True, nullable=False)
    password_hash = db.Column(db.String(164), nullable=False)
    profile_picture = db.Column(db.String(124), default="default.jpg")
    posts = db.relationship("Posts", backref="author", lazy="dynamic")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(124), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    county = db.Column(db.String(124), nullable=False)
    quadrature = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(124), nullable=False)
    sale_rent = db.Column(db.String(124), nullable=False)
    property_pictures = db.Column(db.String(1000), default="default_property.png")

    def __init__(self, user_id, title, text, county, quadrature, price, property_type, sale_rent, property_pictures):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.county = county
        self.quadrature = quadrature
        self.price = price
        self.property_type = property_type
        self.sale_rent = sale_rent
        self.property_pictures = property_pictures

