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
