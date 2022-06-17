from flask import url_for
from flaskblog import mail
import datetime
from flask_mail import Message

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
