from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from blog import db
from blog.main.configuration import Config
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(1000))
    image_file = db.Column(db.String(30), nullable=False, default="default.jpg")
    posts = db.relationship("BlogPost", backref="user_posts")
    comments = db.relationship("CommentDB", backref="user_comments")
    kanban_table_own = db.relationship("Kanban_Table", backref="user_tables")
    kanban_table_note = db.relationship("Note", backref="user_notes")


    def __init__(self, email, password, user_name):
        self.email = email.lower()
        self.user_name = user_name
        self.password = generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=5)

    def __repr__(self):
        return f"List(id: {self.id}, email: {self.email}, posts: {self.posts}, user_name:{self.user_name})"

    def get_reset_token(self, expires_time=100):
        s = Serializer(Config.SECRET_KEY, expires_time)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
