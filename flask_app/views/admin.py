from flask import render_template, Blueprint, redirect
from flask_login import login_required, current_user
import pandas as pd
from .. import db
import os
import json
from .individual_blends import colors
import itertools

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route("/admin")
@login_required
def admin():
    if current_user.email not in eval(os.environ["ADMIN_EMAILS"]):
        return redirect("/")
    users = pd.read_sql("user", db.engine)
    users["email_updates"] = users["email_updates"].apply(lambda x: json.loads(x))
    blends = []
    [[blends.append(i) for i in n] for n in users["email_updates"]]
    blends = pd.DataFrame(blends)
    blends = pd.Series("<b>" + blends["brand"] + "</b> " + blends["blend"]).value_counts()
    return render_template("admin.html", users=users.to_dict("records"), store_colors=colors, blends=blends.to_dict())
