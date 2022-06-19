# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# # from flaskblog import current_app
# from werkzeug.security import generate_password_hash
# from flaskblog.util.utils import PSTNow
#
# db = SQLAlchemy()
#
# class Note(db.Model):
#     __tablename__ = "kanban_note"
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(100), nullable=False)
#     stage_name = db.Column(db.String(30), db.ForeignKey('kanban_stage.name'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     date = db.Column(db.String, default=PSTNow)
#     kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))
#
#     def __init__(self, content, stage_name, user_id,kanban_table):
#         self.content = content
#         self.stage_name = stage_name
#         self.user_id = user_id
#         self.kanban_table = kanban_table
#
#
# class Stage(db.Model):
#     __tablename__ = "kanban_stage"
#
#     id = db.Column(db.Integer, primary_key=True)
#     notes = db.relationship("Note", backref="stage")
#     name = db.Column(db.String(30), nullable=False)
#     inside_kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))
#
#
# # user_name = db.Column(db.String, db.ForeignKey(user_name))
#
# class Kanban_Table(db.Model):
#     __tablename__ = "kanban_table"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     description = db.Column(db.String)
#     stages = db.relationship("Stage", backref="kanban_table")
#     notes = db.relationship("Note", backref="kanban_notes")
#     owner_user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
#     # access_users_name = db.Column(db.String, db.ForeignKey('users.user_name'))
#
#
# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     user_name = db.Column(db.String(1000))
#     image_file = db.Column(db.String(30), nullable=False, default="default.jpg")
#     posts = db.relationship("BlogPost", backref="user")
#     comments = db.relationship("CommentDB", backref="post")
#     kanban_table_own = db.relationship("Kanban_Table", backref="table_owner_user")  ##################
#     kanban_table_note = db.relationship("Note", backref="note_owner_user")  ##################
#
#     # kanban_table_access = db.relationship("Kanban_Table", backref="table_access_user")  ##########
#
#     def __init__(self, email, password, user_name):
#         self.email = email.lower()
#         self.user_name = user_name
#         self.password = generate_password_hash(password,
#                                                method='pbkdf2:sha256',
#                                                salt_length=5)
#
#     def __repr__(self):
#         return f"List(id: {self.id}, email: {self.email}, posts: {self.posts}, user_name:{self.user_name})"
#
#     # def get_reset_token(self, expires_time=100):
#     #     s = Serializer(current_app.config['SECRET_KEY'], expires_time)
#     #     return s.dumps({"user_id": self.id}).decode('utf-8')
#
#     # @staticmethod
#     # def verify_reset_token(token):
#     #     s = Serializer(current_app.config['SECRET_KEY'])
#     #     try:
#     #         user_id = s.loads(token)["user_id"]
#     #     except:
#     #         return None
#     #     return User.query.get(user_id)
#
#
# class BlogPost(db.Model):
#     __tablename__ = 'posts'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     author = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     comment_id = db.relationship("CommentDB", backref="postt")
#
#     def __init__(self, post_id, title, subtitle, date, body, img_url, author):
#         self.title = title
#         self.post_id = post_id
#         self.subtitle = subtitle
#         self.date = date
#         self.body = body
#         self.img_url = img_url
#         self.author = author
#         # self.comment_id = comment_id
#
#     def __repr__(self):
#         return f"Post(id: {self.id}, title: {self.title}, subtitle: {self.subtitle})"
#
#
# class CommentDB(db.Model):
#     __tablename__ = 'comments'
#
#     id = db.Column(db.Integer, primary_key=True)
#     comment = db.Column(db.String, unique=False, nullable=False)
#     user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
#
#     def __init__(self, comment, user_name, post_id):
#         self.comment = comment
#         self.post_id = post_id
#         self.user_name = user_name
