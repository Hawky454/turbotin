from .. import db
from flask import render_template, Blueprint, request, redirect, url_for
from .full_table import main_df
from .individual_blends import blend_list, store_colors
import pandas as pd
import json
from flask_login import login_required, current_user

email_updates_blueprint = Blueprint('email_updates', __name__, template_folder='templates')

df = main_df.copy()
brands = list(pd.unique(df["brand"]))
blends = {}
for brand, data in df.groupby("brand"):
    blends[brand] = list(pd.unique(data["blend"]))
store_list = list(pd.unique(df["store"]))


@email_updates_blueprint.route('/email_updates')
@login_required
def main():
    updates = json.loads(current_user.email_updates)
    for n in range(len(updates)):
        brand_blend = updates[n]["brand"] + " " + updates[n]["blend"]
        if brand_blend in blend_list:
            updates[n]["id"] = blend_list.index(updates[n]["brand"] + " " + updates[n]["blend"])
        else:
            updates[n]["id"] = None
    return render_template("email_updates.html", brands=brands, blends=blends, stores=store_list,
                           updates=updates, store_colors=store_colors)


@email_updates_blueprint.route('/email_updates/add_notification', methods=['POST'])
@login_required
def add_notification():
    def check_lowercase(item, array):
        if item.lower() in [n.lower() for n in array]:
            return array[[n.lower() for n in array].index(item.lower())]
        else:
            return None

    brand = check_lowercase(request.form["brand"], brands)
    if not brand:
        return json.dumps({"failed": True, "what": "The brand is invalid."})
    blend = check_lowercase(request.form["blend"], blends[brand])
    if not blend:
        return json.dumps({"failed": True, "what": "The blend is invalid."})

    stores = json.loads(request.form["stores"])
    if not stores or len(stores) == len(store_list):
        stores = None
    max_price = request.form["max_price"]
    if max_price:
        try:
            max_price = float(request.form["max_price"])
        except ValueError:
            return json.dumps({"failed": True, "what": "The price is invalid."})
    updates = json.loads(current_user.email_updates)
    if len(updates) >= 10:
        return json.dumps({"failed": True, "what": "You cannot subscribe to more than 10 updates."})
    updates.append({"brand": brand, "blend": blend, "stores": stores, "max_price": max_price})
    current_user.email_updates = json.dumps(updates)
    db.session.commit()
    return json.dumps({"failed": False, "what": None})


@email_updates_blueprint.route('/email_updates/remove_notification', methods=['POST'])
@login_required
def remove_notification():
    index = int(request.form["index"])
    updates = json.loads(current_user.email_updates)
    updates.pop(index)
    current_user.email_updates = json.dumps(updates)
    db.session.commit()
    return json.dumps({"failed": False})
