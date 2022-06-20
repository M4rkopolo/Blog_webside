import os

class Config():
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")#, "sqlite:///blogg.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.poczta.onet.pl'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "xxx@email.pl"
    MAIL_PASSWORD = "xxx"