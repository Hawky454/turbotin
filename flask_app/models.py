from flask_login import UserMixin
from . import db


class Tobacco(db.Model):
    store = db.Column(db.String(100))
    item = db.Column(db.String(200), primary_key=True)
    price = db.Column(db.String(100))
    stock = db.Column(db.String(100))
    link = db.Column(db.String(300), primary_key=True)
    time = db.Column(db.DateTime(), primary_key=True)
    brand = db.Column(db.String(500))
    blend = db.Column(db.String(500))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email_verified = db.Column(db.Boolean())
    email_code = db.Column(db.String(100))
    email_updates = db.Column(db.String(10000))
    password_reset_code = db.Column(db.String(100))
    latest_auth_email = db.Column(db.DateTime())
