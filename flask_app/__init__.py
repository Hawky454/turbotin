from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
import os
import pandas as pd
from datetime import timedelta

path = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

from .models import Tobacco

max_time = db.session.query(func.max(Tobacco.time)).scalar() - timedelta(hours=10)
main_df = pd.read_sql(Tobacco.query.filter(Tobacco.time >= max_time).statement, db.session.bind)


@app.route('/')
def main():
    global main_df
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
    
    df = df.rename(columns={"time": "last updated (utc)"})
    df = df.rename(columns={"item": render_template("table_forms/search_form.html", label="item", column=1)})
    df = df.rename(columns={"store": render_template("table_forms/search_form.html", label="store", column=0)})
    df = df.rename(columns={"stock": render_template("table_forms/stock_toggle_button.html")})
    df = df.rename(columns={"price": render_template("table_forms/price_sort_button.html")})

    table = df.to_html(index=False, classes="table table-hover display table-bordered table-responsive-lg",
                       escape=False, border=0, justify="left", table_id="myTable")
    return render_template("main.html", table=table)


@app.route('/faq')
def faq():
    with open(os.path.join(path, "static/questions.json")) as f:
        faq_items = json.load(f)
    return render_template("faq.html", faq_items=faq_items)


@app.route('/blends/', defaults={'blend': None})
@app.route('/blends/<blend>')
def blends(blend):
    return render_template("blend.html")
