from .. import db
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd
from sqlalchemy import func
from datetime import timedelta

full_table_blueprint = Blueprint('full_table', __name__, template_folder='templates')

max_time = db.session.query(func.max(Tobacco.time)).scalar() - timedelta(hours=10)
main_df = pd.read_sql(Tobacco.query.filter(Tobacco.time >= max_time).statement, db.session.bind)

df = main_df.copy()
df["price_num"] = df["price"].str.extract(r'(\d+.\d+)')
df["price_num"] = pd.to_numeric(df["price_num"], errors="coerce").fillna(10 ** 4)
df = df[df["item"] != ""]

df["item_class"] = "text-dark"
df.loc[df["stock"] == "Out of stock", "item_class"] = "text-danger"
df["item"] = "<a class='" + df["item_class"] + "' target='_blank' href='" + df["link"] + "'>" + df["item"] + "</a>"
df["stock"] = "<div class='" + df["item_class"] + "'>" + df["stock"] + "</div>"

cols = ["store", "item", "stock", "price", "time", "price_num"]
df = df[cols]


@full_table_blueprint.route('/full_table')
def main():
    global df
    df = df.rename(columns={"time": "last updated (utc)"})
    df = df.rename(columns={"item": render_template("table_forms/search_form.html", label="item", column=1)})
    df = df.rename(columns={"store": render_template("table_forms/search_form.html", label="store", column=0)})
    df = df.rename(columns={"stock": render_template("table_forms/stock_toggle_button.html")})
    df = df.rename(columns={"price": render_template("table_forms/price_sort_button.html")})
    table = df.to_html(index=False, classes="table table-hover display table-bordered table-responsive-lg",
                       escape=False, border=0, justify="left", table_id="myTable")
    return render_template("full_table.html", table=table)
