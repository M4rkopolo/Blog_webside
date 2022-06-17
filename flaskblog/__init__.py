from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.configuration import Config

ckeditor = CKEditor()
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()

def current_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    Bootstrap(app)
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.kanban.routes import kanban
    from flaskblog.main.routes import main
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(kanban)

    return app