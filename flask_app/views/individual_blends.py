from .. import db
from .full_table import main_df
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd

individual_blends_blueprint = Blueprint('individual_blends', __name__, template_folder='templates')

# archive_df = pd.read_sql("tobacco", db.engine)
# archive_df.to_feather("archive.feather")
blend_list = list(pd.unique(main_df["brand"] + " " + main_df["blend"]))
search_list = [{"key": n, "text": blend_list[n].lower(), "full_text": blend_list[n]} for n in range(len(blend_list))]
archive_df = pd.read_feather("archive.feather")


@individual_blends_blueprint.route('/individual_blends/<blend>')
def main(blend):
    blend = int(blend)
    print(blend_list[blend])
    brand = main_df["brand"][(main_df["brand"] + " " + main_df["blend"]) == blend_list[blend]].iloc[0]
    blends = pd.unique(main_df["blend"][main_df["brand"] == brand])
    blends = [{"name": n, "id": blend_list.index(brand + " " + n)} for n in blends]

    return render_template("individual_blends.html", brand=brand, blends=blends, search_list=search_list, id=blend)
