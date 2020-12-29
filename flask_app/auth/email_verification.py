from flask import redirect, flash, Blueprint
from ..models import User
from .. import db
from flask_login import login_required, current_user
from . import send_email_verification_code

email_verification_blueprint = Blueprint('email_verification', __name__)


@email_verification_blueprint.route('/verify_email/<user_id>/<email_code>')
def verify_email(user_id, email_code):
    user = User.query.filter_by(id=user_id).first()
    if email_code == user.email_code:
        user.email_verified = True
        db.session.commit()
        flash('Email verified', "success")
    else:
        flash("The url is incorrect, email not verified", "danger")
    if current_user.is_authenticated:
        return redirect("/email_updates")
    else:
        return redirect("/login")


@email_verification_blueprint.route('/resend_email')
@login_required
def resend_email():
    send_email_verification_code(current_user)
    if current_user.is_authenticated:
        return redirect("/email_updates")
    else:
        return redirect("/login")
