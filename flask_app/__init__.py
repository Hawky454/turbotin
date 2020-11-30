from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os

path = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
from .views.full_table import full_table_blueprint
from .views.individual_blends import individual_blends_blueprint

app.register_blueprint(full_table_blueprint)
app.register_blueprint(individual_blends_blueprint)


@app.route('/')
def main():
    return redirect("/full_table", code=302)


@app.route('/faq')
def faq():
    with open(os.path.join(path, "static/questions.json")) as f:
        faq_items = json.load(f)
    return render_template("faq.html", faq_items=faq_items)
