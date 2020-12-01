from .. import db, path
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd
from sqlalchemy import func
from datetime import timedelta
import os

email_updates_blueprint = Blueprint('email_updates', __name__, template_folder='templates')


@email_updates_blueprint.route('/email_updates')
def main():
    return render_template("email_updates.html")
