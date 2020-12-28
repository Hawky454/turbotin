from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from ..models import User
from .. import db
import os
import json
from . import auth_blueprint


@auth_blueprint.route('/signup')
def signup():
    return render_template("signup.html")


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = " ".join([n.title() for n in str(email).split("@")[0].split(".")])
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists', "danger")
        return redirect(url_for('auth.signup'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256'),
        email_code=str(os.urandom(16)),
        email_verified=False,
        email_updates=json.dumps([])
    )

    db.session.add(new_user)
    db.session.commit()
    url = request.url_root + url_for("auth.verify_email", user_id=new_user.id, email_code=new_user.email_code)
    # send_email_confirmation_code(new_user.email, url)

    return redirect(url_for('auth.login'))
