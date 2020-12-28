from flask import Blueprint, redirect
from flask_login import logout_user, login_required
from scripts.email_methods import send_email
from datetime import datetime

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def send_email_safely(user, subject, body):
    if user.latest_auth_email and user.latest_auth_email - datetime.now():
        None
