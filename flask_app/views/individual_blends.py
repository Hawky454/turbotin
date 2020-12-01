from .. import db
from .full_table import main_df
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd
import random

individual_blends_blueprint = Blueprint('individual_blends', __name__, template_folder='templates')

df = main_df.copy()
df["price_num"] = df["price"].str.extract(r'(\d+.\d+)')
df["price_num"] = pd.to_numeric(df["price_num"], errors="coerce").fillna(10 ** 4)
df = df[df["item"] != ""]

df["item_class"] = "text-dark"
df.loc[df["stock"] == "Out of stock", "item_class"] = "text-danger"
df["stock"] = "<div class='" + df["item_class"] + "'>" + df["stock"] + "</div>"
df["time"] = pd.to_datetime(df["time"], format="%m/%d/%Y %H:%M", utc=True)
df["time"] = df["time"].apply(lambda x: str(int(x.timestamp())))
df["time"] = '''<script>document.write(moment.unix(''' + df["time"] + ''').fromNow());</script>'''

# archive_df = pd.read_sql("tobacco", db.engine)
# archive_df.to_feather("archive.feather")
blend_list = list(pd.unique(main_df["brand"] + " " + main_df["blend"]))
search_list = [{"key": n, "text": blend_list[n].lower(), "full_text": blend_list[n]} for n in range(len(blend_list))]
archive_df = pd.read_feather("archive.feather")
archive_df["price_num"] = archive_df["price"].str.extract(r'(\d+.\d+)')
archive_df["price_num"] = pd.to_numeric(archive_df["price_num"], errors="coerce")
archive_df = archive_df[archive_df["item"] != ""]

colors = ["#007bff", "#6610f2", "#6f42c1", "#e83e8c", "#dc3545", "#fd7e14", "#ffc107", "#28a745", "#20c997", "#17a2b8"]
random.shuffle(colors)


@individual_blends_blueprint.route('/individual_blends/<blend>')
def main(blend):
    blend = int(blend)
    brand = main_df["brand"][(main_df["brand"] + " " + main_df["blend"]) == blend_list[blend]].iloc[0]
    blends = pd.unique(main_df["blend"][main_df["brand"] == brand])
    blends = [{"name": n, "id": blend_list.index(brand + " " + n)} for n in blends]
    _, blends = zip(*sorted(zip([n["name"] for n in blends], blends)))
    blend_name = [n["name"] for n in blends if n["id"] == blend][0]

    global df
    table_df = df.copy()
    table_df = table_df[(table_df["brand"] == brand) & (table_df["blend"] == blend_name)]
    table_df = table_df.sort_values("price_num")
    cols = ["store", "item", "stock", "price", "time"]
    table_df = table_df[cols]

    stores = list(pd.unique(table_df["store"]))
    store_colors = {stores[n]: colors[divmod(n, len(colors))[1]] for n in range(len(stores))}

    return render_template("individual_blends.html", brand=brand, blends=blends, search_list=search_list, id=blend,
                           blend=blend_name, items=list(table_df.T.to_dict().values()), store_colors=store_colors,
                           plot_data=get_plot_data(brand, blend_name))


def get_plot_data(brand, blend):
    plot_df = archive_df[(archive_df["brand"] == brand) & (archive_df["blend"] == blend)]
    plot_df = plot_df.groupby(["time", "store"])["price_num"].aggregate("min").unstack()
    plot_df = plot_df.dropna(axis="columns", how="all")
    plot_df = plot_df.dropna(axis="rows", how="all")
    plot_df = plot_df.fillna("NaN")
    datasets = [{"store": col, "data": list(plot_df[col])} for col in plot_df.columns]
    plot_data = {"labels": list(plot_df.index.astype(str)), "datasets": datasets}
    return plot_data
