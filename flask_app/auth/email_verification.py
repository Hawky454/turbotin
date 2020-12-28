from flask import redirect, url_for, request, flash
from ..models import User
from .. import db
from flask_login import login_required, current_user
from . import auth_blueprint


@auth_blueprint.route('/verify_email/<user_id>/<email_code>')
def verify_email(user_id, email_code):
    user = User.query.filter_by(id=user_id).first()
    if email_code == user.email_code:
        user.email_verified = True
        db.session.commit()
        flash('Email verified', "success")

    return redirect("/email_updates")


@auth_blueprint.route('/resend_email')
@login_required
def resend_email():
    url = request.url_root + url_for("auth.verify_email", user_id=current_user.id, email_code=current_user.email_code)
    # send_email_confirmation_code(current_user.email, url)
    flash('Email sent', "success")
    return redirect("/email_updates")
