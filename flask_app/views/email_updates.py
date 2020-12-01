from .. import db, path
from flask import render_template, Blueprint
from .full_table import main_df
from ..models import Tobacco
import pandas as pd
import os

email_updates_blueprint = Blueprint('email_updates', __name__, template_folder='templates')

df = main_df.copy()
brands = list(pd.unique(df["brand"]))
blends = {}
for brand, data in df.groupby("brand"):
    blends[brand] = list(pd.unique(data["blend"]))


@email_updates_blueprint.route('/email_updates')
def main():
    return render_template("email_updates.html", brands=brands, blends=blends)
