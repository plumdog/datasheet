from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from flask_crud import CrudBase

db = SQLAlchemy()


class Base(db.Model, CrudBase):
    __abstract__ = True


class User(Base, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(1000))
