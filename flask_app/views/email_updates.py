from .. import db, path
from flask import render_template, Blueprint, request, redirect, url_for
from .full_table import main_df
from ..models import Tobacco
import pandas as pd
import os
import json

email_updates_blueprint = Blueprint('email_updates', __name__, template_folder='templates')

df = main_df.copy()
brands = list(pd.unique(df["brand"]))
blends = {}
for brand, data in df.groupby("brand"):
    blends[brand] = list(pd.unique(data["blend"]))
store_list = list(pd.unique(df["store"]))


@email_updates_blueprint.route('/email_updates')
def main():
    return render_template("email_updates.html", brands=brands, blends=blends, stores=store_list)


@email_updates_blueprint.route('/email_updates/add_notification', methods=['POST'])
def add_notification():
    def check_lowercase(item, array):
        if item.lower() in [n.lower() for n in array]:
            return array[[n.lower() for n in array].index(item.lower())]
        else:
            return None

    brand = check_lowercase(request.form["brand"], brands)
    if not brand:
        return json.dumps({"failed": True, "what": "Brand"})
    blend = check_lowercase(request.form["blend"], blends[brand])
    if not blend:
        return json.dumps({"failed": True, "what": "Blend"})

    stores = json.loads(request.form["stores"])
    if not stores or len(stores) == len(store_list):
        stores = None
    max_price = request.form["max_price"]
    if max_price:
        try:
            max_price = float(request.form["max_price"])
        except ValueError:
            return json.dumps({"failed": True, "what": "Price"})

    return json.dumps({"failed": False, "what": None})
