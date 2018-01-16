# models.py


import datetime
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String, nullable=False)
    mother_name = db.Column(db.String, nullable=False)
    id_series_number = db.Column(db.String, nullable=False)
    pesel = db.Column(db.String, nullable=False)
    has_voted = db.Column(db.Boolean, nullable=True, default=False)

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key))
            else:
                raise AttributeError(self.__class__.__name__ + ' has no attribute: \'' + key + '\'')


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    party = db.Column(db.String, nullable=True, default='None')
    description = db.Column(db.String, nullable=True, default='')


    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key))
            else:
                raise AttributeError(self.__class__.__name__ + ' has no attribute: \'' + key + '\'')

