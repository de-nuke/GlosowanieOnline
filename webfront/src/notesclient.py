# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for, request
import random, string, re
from urllib2 import Request, urlopen, HTTPError
from werkzeug import SharedDataMiddleware
import json, urllib
app_url = '/site'
app = Flask(__name__, static_url_path='/makosak/notesclient/static', static_folder='static')
app.secret_key = "SecretAppKeyXxX"


app.debug = True


@app.route(app_url + '/login')
def login():
	if session.has_key('user'):
		return redirect(app_url + '/notes')
	else:
		return render_template('/login.html')

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
			return redirect(app_url + '/notes')

		else:
			return render_template('/login_error.html')
		
	except HTTPError, error:
		print error.code 
		return render_template('/login_error.html')
@app.route(app_url + '/notes')
def notes():
	if session.has_key('user'):
		return render_template('/notes.html', user = session['user'], message = "Wybierz co chcesz zobic z panelu po lewej stronie.")
	else:
		return redirect(app_url + '/login')

@app.route(app_url + '/new_note')
def new_note():
	if session.has_key('user'):
                return render_template('/new_note.html')
        else:
                return redirect(app_url + '/login')

@app.route(app_url + '/created', methods=['POST'])
def created():
	if session.has_key('user'):
		headers = {"Content-Type" : 'application/json', "token" : session['token']}
		data_dict = {}
		data_dict['title'] = request.form["new_note_title"]
		data_dict['content'] = request.form["new_note_content"]
		data_dict['category'] = request.form["new_note_category"]
		data_dict['tag'] = request.form["new_note_tag"]
		data = json.dumps(data_dict)
		requestedData = Request('http://edi.iem.pw.edu.pl/makosak/notes', data=data, headers=headers)
                response = urlopen(requestedData)
                response_dict = json.load(response)
                if response_dict['message'] == "OK":
			return render_template('/notes.html', user = session['user'], message = "Utworzono notatke")
		else:
			return render_template('/notes.html', user = session['user'], message = "Nie udalo sie utworzyc notatki")
	else:
		return redirect(app_url + '/login')

@app.route(app_url + '/edit/<id>', methods=['PUT'])
def edit(id):
	if session.has_key('user'):
		headers = {"token" : session['token'], "Content-Type" : 'application/json'}
                requestedData = Request("http://edi.iem.pw.edu.pl/makosak/notes/" + str(id), headers=headers)
		response = urlopen(requestedData)
                response_dict = json.load(response)
                if response.getcode() == 200:
                       	title = response_dict['title']
                       	content = response_dict['content']
                       	category = response_dict['category']
                       	tag = response_dict['tag']
			return render_template('/edit_note.html', id=id, title = title, tag=tag, category=category, content=content)
		else:
                       	return render_template('/alert.html', message = "Nie udalo sie otworzyc notatki")
	else:
		return redirect(app_url + '/login')
@app.route(app_url + '/edited/<id>', methods=['PUT', 'POST'])
def edited(id):
	if session.has_key('user'):
                headers = {"token" : session['token'], "Content-Type" : 'application/json'}
		data_dict = {}
                data_dict['title'] = request.form["edited_note_title"]
                data_dict['content'] = request.form["edited_note_content"]
                data_dict['category'] = request.form["edited_note_category"]
                data_dict['tag'] = request.form["edited_note_tag"]
		data = json.dumps(data_dict)
                requestedData = Request("http://edi.iem.pw.edu.pl/makosak/notes/" + str(id), data=data, headers=headers)
		requestedData.get_method = lambda: 'PUT'
                try:
			urlopen(requestedData)
                        requestedData.get_method = lambda: 'GET'
                        return render_template('/notes.html', user = session['user'], message  = "Edytowano notatke")
                except HTTPError, e:
                        return render_template('/notes.html', user = session['user'], message  = "Edycja notatki nie powiodla sie")
	else:
		return redirect(app_url + '/login')

@app.route(app_url + '/logout')
def logout():
	session.clear()
	return redirect(app_url + '/login')

@app.route(app_url + '/delete/<id>', methods=['DELETE'])
def delete(id):
	if 'user' in session:
        	headers = {"token" : session['token'], "Content-Type" : 'application/json'}
        	requestedData = Request("http://edi.iem.pw.edu.pl/makosak/notes/" + str(id), headers=headers)
		requestedData.get_method = lambda: 'DELETE'
		try:
			urlopen(requestedData)
			requestedData.get_method = lambda: 'GET'
			return render_template('/alert.html', alert  = "Usunieto notatke")
		except HTTPError, e:
			return render_template('/alert.html', alert  = "Usunieto notatke")
	else:
                return redirect(app_url + '/login')


@app.route(app_url + '/display/<id>', methods=['GET'])
def display(id):
	if 'user' in session:
		headers = {"token" : session['token'], "Content-Type" : 'application/json'}
		requestedData = Request("http://edi.iem.pw.edu.pl/makosak/notes/" + str(id), headers=headers)
		response = urlopen(requestedData)
		response_dict = json.load(response)
		if response.getcode() == 200:
			title = response_dict['title']
			content = response_dict['content']
			category = response_dict['category']
			tag = response_dict['tag']
			return render_template("single_note.html", id=id, title=title, content=content, category=category, tag=tag)
		else:
			return render_template("alert.html", alert="Niestety nie udalo sie wyswietlic wiadomosci...")
	else:
		return redirect(app_url + '/login')

@app.route(app_url + '/get_all_notes', methods=['GET'])
def get_all_notes():
	if 'user' in session:
		headers = {"token": session['token'], "Content-Type" : 'application/json'}
		requestedData = Request("http://edi.iem.pw.edu.pl/makosak/notes", headers=headers)
		response = urlopen(requestedData)
		response_dict = json.load(response)
        	ids = []
       		titles = []
		categories = []
		tags = []
        	for i in response_dict:
				print i
				ids.append(i["id"])
	       	                titles.append(i["title"])
        	                categories.append(i["category"])
				tags.append(i['tag'])
		return render_template("note_list.html", ids=ids, titles=titles, categories=categories, tags=tags)
	else:
		return redirect(app_url + '/login')
@app.route(app_url + '/get_notes/category/' + "<category>")
def get_notes_by_category(category):
	return
@app.route(app_url + '/get_notes/tag/' + "<tag>"  )
def get_notes_by_tag(tag):
	return

@app.route(app_url)
def normalpath():
	return redirect(app_url + '/notes')
@app.errorhandler(404)
def page_not_found(e):
	print("Nie znaleziono strony.")
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
