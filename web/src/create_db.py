# create_db.py


from app import db
from models import Machine

db.create_all()
db.session.add(Machine('localhost'))
db.session.add(Machine('web'))
db.session.add(Machine('postgres_running'))
db.session.add(Machine('missing'))
db.session.commit()
