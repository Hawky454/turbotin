from .. import db
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd
from sqlalchemy import func
from datetime import timedelta

full_table_blueprint = Blueprint('full_table', __name__, template_folder='templates')

max_time = db.session.query(func.max(Tobacco.time)).scalar() - timedelta(hours=10)
main_df = pd.read_sql(Tobacco.query.filter(Tobacco.time >= max_time).statement, db.session.bind)
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
