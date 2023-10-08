from flask_login import UserMixin

from . import db


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, description, price, owner_id):
        self.name = name
        self.description = description
        self.price = price
        self.owner_id=owner_id


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hased_password = db.Column(db.String(120), unique=True, nullable=False)
    assets = db.relationship('Asset', backref='owner', lazy='dynamic')

    def __init__(self, username, hased_password):
        self.username = username
        self.hased_password = hased_password




