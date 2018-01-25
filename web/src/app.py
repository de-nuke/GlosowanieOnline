# app.py

from flask import Flask, jsonify, session, make_response
from flask import request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta, datetime as dt
from jose import jwt, exceptions, JWTError
import json
import hashlib

app = Flask(__name__, static_url_path='/src/static')
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

""" Imports that depend on db object"""
from models import *
from admin_login import MyAdminIndexView, init_login
from admin_views import SecureFormAdminView, VoteAdminView

init_login()

admin = Admin(app, name='Voting online', template_mode='bootstrap3', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(SecureFormAdminView(User, db.session))
admin.add_view(SecureFormAdminView(Candidate, db.session))
# admin.add_view(VoteAdminView(Vote, db.session))  # Administrator shouldn't see votes
admin.add_view(SecureFormAdminView(Config, db.session))


def require_voting_active(func):
    def func_wrapper():
        if voting_is_active():
            return func()
        else:
            return my_make_response(json.dumps({
                'error_type': 'voting_inactive',
                'voting_inactive': 'You cannot perform this action, because there is no active voting now.'
            }), 410)

    func_wrapper.__name__ = func.__name__
    return func_wrapper


def require_voting_inactive(func):
    def func_wrapper():
        if not voting_is_active():
            return func()
        else:
            return my_make_response(json.dumps({
                'error_type': 'voting_active',
                'voting_inactive': 'You cannot perform this action while voting is active'
            }), 403)

    func_wrapper.__name__ = func.__name__
    return func_wrapper


@app.route('/login', methods=['POST'])
@require_voting_active
def login():
    claims = request.json
    headers = request.headers

    required_fields = {'first_name', 'last_name', 'father_name', 'mother_name', 'id_series_number', 'pesel'}
    if required_fields.issubset(set(claims)):
        for hf in USER_HASHED_FIELDS:  # imported from models.py
            claims[hf] = hashlib.sha256(claims[hf].encode("utf-8")).hexdigest()

        matching_records = User.query.filter_by(**claims).all()
        if len(matching_records) == 1:
            token = jwt.encode(claims, app.secret_key, headers=headers)
            return my_make_response(json.dumps({"token": token, "has_voted": matching_records[0].has_voted}), 200)
        elif len(matching_records) >= 2:
            return my_make_response(json.dumps({
                'error_type': 'multiple_users',
                'multiple_users': [u.to_dict_repr() for u in matching_records]
            }), 400)
        else:
            return my_make_response(json.dumps({
                'error_type': 'user_not_found',
                'user_not_found': str(claims)
            }), 400)
    else:
        missing_fields = required_fields - set(claims)
        return my_make_response(json.dumps({
            'error_type': 'missing_fields',
            'missing_fields': ','.join(missing_fields)
        }), 400)


@app.route('/candidates', methods=['GET'])
@require_voting_active
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
    return jsonify({'candidates_list': sorted(candidates_list, key=lambda x:x['id'])})


@app.route('/candidate/<int:pk>')
@require_voting_active
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


@app.route('/vote', methods=['POST'])
@require_voting_active
def vote():
    check_output = check_token()
    if 'user' in check_output['result']:
        user = check_output['result']['user']
    else:
        return my_make_response(json.dumps(check_output['result']), check_output['status_code'])

    data = request.json

    if not 'candidate_id' in data:
        return my_make_response(json.dumps({
            'error_type': 'candidate_not_found',
            'candidate_not_found': ''
        }), 400)

    candidates = Candidate.query.filter_by(id=data['candidate_id']).all()
    if len(candidates) >= 2:
        return my_make_response(json.dumps({
            'error_type': 'multiple_candidates',
            'multiple_candidates': [c.to_dict_repr for c in candidates]
        }), 400)
    elif not candidates:
        return my_make_response(json.dumps({
            'error_type': 'candidate_not_found',
            'candidate_not_found': data['candidate_id']
        }), 400)
    else:
        """ Found one candidate """
        if user.can_vote() and voting_is_active():
            candidate = candidates[0]
            candidate.num_of_votes += 1
            v = Vote(voter=user, candidate=candidate)
            user.has_voted = True
            db.session.add(v)
            db.session.commit()
        else:
            reason = 'User(id={}) has already voted'.format(user.id) if not user.can_vote() else 'Voting is disabled now'
            return my_make_response(json.dumps({
                'error_type': 'voting_unavailable',
                'voting_unavailable': reason
            }), 403)

    return my_make_response(json.dumps({
        'message': 'Success! User: {} {} has voted.'.format(user.first_name, user.last_name)
    }), 200)


@app.route('/results')
@require_voting_inactive
def results():
    if not voting_is_active():
        candidates = sorted(Candidate.query.all(), key=lambda x: -x.num_of_votes)
        return my_make_response(json.dumps({
            'candidates': [c.to_dict_full() for c in candidates]
        }), 200)
    else:
        return my_make_response(json.dumps({
            'error_type': 'results_unavailable',
            'results_unavailable': 'Cannot get results while voting is active'
        }), 403)


# --------------------


def check_token():
    try:
        if 'token' in request.headers:  # order of checking matters. Checking headers must be first
            try:
                decoded = jwt.decode(request.headers['token'], app.secret_key)
                matching_records = db.session.query(User).filter_by(**decoded).all()
                if len(matching_records) == 1:
                    user = matching_records[0]
                    result = {"user": user}
                    code = 200
                elif len(matching_records) >= 2:
                    result = {'error_type': 'multiple_users',
                              'multiple_users': [u.to_dict_repr() for u in matching_records]}
                else:
                    result = {'error': 'Invalid token'}
                    code = 403
            except JWTError as e:
                result = {'error': str(e)}
                code = 400
        elif 'token' in request.json:
            try:
                decoded = jwt.decode(request.json['token'], app.secret_key)
                matching_records = User.query.filter_by(**decoded).all()
                if len(matching_records) == 1:
                    user = matching_records[0]
                    result = {"user": user}
                    code = 200
                elif len(matching_records) >= 2:
                    result = {'error_type': 'multiple_users',
                              'multiple_users': [u.to_dict_repr() for u in matching_records]}
                else:
                    result = {'error': 'Invalid token'}
                    code = 403
            except JWTError as e:
                result = {'error': str(e)}
                code = 400
        else:
            result = {'error': 'No token in Headers'}
            code = 401
    except TypeError:
        result = {"error": "token required (checked Headers and Body)."}
        code = 401
    return {"status_code": code, "result": result}


def voting_is_active():
    c = Config.query.first()
    now = dt.now()
    if not c:
        return True
    return c.voting_start < now < c.voting_stop


def my_make_response(resp_body, code):
    resp = make_response(resp_body)
    resp.headers['Content-Length'] = str(len(resp_body))
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = code
    return resp
pass

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
