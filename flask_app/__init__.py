from flask import Flask, render_template
import json
import os
import pandas as pd

app = Flask(__name__)
path = os.path.dirname(__file__)

df = pd.read_pickle("data/cat_data.p")
blends = df["brand"] + " " + df["blend"]
blends_list = pd.unique(blends)
blends_list = [{"key": n, "text": blends_list[n].lower(), "full_text": blends_list[n]} for n in range(len(blends_list))]


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/faq')
def faq():
    with open(os.path.join(path, "static/questions.json")) as f:
        faq_items = json.load(f)
    return render_template("faq.html", faq_items=faq_items)


@app.route('/blends/', defaults={'blend': None})
@app.route('/blends/<blend>')
def blends(blend):
    if not blend:
        blend = blends_list[0]
    return render_template("blend.html", blends_list=blends_list)
