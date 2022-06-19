from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from users.db_model import User
# from flaskblog.modules import User

class NewUser(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Create new Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ResetPasword(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Reset Password")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash("There is no account which this email")


class NewPassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Set new password")
