# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, request
import random, string, re
from urllib2 import Request, urlopen, HTTPError
from werkzeug import SharedDataMiddleware
import json, urllib
app_url = ''
app = Flask(__name__, static_url_path='//NO_IDEA_MATE', static_folder='static')
app.secret_key = "SecretAppKeyXxX"
    

app.debug = True

@app.route(app_url + '/')
def index():
    if session.has_key('pesel'):
        return render_template(app_url + '/logged.html', first_name = session['first_name'], second_name = session['last_name'])
    else:
        return render_template('/index.html')
@app.route(app_url + '/login')
def login():
	if session.has_key('pesel'):
		return redirect(app_url + '/logged')
	else:
		return render_template('/login.html')
#JUST WRONG
@app.route(app_url + '/check', methods=['POST', 'GET'])
def check():
	values_dict = {}
	values_dict['login'] = request.form["login"]
	values_dict['password'] = request.form["password"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
	requestedData = Request('http://edi.iem.pw.edu.pl/makosak/notes/login', data=values, headers=headers)
	try:
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200 and response_dict['message'] == 'OK':
			session['token'] = response_dict['token']
			session['user'] = response_dict['user']
			return redirect(app_url + '/logged')

		else:
			return render_template('/login_error.html')
		
	except HTTPError, error:
		print error.code 
		return render_template('/login_error.html')
@app.route(app_url + '/logged')
def logged():
	if session.has_key('pesel'):
		return render_template('/logged.html', first_name = session['first_name'], second_name = session['last_name']) #ZMIENNA VOTED?
	else:
		return redirect(app_url + '/')
@app.route(app_url + '/logout')
def logout():        
	session.clear()
	return redirect(app_url + '/')
#
#
#	else:
#		return redirect(app_url + '/login')
@app.route(app_url + '/vote')
def vote():
    if session.has_key('pesel'):#Sprawdzaj czy zagłosowane.
        return render_template('/vote.html', first_name = session['first_name'], second_name = session['last_name'])
    else:
        return redirect(app_url + '/login')
@app.route(app_url + "/candidates")
def candidates_list():
    return render_template('/candidates_list.html')

@app.errorhandler(404)
def page_not_found(e):
	print("Nie znaleziono strony.")
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
