from blog import db


class BlogPost(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # post_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # comment_id = db.relationship("CommentDB", backref="post_comments")

    # def __init__(self, post_id, title, subtitle, date, body, img_url, author):
    #     self.title = title
    #     self.post_id = post_id
    #     self.subtitle = subtitle
    #     self.date = date
    #     self.body = body
    #     self.img_url = img_url
    #     self.author = author
    #     # self.comment_id = comment_id

    def __repr__(self):
        return f"Post(id: {self.id}, title: {self.title}, subtitle: {self.subtitle})"


class CommentDB(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, unique=False, nullable=False)
    # user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
    # post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    # def __init__(self, comment, user_name, post_id):
    #     self.comment = comment
    #     self.post_id = post_id
    #     self.user_name = user_name
