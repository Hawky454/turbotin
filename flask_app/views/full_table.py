from .. import db, path
from flask import render_template, Blueprint
from ..models import Tobacco
import pandas as pd
from sqlalchemy import func
from datetime import timedelta
from bs4 import BeautifulSoup
import os

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
df["time"] = df["time"].dt.strftime("%m/%d/%Y, %H:%M")

cols = ["store", "item", "stock", "price", "time", "price_num"]
df = df[cols]
df = df.rename(columns={"time": "Last Updated (UTC)"})
with open(os.path.join(path, "static/table_forms/search_form.html"), "r") as f:
    template = f.read()
    df = df.rename(columns={"item": template.format(label="item")})
    df = df.rename(columns={"store": template.format(label="store")})
with open(os.path.join(path, "static/table_forms/stock_toggle_button.html"), "r") as f:
    df = df.rename(columns={"stock": f.read()})
with open(os.path.join(path, "static/table_forms/price_sort_button.html"), "r") as f:
    df = df.rename(columns={"price": f.read()})
table = df.to_html(index=False, escape=False, border=0, justify="left", table_id="myTable",
                   classes="table table-hover display table-bordered table-responsive-lg bg-light table-striped")
table = BeautifulSoup(table, features="lxml")
n = 0
for tr in table.find_all("tr"):
    if n > 100:
        tr["style"] = "display: none;"
    n += 1
table = str(table)


@full_table_blueprint.route('/full_table')
def main():
    return render_template("full_table.html", table=table)
