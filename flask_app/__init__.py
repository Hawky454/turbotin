from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import os

path = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, engine_options={"pool_recycle": 280})
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

from .views.full_table import full_table_blueprint
from .views.individual_blends import individual_blends_blueprint
from .views.email_updates import email_updates_blueprint
from .auth import auth_blueprint

app.register_blueprint(full_table_blueprint)
app.register_blueprint(individual_blends_blueprint)
app.register_blueprint(email_updates_blueprint)
app.register_blueprint(auth_blueprint)

app.jinja_env.add_extension('jinja2.ext.do')


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route('/')
def main():
    return redirect("/full_table", code=302)


@app.route('/faq')
def faq():
    with open(os.path.join(path, "static/questions.json")) as f:
        faq_items = json.load(f)
    return render_template("faq.html", faq_items=faq_items)
