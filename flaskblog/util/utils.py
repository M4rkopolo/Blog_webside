import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date
import datetime
from flask_mail import Mail, Message



def now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def astimezone(d, offset):
    return d.astimezone(datetime.timezone(datetime.timedelta(hours=offset)))

def PDTNow():
    return str(astimezone(now(), -7))

def PSTNow():
    return str(astimezone(now(), -8))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request",
                  sender='mariusztest123@op.pl',
                  recipients=[user.email])
    msg.body = f'''To reset your password viset following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no chnge password 
{user.user_name} {user.password}'''
    mail.send(msg)
