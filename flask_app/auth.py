from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import os
import json

from scripts.email_methods import send_email_confirmation_code

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login')
def login():
    return render_template("login.html")


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('email_updates.main'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@auth_blueprint.route('/signup')
def signup():
    return render_template("signup.html")


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = " ".join([n.title() for n in str(email).split("@")[0].split(".")])
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    # if a user is found, we want to redirect back to signup page so user can try again
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256'),
        email_code=str(os.urandom(16)),
        email_verified=False,
        email_updates=json.dumps([])
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    send_email_confirmation_code(current_user.email, url_for("auth.verify_email", user_id=current_user.id,
                                                             email_code=current_user.email_code))

    return redirect(url_for('auth.login'))


@auth_blueprint.route('/verify_email/<user_id>/<email_code>')
@login_required
def verify_email(user_id, email_code):
    user = User.query.filter_by(id=user_id).first()
    if email_code == user.email_code:
        user.email_verified = True
        db.session.commit()
        flash('Email verified')

    return redirect("/email_updates")


@auth_blueprint.route('/resend_email')
@login_required
def resend_email():
    send_email_confirmation_code(current_user.email,
                                 request.url_root + url_for("auth.verify_email", user_id=current_user.id,
                                                            email_code=current_user.email_code))
    flash('Email sent')
    return redirect("/email_updates")
