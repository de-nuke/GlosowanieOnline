# myapp.py


from flask import Flask
from flask import request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig

from models import *

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


db.create_all()
db.session.add(User(
    first_name='Michal',
    last_name='Sut',
    father_name='Grzegorz',
    mother_name='Beata',
    id_series_number='AAVA12411',
    pesel='96040702510',
))

db.session.commit()
@app.route('/index', methods=['GET'])
def index():
    users = User.query.all()
    return str(users)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

