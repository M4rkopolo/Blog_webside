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
app.config['MAIL_SERVER'] = 'smtp.poczta.onet.pl'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "xxx@email.pl"
app.config['MAIL_PASSWORD'] = "xxx"
mail = Mail(app)


def now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def astimezone(d, offset):
    return d.astimezone(datetime.timezone(datetime.timedelta(hours=offset)))


def PDTNow():
    return str(astimezone(now(), -7))


def PSTNow():
    return str(astimezone(now(), -8))


##CONFIGURE TABLE

class Note(db.Model):
    __tablename__ = "kanban_note"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    stage_name = db.Column(db.String(30), db.ForeignKey('kanban_stage.name'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String, default=PSTNow)
    kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))

    def __init__(self, content, stage_name, user_id,kanban_table):
        self.content = content
        self.stage_name = stage_name
        self.user_id = user_id
        self.kanban_table = kanban_table


class Stage(db.Model):
    __tablename__ = "kanban_stage"

    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship("Note", backref="stage")
    name = db.Column(db.String(30), nullable=False)
    inside_kanban_table = db.Column(db.Integer, db.ForeignKey('kanban_table.id'))


# user_name = db.Column(db.String, db.ForeignKey(user_name))

class Kanban_Table(db.Model):
    __tablename__ = "kanban_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String)
    stages = db.relationship("Stage", backref="kanban_table")
    notes = db.relationship("Note", backref="kanban_notes")
    owner_user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
    # access_users_name = db.Column(db.String, db.ForeignKey('users.user_name'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(1000))
    image_file = db.Column(db.String(30), nullable=False, default="default.jpg")
    posts = db.relationship("BlogPost", backref="user")
    comments = db.relationship("CommentDB", backref="post")
    kanban_table_own = db.relationship("Kanban_Table", backref="table_owner_user")  ##################
    kanban_table_note = db.relationship("Note", backref="note_owner_user")  ##################

    # kanban_table_access = db.relationship("Kanban_Table", backref="table_access_user")  ##########

    def __init__(self, email, password, user_name):
        self.email = email.lower()
        self.user_name = user_name
        self.password = generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=5)

    def __repr__(self):
        return f"List(id: {self.id}, email: {self.email}, posts: {self.posts}, user_name:{self.user_name})"

    def get_reset_token(self, expires_time=100):
        s = Serializer(app.config['SECRET_KEY'], expires_time)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


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
        # self.comment_id = comment_id

    def __repr__(self):
        return f"Post(id: {self.id}, title: {self.title}, subtitle: {self.subtitle})"


class CommentDB(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, unique=False, nullable=False)
    user_name = db.Column(db.String, db.ForeignKey('users.user_name'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, comment, user_name, post_id):
        self.comment = comment
        self.post_id = post_id
        self.user_name = user_name


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


class ResetPasword(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Reset Password")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash("There is no account which this email")


class NewPassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Set new password")


class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Add Comment")


class NoteForm(FlaskForm):
    # note_name = StringField("Note_Name", validators=[DataRequired()])
    note_content = StringField("Note_Content", validators=[DataRequired()])
    submit = SubmitField("Add Note")


class KanbanStageForm(FlaskForm):
    stage_name = StringField("Stage_Name", validators=[DataRequired()])
    submit = SubmitField("Add stage")


class KanbanForm(FlaskForm):
    kanban_table_name = StringField("Table_Name", validators=[DataRequired()])
    kanban_table_descripton = StringField("Table_Descripton")
    # kanban_access_users = StringField("Accesed_Users", validators=[DataRequired()])
    submit = SubmitField("Add Kanban Table")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset password")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("THat is an invalid or expired token")
        return redirect(url_for('reset_password'))
    form = NewPassword()
    if form.validate_on_submit():
        new_password = generate_password_hash(form.password.data,
                                              method='pbkdf2:sha256',
                                              salt_length=5)
        user.password = new_password
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('new_password.html', form=form, logged_in=current_user.is_authenticated)


@app.route("/kanban_tables", methods=["GET", "POST"])
@login_required
def kanban_tables_overview():
    form = KanbanForm()
    tables = Kanban_Table.query.filter_by(owner_user_name=current_user.user_name).all()
    if form.validate_on_submit():
        new_kanban_table = Kanban_Table(name=form.kanban_table_name.data,
                                        description=form.kanban_table_descripton.data,
                                        # access_users_name=form.kanban_access_users.data,
                                        owner_user_name=current_user.user_name)

        db.session.add(new_kanban_table)
        db.session.commit()
        first_stage = Stage(
            name="to do",
            inside_kanban_table=new_kanban_table.id)
        db.session.add(first_stage)
        db.session.commit()
        return redirect(url_for('kanban_tables_overview'))
    return render_template("kanban_table_overview.html", form=form, tables=tables, logged_in=current_user.is_authenticated)


@app.route("/kanban_table/<int:id>", methods=["GET", "POST"])
@login_required
def kanban_table(id):
    note_form = NoteForm()
    stage_form = KanbanStageForm()
    exist_stages = Stage.query.filter_by(inside_kanban_table=id).all()
    notes = Note.query.filter_by(kanban_table=id)
    if note_form.validate_on_submit():
        new_note = Note(
            content=note_form.note_content.data,
            stage_name=exist_stages[0].name,
            user_id=current_user.id,
            kanban_table=id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('kanban_table', id=id))
    if stage_form.validate_on_submit():
        new_stage = Stage(name = stage_form.stage_name.data,
                          inside_kanban_table = id)
        db.session.add(new_stage)
        db.session.commit()
        return redirect(url_for('kanban_table', id=id))
    return render_template("kanban_table.html", note_form=note_form, stage_form=stage_form, stages=exist_stages,
                           notes=notes, logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    new_user = NewUser()
    if new_user.validate_on_submit():
        # add check if user already exist
        new_user_db = User(
            user_name=new_user.user_name.data,
            email=new_user.email.data,
            password=new_user.password.data, )
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
                                   form=login_form, )
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
@app.route("/post/<int:id>", methods=['GET', 'POST'])
def show_post(id):
    comments_form = CommentForm()
    requested_post = BlogPost.query.get(id)
    comments = CommentDB.query.filter_by(post_id=id).all()
    rights = False
    if current_user.is_authenticated:
        rights = True if current_user.id == requested_post.post_id else False
    if comments_form.validate_on_submit() and current_user.is_authenticated:
        print("current_user.user_name")
        new_comment = CommentDB(comment=comments_form.comment.data,
                                user_name=current_user.user_name,
                                post_id=id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', id=id))
    return render_template("post.html",
                           post=requested_post,
                           all_comments=comments,
                           logged_in=current_user.is_authenticated,
                           have_rights=rights,
                           form=comments_form)


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_post = BlogPost.query.get(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/delete_note", methods=["GET"])
def delete_note():
    id = request.args.get('id')
    id_table = request.args.get("id_table")
    note_id = Note.query.filter_by(id=id).first()
    db.session.delete(note_id)
    db.session.commit()
    return redirect(url_for('kanban_table', id=id_table))

@app.route("/move_note", methods=["GET"])
def move_note():
    id = request.args.get('id')
    id_table = request.args.get("id_table")
    note_id = Note.query.filter_by(id=id).first()
    print(request.args.get('stage'))
    note_id.stage_name = request.args.get('stage')
    # db.session.delete(note_id)
    db.session.commit()
    return redirect(url_for('kanban_table', id=id_table))

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
            post_id=user_id)
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
        body=post.body, )
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
