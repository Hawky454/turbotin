from flask import Flask, render_template
import json
import os
import pandas as pd
import pickle
import timeago
import datetime

app = Flask(__name__)
path = os.path.dirname(__file__)

df = pd.read_pickle("data/cat_data.p")
blends = df["brand"] + " " + df["blend"]
blends_list = pd.unique(blends)
blends_list = [{"key": n, "text": blends_list[n].lower(), "full_text": blends_list[n]} for n in range(len(blends_list))]


@app.route('/')
def main():
    with open(os.path.join(os.path.dirname(path), "data/sample_data.p"), "rb") as f:
        df = pickle.load(f)
    # df = df.loc[:200]
    df["price_num"] = df["price"].str.extract(r'(\d+.\d+)')
    df["price_num"] = pd.to_numeric(df["price_num"], errors="coerce")
    df = df[df["item"] != ""]
    df["item_class"] = "text-dark"
    df.loc[df["stock"] == "Out of stock", "item_class"] = "text-danger"
    df["item"] = '''<a class=' ''' + df["item_class"] + ''' ' target="_blank" href="''' + df["link"] + '''">''' + df[
        "item"] + '''</a>'''

    cols = ["store", "item", "stock", "price", "time", "price_num"]
    df = df[cols]

    df = df.rename(columns={"time": "last updated (utc)"})
    df = df.rename(columns={"item": render_template("table_forms/search_form.html", label="item", column=1)})
    df = df.rename(columns={"store": render_template("table_forms/search_form.html", label="store", column=0)})
    df = df.rename(columns={"stock": render_template("table_forms/stock_toggle_button.html")})
    df = df.rename(columns={"price": render_template("table_forms/price_sort_button.html")})

    table = df.to_html(index=False, classes="table table-hover display table-bordered table-responsive-lg",
                       escape=False, border=0, justify="left", table_id="myTable")
    return render_template("main.html", table=table, blends_list=blends_list)


@app.route('/faq')
def faq():
    with open(os.path.join(path, "static/questions.json")) as f:
        faq_items = json.load(f)
    return render_template("faq.html", faq_items=faq_items, blends_list=blends_list)


@app.route('/blends/', defaults={'blend': None})
@app.route('/blends/<blend>')
def blends(blend):
    if not blend:
        blend = blends_list[0]
    return render_template("blend.html", blends_list=blends_list)
