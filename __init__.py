# from flask import Flask
# from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
# from flask_ckeditor import CKEditor
# from flask_login import LoginManager
# from flask_mail import Mail
# from configuration import Config
# # from flaskblog.modules import db
#
# ckeditor = CKEditor()
# login_manager = LoginManager()
# db = SQLAlchemy()
# mail = Mail()
#
#
# def current_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     @app.before_first_request
#     def initialize_database():
#         db.create_all()
#
#     login_manager.init_app(app)
#     Bootstrap(app)
#     db.init_app(app)
#     mail.init_app(app)
#     ckeditor.init_app(app)
#
#     from .users.routes import users
#     from .posts.routes import posts
#     from .kanban.routes import kanban
#     from .main.routes import main
#     app.register_blueprint(main)
#     app.register_blueprint(users)
#     app.register_blueprint(posts)
#     app.register_blueprint(kanban)
#
#     return app
#
# app = current_app()
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
