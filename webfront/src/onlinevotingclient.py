# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, request
import random, string, re
from urllib2 import Request, urlopen, HTTPError
from werkzeug import SharedDataMiddleware
import json, urllib
app_url = ''
app = Flask(__name__, static_url_path='/static', static_folder='static')
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
	values_dict['first_name'] = request.form["first_name"]
	values_dict['last_name'] = request.form["last_name"]
        values_dict['fathers_name'] = request.form["fathers_name"]
        values_dict['mothers_name'] = request.form["mothers_name"]
        values_dict['id_number'] = request.form["id_number"]
        values_dict['pesel'] = request.form["pesel"]
	values = json.dumps(values_dict)
	headers = {'Content-Type': 'application/json'}
        requestedData = Request('http://localhost:8001/login', data=values, headers=headers)
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
@app.route(app_url + "/candidates", methods=['GET'])
def candidates_list():
    candidates_list = []
    ids = []
    requestedData = Request('http://localhost:8001/candidates')
    print("I can't even try. MUTHAFUCKING IDIOTIC")
    response = urlopen(requestedData)
    response_dict = json.load(response)
    print("CAN A MAN GET A CODE?")
    if response.getcode() == 200:
        print("CODE WAS 200")
        candidates_list = response_dict['candidates_list']
        print(candidates_list)
        for value in candidates_list:
            ids.append(value['id'])
    return render_template('/candidates_list.html', ids=ids)
    #return render_template('/candidates_list.html', ids=ids)
@app.route(app_url + '/humunculus1')
def admin1_login():
    return render_template('/admin_login.html')
@app.route(app_url + '/humunculus2')
def admin2_login():
    return render_template('/admin_login.html')
@app.route(app_url + '/check_admin')
def check_admin():
    values_dict = {}
    values_dict['id_number'] = request.form["id_number"]
    values_dict['pesel'] = request.form["pesel"]
    values_dict['password'] = request.form["password"]
    values = json.dumps(values_dict)
    headers = {'Content-Type': 'application/json'}
    requestedData = Request('http://localhost:8001/login', data=values, headers=headers)
    try:
        response = urlopen(requestedData)
        response_dict = json.load(response)
        if response.getcode() == 200 and response_dict['message'] == 'OK':
            session['token'] = response_dict['token']
            session['user'] = response_dict['user']
            return redirect(app_url + '/logged')
        else:
            return render_template('/login_error.html')
    except Exception as e:
        return render_template('/login_error.html')
@app.errorhandler(404)
def page_not_found(e):
	print("Nie znaleziono strony.")
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0', port=8002)
