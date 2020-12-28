from . import auth_blueprint
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user
from ..models import User


@auth_blueprint.route('/login')
def login():
    return render_template("login.html")


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', "danger")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('email_updates.main'))
