# myapp.py


from flask import Flask, jsonify, session, make_response
from flask import request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *
from datetime import timedelta
from jose import jwt, exceptions, JWTError
import json


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

admin = Admin(app, name='Voting online', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Candidate, db.session))


@app.before_request
def func():
    session.modified = True
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/index', methods=['GET'])
def index():
    users = User.query.all()
    return str(users)


@app.route('/login', methods=['POST'])
def login():
    claims = request.json
    headers = request.headers
    required_fields = {'first_name', 'last_name', 'father_name', 'mother_name', 'id_series_number', 'pesel'}
    if required_fields.issubset(set(claims)):
        matching_records = User.query.filter_by(**claims).all()
        if len(matching_records) == 1:
            token = jwt.encode(claims, app.secret_key, headers=headers)
            return my_make_response(json.dumps({"token": token}), 200)
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


@app.route('/vote', methods=['POST'])
def vote():
    check_output = check_token(request)
    if 'user' in check_output['result']:
        user = check_output['result']['user']
    else:
        return my_make_response(json.dumps(check_output['result']), check_output['status_code'])

    return my_make_response(json.dumps({
        'message': 'Success! User: {} {} has voted.'.format(user.first_name, user.last_name) + str(session)
    }), 200)


# --------------------


def check_token(request):
    try:
        if 'token' in request.headers:  # order of checking matters. Checking headers must be first
            try:
                decoded = jwt.decode(request.headers['token'], app.secret_key)
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


def my_make_response(resp_body, code):
    resp = make_response(resp_body)
    resp.headers['Content-Length'] = str(len(resp_body))
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = code
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
