# myapp.py


from flask import Flask, jsonify
from flask import request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Candidate, db.session))


@app.route('/index', methods=['GET'])
def index():
    users = User.query.all()
    return str(users)


@app.route('/candidates', methods=['GET'])
def candidates():
    all_candidates = Candidate.query.all()
    candidates_list = []
    for candidate in all_candidates:
        candidates_list.append({
            'url': '/candidate/{:d}/'.format(candidate.id),
            'id': candidate.id,
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'age': candidate.age,
            'party': candidate.party,
            'description': candidate.description,
        })
    return jsonify({'candidates_list': candidates_list})


@app.route('/candidate/<int:pk>')
def candidate_details(pk):
    candidate = Candidate.query.get(pk)
    return jsonify(
        {
            'url': '/candidate/{:d}/'.format(candidate.id),
            'id': candidate.id,
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'age': candidate.age,
            'party': candidate.party,
            'description': candidate.description,
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
