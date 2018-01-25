# models.py


import datetime
from app import db
import json
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import hashlib

USER_HASHED_FIELDS = ['id_series_number', 'pesel']

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String, nullable=False)
    mother_name = db.Column(db.String, nullable=False)
    id_series_number = db.Column(db.String, nullable=False)
    pesel = db.Column(db.String, nullable=False)

    vote = relationship('Vote', uselist=False, back_populates='voter')

    has_voted = db.Column(db.Boolean, nullable=True, default=False)


    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key) and key not in USER_HASHED_FIELDS:
                setattr(self, key, kwargs.get(key))
            else:
                raise AttributeError(self.__class__.__name__ + ' has no attribute: \'' + key + '\'')

        for hf in USER_HASHED_FIELDS:
            if hf in kwargs:
                hashed = hashlib.sha256(kwargs.get('id_series_number')).hexdigest()
                setattr(self, hf, hashed)


    def __str__(self):
        return '{}. {} {}, {}'.format(self.id, self.first_name, self.last_name, 'Already voted' if self.has_voted else 'Not voted yet')

    def to_dict_repr(self):
        return {'user': {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }}

    def can_vote(self):
        return not self.has_voted and self.vote is None


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False, default='')
    last_name = db.Column(db.String, nullable=False, default='')
    age = db.Column(db.Integer, nullable=False, default=0)
    party = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    num_of_votes = db.Column(db.Integer, nullable=False, default=0)

    votes_set = relationship('Vote', back_populates='candidate')

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key))
            else:
                raise AttributeError(self.__class__.__name__ + ' has no attribute: \'' + key + '\'')

    def __str__(self):
        return '{}. {} {}, {}'.format(self.id, self.first_name, self.last_name, self.party)

    def to_dict_repr(self):
        return {'candidate': {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }}

    def to_dict_full(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'party': self.party,
            'num_of_votes': self.num_of_votes
        }

class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, ForeignKey('users.id'))
    voter = relationship('User', back_populates='vote')
    candidate_id = db.Column(db.Integer, ForeignKey('candidates.id'))
    candidate = relationship("Candidate", back_populates="votes_set")
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        super(Vote, self).__init__(**kwargs)
        self.created = datetime.datetime.now()


class Config(db.Model):
    __tablename__ = 'configs'

    id = id = db.Column(db.Integer, primary_key=True)
    voting_start = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    voting_stop = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __str__(self):
        return 'voting active: {} - {}'.format(self.voting_start, self.voting_stop)