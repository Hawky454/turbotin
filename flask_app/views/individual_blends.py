from .. import db
from .full_table import main_df, ids
from flask import render_template, Blueprint, redirect
from ..models import Tobacco
import pandas as pd
import random

individual_blends_blueprint = Blueprint('individual_blends', __name__, template_folder='templates')

df = main_df.copy()

df["item_class"] = "text-dark"
df.loc[df["stock"] == "Out of stock", "item_class"] = "text-danger"
df["stock"] = "<div class='" + df["item_class"] + "'>" + df["stock"] + "</div>"
df["time"] = '''<script>document.write(moment.unix(''' + df["time"] + ''').fromNow());</script>'''

# archive_df = pd.read_sql("tobacco", db.engine)
# archive_df.to_feather("archive.feather")
search_list = [{"link": "/individual_blends/{}".format(n), "text": ids[n]} for n in range(len(ids))]
archive_df = pd.read_feather("archive.feather")
archive_df["price_num"] = archive_df["price"].str.extract(r'(\d+.\d+)')
archive_df["price_num"] = pd.to_numeric(archive_df["price_num"], errors="coerce")
archive_df = archive_df[archive_df["item"] != ""]
archive_df = archive_df[archive_df["stock"] != "Out of stock"]

colors = ["#007bff", "#6610f2", "#6f42c1", "#e83e8c", "#dc3545", "#fd7e14", "#ffc107", "#28a745", "#20c997", "#17a2b8"]
stores = list(pd.unique(archive_df["store"]))
store_colors = {stores[n]: colors[divmod(n, len(colors))[1]] for n in range(len(stores))}


@individual_blends_blueprint.route('/individual_blends/<blend>')
def main(blend):
    blend = int(blend)
    brand = main_df["brand"][(main_df["brand"] + " " + main_df["blend"]) == ids[blend]].iloc[0]
    blends = pd.unique(main_df["blend"][main_df["brand"] == brand])
    blends = [{"name": n, "id": ids.index(brand + " " + n)} for n in blends]
    _, blends = zip(*sorted(zip([n["name"] for n in blends], blends)))
    blend_name = [n["name"] for n in blends if n["id"] == blend][0]

    global df
    table_df = df.copy()
    table_df = table_df[(table_df["brand"] == brand) & (table_df["blend"] == blend_name)]
    table_df = table_df.sort_values("price_num")
    cols = ["store", "item", "stock", "price", "time", "link"]
    table_df = table_df[cols]

    return render_template("individual_blends.html", brand=brand, blends=blends, search_list=search_list, id=blend,
                           blend=blend_name, items=list(table_df.T.to_dict().values()), store_colors=store_colors,
                           plot_data=get_plot_data(brand, blend_name))


@individual_blends_blueprint.route('/individual_blends')
def default():
    return redirect("/individual_blends/{}".format(int(random.random() * len(ids))))


def get_plot_data(brand, blend):
    plot_df = archive_df[(archive_df["brand"] == brand) & (archive_df["blend"] == blend)]
    plot_df = plot_df.groupby(["time", "store"])["price_num"].aggregate("min").unstack()
    plot_df = plot_df.dropna(axis="columns", how="all")
    plot_df = plot_df.dropna(axis="rows", how="all")
    plot_df = plot_df.fillna("NaN")
    datasets = [{"store": col, "data": list(plot_df[col])} for col in plot_df.columns]
    plot_data = {"labels": list(plot_df.index.astype(str)), "datasets": datasets}
    return plot_data
