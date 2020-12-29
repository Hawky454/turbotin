from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import current_user
from werkzeug.security import generate_password_hash
from ..models import User
from .. import db
from . import send_email_safely, create_code

reset_password_blueprint = Blueprint("reset_password", __name__)


def send_password_reset_code(user):
    url = request.url_root + url_for("reset_password.create_new_password", user_id=user.id,
                                     password_reset_code=user.password_reset_code)
    subject = "Your TurboTin.com password reset code"
    body = "Use this url to create a new password: {}".format(url)
    return send_email_safely(user, subject, body)


@reset_password_blueprint.route('/reset_password')
def reset_password():
    return render_template("reset_password.html")


@reset_password_blueprint.route('/reset_password', methods=['POST'])
def reset_password_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Could not find a user with that email address.', "danger")
        return redirect("/reset_password")
    old_code = user.password_reset_code
    user.password_reset_code = create_code()
    password_sent = send_password_reset_code(user)
    if not password_sent:
        user.password_reset_code = old_code
    db.session.commit()
    return redirect("/reset_password")


@reset_password_blueprint.route('/create_new_password/<user_id>/<password_reset_code>')
def create_new_password(user_id, password_reset_code):
    user = User.query.filter_by(id=user_id).first()
    if password_reset_code != user.password_reset_code:
        return "Incorrect code"
    return render_template("create_new_password.html")


@reset_password_blueprint.route('/create_new_password/<user_id>/<password_reset_code>', methods=["POST"])
def create_new_password_post(user_id, password_reset_code):
    user = User.query.filter_by(id=user_id).first()
    if password_reset_code != user.password_reset_code:
        return "Incorrect code"
    new_password = request.form.get("password")
    user.password = generate_password_hash(new_password, method='sha256')
    db.session.commit()
    flash("New password created", "success")
    if current_user.is_authenticated:
        return redirect("/email_updates")
    else:
        return redirect("/login")
