from flask import render_template, redirect, url_for, request, flash
from ..models import User
import os
from datetime import datetime
from . import auth_blueprint


@auth_blueprint.route('/reset_password')
def reset_password():
    return render_template("reset_password.html")


@auth_blueprint.route('/reset_password', methods=['POST'])
def reset_password_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Could not find a user with that email address.', "danger")
        return redirect(url_for("auth.reset_password"))
    user.password_reset_code = str(os.urandom(16))
    user.latest_auth_email = datetime.now()
    return redirect(url_for('email_updates.main'))
