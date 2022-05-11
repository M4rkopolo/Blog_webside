from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
basedir = os.path.abspath(os.path.dirname(__file__))
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(1000))
    image_file = db.Column(db.String(30), nullable=False, default="default.jpg")
    posts = db.relationship("BlogPost", backref="user")
    comments = db.relationship("CommentDB", backref="post")

    def __init__(self, email, password, user_name):
        self.email = email.lower()
        self.user_name = user_name
        self.password = generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=5)

    def __repr__(self):
        return f"List(id: {self.id}, email: {self.email}, posts: {self.posts}, user_name:{self.user_name})"


class BlogPost(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_id = db.relationship("CommentDB", backref="postt")

    def __init__(self, post_id, title, subtitle, date, body, img_url, author):
        self.title = title
        self.post_id = post_id
        self.subtitle = subtitle
        self.date = date
        self.body = body
        self.img_url = img_url
        self.author = author
        #self.comment_id = comment_id

    def __repr__(self):
        return f"Post(id: {self.id}, title: {self.title}, subtitle: {self.subtitle})"


class CommentDB(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, comment, user_id, post_id):
        self.comment = comment
        self.post_id = post_id
        self.user_id = user_id

#db.create_all()

##WTForm
class NewUser(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Create new Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Add Comment")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    new_user = NewUser()
    if new_user.validate_on_submit():
        # add check if user already exist
        new_user_db = User(
            user_name=new_user.user_name.data,
            email=new_user.email.data,
            password=new_user.password.data,)
        db.session.add(new_user_db)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('register.html', form=new_user, logged_in=current_user.is_authenticated)


# add is_logged to hide some buttons while logged

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    password = login_form.password.data
    email = login_form.email.data
    user = User.query.filter_by(email=email).first()
    if login_form.validate_on_submit():
        if not user:
            flash("User with this address email does not exist")
            return render_template('login.html',
                                   flash=flash,
                                   form=login_form,)
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Wrong Password")
                return render_template('login.html',
                                       flash=flash,
                                       form=login_form,
                                       logged_in=current_user.is_authenticated)
    return render_template('login.html',
                            form=login_form,
                            logged_in=current_user.is_authenticated)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html",
                           all_posts=posts,
                           logged_in=current_user.is_authenticated)


##RENDER POST USING DB
@app.route("/post/<int:id>")
def show_post(id):
    comments_form = CommentForm()
    requested_post = BlogPost.query.get(id)
    rights = False
    if current_user.is_authenticated:
        rights = True if current_user.id == requested_post.post_id else False
    return render_template("post.html",
                           post=requested_post,
                           logged_in=current_user.is_authenticated,
                           have_rights = rights,
                           form = comments_form)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/delete/<int:id>", )
@login_required
def delete(id):
    delete_post = BlogPost.query.get(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/new_post", methods=["GET", "POST"])
@login_required
def add_new_post():
    new_post_form = CreatePostForm()
    user_id = current_user.id
    if new_post_form.validate_on_submit():
       new_post_db = BlogPost(
                            title=new_post_form.title.data,
                            subtitle=new_post_form.subtitle.data,
                            author=current_user.user_name,
                            img_url=new_post_form.img_url.data,
                            date=date.today().strftime("%B %d, %Y"),
                            body=new_post_form.body.data,
                            post_id = user_id)
       db.session.add(new_post_db)
       db.session.commit()
       return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=new_post_form, logged_in=current_user.is_authenticated)


@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    to_edit_post_form = CreatePostForm(
                            title=post.title,
                            subtitle=post.subtitle,
                            img_url=post.img_url,
                            body=post.body,)
    if to_edit_post_form.validate_on_submit():
        post.title = to_edit_post_form.title.data
        post.subtitle = to_edit_post_form.subtitle.data
        post.author = current_user.user_name
        post.img_url = to_edit_post_form.img_url.data
        post.body = to_edit_post_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", id=post.id))
    return render_template("make-post.html", form=to_edit_post_form, logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
