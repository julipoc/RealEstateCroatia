from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField
from project.models import Users
from flask_login import current_user


class RegisterForm(FlaskForm):
    email = StringField("", validators=[DataRequired(), Email()])
    username = StringField("", validators=[DataRequired()])
    password = PasswordField("", validators=[DataRequired(), EqualTo("confirm_password",
                                                                             message="Passwords must match"),
                                                     Length(min=6, max=20)])
    confirm_password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        if Users.query.filter_by(email=email.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first():
            raise ValidationError("Your username has been registered already!")


class LoginForm(FlaskForm):
    email = StringField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField("Profile picture", validators=[FileAllowed(["png", "jpg"])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            if Users.query.filter_by(email=email.data).first():
                raise ValidationError("Your email has been registered already!")

    def validate_username(self, username):
        if username.data != current_user.username:
            if Users.query.filter_by(username=username.data).first():
                raise ValidationError("Your username has been registered already!")
