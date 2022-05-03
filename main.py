from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


##RENDER POST USING DB
@app.route("/post/<int:id>")
def show_post(id):
    requested_post = BlogPost.query.get(id)
    return render_template("post.html", post=requested_post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/delete/<int:id>",)
def delete(id):
    delete_post = BlogPost.query.get(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/new_post", methods=["GET", "POST"])
def add_new_post():
    new_post_form = CreatePostForm()
    if new_post_form.validate_on_submit():
        new_post_db = BlogPost(
            title= new_post_form.title.data,
            subtitle = new_post_form.subtitle.data,
            author = new_post_form.author.data,
            img_url = new_post_form.img_url.data,
            date= date.today().strftime("%B %d, %Y"),
            body = new_post_form.body.data,)
        db.session.add(new_post_db)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=new_post_form)

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    to_edit_post_form = CreatePostForm(
            title= post.title,
            subtitle= post.subtitle,
            author= post.author,
            img_url= post.img_url,
            body= post.body,)

    if to_edit_post_form.validate_on_submit():
        post.title=to_edit_post_form.title.data
        post.subtitle=to_edit_post_form.subtitle.data
        post.author=to_edit_post_form.author.data
        post.img_url=to_edit_post_form.img_url.data
        post.body=to_edit_post_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", id=post.id))
    return render_template("make-post.html", form=to_edit_post_form)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)