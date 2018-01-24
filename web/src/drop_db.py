from app import db
from models import *

Vote.query.delete()
User.query.delete()
Candidate.query.delete()
Config.query.delete()
db.session.commit()
