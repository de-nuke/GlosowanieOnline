from app import db
from models import *

Vote.query.delete()
for c in Candidate.query.all():
    c.num_of_votes = 0
    c.votes = None
for u in User.query.all():
    u.vote = None
    u.has_voted = False
db.session.commit()

