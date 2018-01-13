# models.py


import datetime
from app import db


class Machine(db.Model):

    __tablename__ = 'machines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    last_checked = db.Column(db.DateTime, nullable=False)
    last_status = db.Column(db.Boolean, nullable=False)
    def __init__(self, name):
        self.name = name
        self.last_checked = datetime.datetime.now()
        self.last_status = False
        
