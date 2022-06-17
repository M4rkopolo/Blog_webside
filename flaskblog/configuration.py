import os

class Config():
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.poczta.onet.pl'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "xxx@email.pl"
    MAIL_PASSWORD = "xxx"