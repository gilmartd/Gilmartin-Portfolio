from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Pile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ratio = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(55), default='Active')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55), unique=True)
    password = db.Column(db.String(55))
    firstName = db.Column(db.String(55))
    lastName = db.Column(db.String(55))
    piles = db.relationship('Pile')


class PileUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ratio = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    date = db.Column(db.Date, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
