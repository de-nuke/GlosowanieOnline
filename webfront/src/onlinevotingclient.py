# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, request
from urllib2 import Request, urlopen, HTTPError
import json, urllib
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, widgets
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
	first_name = StringField('first_name', validators=[DataRequired()])
	last_name = StringField('last_name', validators=[DataRequired()])
	father_name = StringField('father_name', validators=[DataRequired()])
	mother_name = StringField('mother_name', validators=[DataRequired()])
	id_series_number = StringField('id_series_number', validators=[DataRequired()])
	pesel = StringField('pesel', validators=[DataRequired()])
class VoteForm(FlaskForm):
	candidate = SelectField('candidate', choices=[], widget=widgets.Select())
app_url = ''
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "SecretAppKeyXxX"
app.debug = False
def u(string):
	return unicode(string, "utf-8")
def voting_ended():
	requestedData = Request('http://localhost:8001/results')
        try:
                response = urlopen(requestedData)
                response_dict = json.load(response)
                if response.getcode() == 200:
			return True
		else:
			return False
	except Exception as e:
		return False
def get_results():
	candidates_list = []
        ids = []
        first_names = []
        last_names = []
        ages = []
        parties = []
	number_of_votes = []
	requestedData = Request('http://localhost:8001/results')
        try:
                response = urlopen(requestedData)
                response_dict = json.load(response)
                if response.getcode() == 200:
			candidates_list = response_dict['candidates']
			for value in candidates_list:
                                ids.append(value['id'])
                                first_names.append(value['first_name'])
                                last_names.append(value['last_name'])
                                ages.append(value['age'])
                                parties.append(value['party'])
				number_of_votes.append(value['num_of_votes'])
                        return render_template('/results.html', number_of_votes = number_of_votes, ids=ids, first_names=first_names, last_names=last_names, ages=ages, parties=parties)
        except Exception as e:
		print e
                return render_template('/error.html', message = u("Zapytanie nie było poprawne lub wybory się nie zakończyły."))


@app.route(app_url + '/')
def index():
        if voting_ended() != False:
                return get_results()
	if session.has_key('token'):
		return render_template(app_url + '/logged.html', first_name = session['first_name'], second_name = session['last_name'])
	else:
		return render_template('/index.html')
@app.route(app_url + '/login')
def login():
        if voting_ended() != False:
                return get_results()
	if session.has_key('token'):
		return redirect(app_url + '/logged')
	else:
		form = LoginForm()
		return render_template('/login.html', form=form)
@app.route(app_url + '/check', methods=['POST', 'GET'])
def check():
	values_dict = {}
	values_dict['first_name'] = request.form["first_name"]
	values_dict['last_name'] = request.form["last_name"]
	values_dict['father_name'] = request.form["father_name"]
	values_dict['mother_name'] = request.form["mother_name"]
	values_dict['id_series_number'] = request.form["id_series_number"]
	values_dict['pesel'] = request.form["pesel"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
	requestedData = Request('http://localhost:8001/login', data=values, headers=headers)
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200:
			session['token'] = response_dict['token']
			session['first_name'] = values_dict['first_name']
			session['last_name'] = values_dict['last_name']
			session['has_voted'] = response_dict['has_voted']
			return redirect(app_url + '/logged')
		else:
			return render_template('/error.html', message = u("Nieprawidłowe dane logowania!"))
	except Exception as e:
		print e
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))
@app.route(app_url + '/logged')
def logged():
        if voting_ended() != False:
                return get_results()
	if session.has_key('token'):
		return render_template('/logged.html', first_name = session['first_name'], last_name = session['last_name'], has_voted = session['has_voted'])
	else:
		return redirect(app_url + '/')
@app.route(app_url + '/logout')
def logout():		
	session.clear()
	return redirect(app_url + '/')
@app.route(app_url + '/vote', methods=['GET', 'POST'])
def vote():
        if voting_ended() != False:
                return get_results()
	if not session.has_key('token'):
		return redirect(app_url + '/login')
	if session['has_voted'] == True:
		return render_template('/error.html', message = u("Już głosowałeś."))
	requestedData = Request('http://localhost:8001/candidates')
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200:
			candidates_list = response_dict['candidates_list']
			form = VoteForm()
			for value in candidates_list:
				candidate_string = str(value['id'])+". "+value['first_name']+ " " +value['last_name']
				form.candidate.choices.append((value['id'], candidate_string))
			return render_template('/vote.html', first_name = session['first_name'], second_name = session['last_name'], form=form)
		else:
			return render_template('/error.html', message = u("Brak komunikacji z bazą kandydatów. Spróbuj ponownie później."))
	except Exception as e:
		print e
		return render_template('/error.html', message = u("Brak komunikacji z bazą kandydatów. Lub zapytanie niepoprawne. Spróbuj ponownie później."))

@app.route(app_url+ '/vote_check', methods=['POST'])
def vote_check():
	values_dict = {}
	values_dict['token'] = session['token']
	values_dict['candidate_id'] = request.form["candidate"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
	requestedData = Request('http://localhost:8001/vote', data=values, headers=headers)
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200:
			session['has_voted'] = True
			return render_template('/error.html', message = u("Oddano głos. Dobra robota obywatelu."))
		else:
			return render_template('/error.html', message = u("Głos nieważny. Spróbuj ponownie później."))
	except Exception as e:
		print e
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))
@app.route(app_url + "/candidates", methods=['GET'])
def candidates_list():
        if voting_ended() != False:
                return get_results()
	candidates_list = []
	ids = []
	first_names = []
	last_names = []
	ages = []
	parties = []
	descriptions = []
	requestedData = Request('http://localhost:8001/candidates')
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200:
			candidates_list = response_dict['candidates_list']
			for value in candidates_list:
				ids.append(value['id'])
				first_names.append(value['first_name'])
				last_names.append(value['last_name'])
				ages.append(value['age'])
				parties.append(value['party'])
				descriptions.append(value['description'])
			return render_template('/candidates_list.html', ids=ids, first_names=first_names, last_names=last_names, ages=ages, parties=parties, descriptions=descriptions)
	except Exception as e:
		print e
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))
@app.errorhandler(404)
def page_not_found(e):
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=8002)
