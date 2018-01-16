# create_db.py


from app import db
from models import Machine, User

db.create_all()
db.session.add(Machine('localhost'))
db.session.add(Machine('web'))
db.session.add(Machine('postgres_running'))
db.session.add(Machine('missing'))
db.session.add(User(
    first_name='Michal',
    last_name='Sut',
    father_name='Grzegorz',
    mother_name='Beata',
    id_series_number='AAVA12411',
    pesel='96040702510',
))
db.session.commit()
