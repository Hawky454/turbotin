from .. import path
from flask import render_template, Blueprint
import pandas as pd
from datetime import timedelta
import os

full_table_blueprint = Blueprint('full_table', __name__, template_folder='templates')

archive = pd.read_feather(os.path.join(os.path.dirname(path), "data/archive.feather"))
main_df = archive[archive["time"] >= archive["time"].max() - timedelta(hours=10)].copy()
main_df["time"] = pd.to_datetime(main_df["time"], format="%m/%d/%Y %H:%M", utc=True)
main_df["time"] = main_df["time"].apply(lambda x: str(int(x.timestamp())))
main_df["price_num"] = main_df["price"].str.extract(r'(\d+.\d+)')
main_df["price_num"] = pd.to_numeric(main_df["price_num"], errors="coerce").fillna(10 ** 4)
main_df = main_df[main_df["item"] != ""]
df = main_df.copy()
ids = list(pd.unique(main_df["brand"] + " " + main_df["blend"]))

df["id"] = (df["brand"] + " " + df["blend"]).apply(lambda x: ids.index(x))

cols = ["store", "link", "item", "stock", "price", "time", "price_num", "id"]
df = df[cols]


@full_table_blueprint.route('/full_table')
def main():
    return render_template("full_table.html", table=df.values.tolist(), stores=sorted(list(pd.unique(df["store"]))))
