# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, request
import random, string, re, sys
from urllib2 import Request, urlopen, HTTPError
from werkzeug import SharedDataMiddleware
import json, urllib
app_url = ''
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "SecretAppKeyXxX"
app.debug = True

def u(string):
	return unicode(string, "utf-8")
@app.route(app_url + '/')
def index():
	if session.has_key('token'):
		return render_template(app_url + '/logged.html', first_name = session['first_name'], second_name = session['last_name'])
	else:
		return render_template('/index.html')
@app.route(app_url + '/login')
def login():
	if session.has_key('token'):
		return redirect(app_url + '/logged')
	else:
		return render_template('/login.html')
@app.route(app_url + '/check', methods=['POST', 'GET'])
def check():
	values_dict = {}
	values_dict['first_name'] = request.form["first_name"]
	values_dict['last_name'] = request.form["last_name"]
	values_dict['age'] = 0
	values_dict['father_name'] = request.form["fathers_name"]
	values_dict['mother_name'] = request.form["mothers_name"]
	values_dict['id_series_number'] = request.form["id_number"]
	values_dict['pesel'] = request.form["pesel"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
	requestedData = Request('http://localhost:8001/login', data=values, headers=headers)
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		print(response)
		print(response_dict)
		if response.getcode() == 200:
			session['token'] = response_dict['token']
			session['first_name'] = values_dict['first_name']
			session['last_name'] = values_dict['last_name']
			#session['has_voted'] = response_dict['has_voted']
			session['has_voted'] = False
			return redirect(app_url + '/logged')
		else:
			return render_template('/error.html', message = u("Nieprawidłowe dane logowania!"))
	except HTTPError, error:
		print error.code 
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))
@app.route(app_url + '/logged')
def logged():
	if session.has_key('token'):
		return render_template('/logged.html', first_name = session['first_name'], last_name = session['last_name'], has_voted = session['has_voted'])
	else:
		return redirect(app_url + '/')
@app.route(app_url + '/logout')
def logout():		
	session.clear()
	return redirect(app_url + '/')
@app.route(app_url + '/vote')
def vote():
	if session.has_key('token'):
		if session['has_voted'] == True:
			return render_template('/error.html', message = u("Już głosowałeś."))
		return render_template('/vote.html', first_name = session['first_name'], second_name = session['last_name'])
	else:
		return redirect(app_url + '/login')
@app.route(app_url+ '/vote_check', methods=['POST'])
def vote_check():
	values_dict = {}
	#name will vary...
	values_dict['candidate'] = request.form["candidate"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
	requestedData = Request('http://localhost:8001/vote', data=values, headers=headers)
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		print(response)
		print(response_dict)
		if response.getcode() == 200:
			return render_template('/error.html', message = u("Oddano glos Dobra robota obywatelu"))
		else:
			return render_template('/error.html', message = u("Głos nieważny. Spróbuj ponownie później."))
	except HTTPError, error:
		print error.code
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))

@app.route(app_url + "/candidates", methods=['GET'])
def candidates_list():
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
		return render_template('/error.html', message = u("Zapytanie nie było poprawne."))
@app.errorhandler(404)
def page_not_found(e):
	print("Nie znaleziono strony.")
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=8002)
