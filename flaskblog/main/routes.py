from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint("main", __name__)

@main.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)

@main.route("/contact")
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)