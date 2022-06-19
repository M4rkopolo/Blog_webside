from main import login_manager, db
from users.db_model import User
from users.forms import NewUser,NewPassword, LoginForm, ResetPasword
from util.utils import send_reset_email
from flask_login import login_user, current_user, logout_user
from flask import render_template, redirect, url_for, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint("users", __name__,)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@users.route('/register', methods=['GET', 'POST'])
def register():
    new_user = NewUser()
    if new_user.validate_on_submit():
        new_user_db = User(
            user_name=new_user.user_name.data,
            email=new_user.email.data,
            password=new_user.password.data, )
        db.session.add(new_user_db)
        db.session.commit()
        return redirect(url_for('posts.get_all_posts'))
    return render_template('register.html', form=new_user, logged_in=current_user.is_authenticated)

@users.route('/login', methods=['GET', 'POST'])
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
                                   form=login_form)
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("posts.get_all_posts"))
            else:
                flash("Wrong Password")
                return render_template('login.html',
                                       flash=flash,
                                       form=login_form,
                                       logged_in=current_user.is_authenticated)
    return render_template('login.html',
                           form=login_form,
                           logged_in=current_user.is_authenticated)

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('posts.get_all_posts'))

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset password")
        return redirect(url_for('posts.login'))
    return render_template('reset_password.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
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
        return redirect(url_for('users.login'))
    return render_template('new_password.html', form=form, logged_in=current_user.is_authenticated)
