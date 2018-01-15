# -*- coding: utf-8 -*-
from flask import Flask, request, Response, json, g
import jwt
app_url = '/makosak/notes'
app = Flask(__name__)
app.secret_key = "SecretAppKeyXxX"


app.debug = True


users = {}
users['user'] = {'password' : 'user', 'notes' : {}}
users['bach'] = {'password' : 'to-nie-ja', 'notes' : {}}

def make_token(user):
	payload = {'user' : user}
	token = jwt.encode(payload, app.secret_key, algorithm='HS256')
	return token.decode('unicode_escape')

def get_user(token):
	try:
		payload = jwt.decode(token, app.secret_key, algorithm='HS256')
	except:
		return None
	if 'user' in payload:
		if payload['user'] in users:
			return payload['user']
		else:
			return None
	else:
		return None

#Login
@app.route(app_url + '/login', methods=['POST'])
def login():
	status = 400
	data = None
	data_read = False
	try:
		data = json.loads(request.data)
		data_read = True
	except:
		response = {'error' : 'Dane wprowadzone w niepoprawnym formacie, nie udalo sie stworzyc slownika'}
	if data_read == True:
		if 'login' in data and 'password' in data:
			user = data['login']
			password = data['password']
			if users[user]['password'] == password:
				response_data = {'message' : 'OK', 'token' : make_token(user), 'user' : user}
				status = 200
			else:
				response = {'error' : 'Niepoprawny login lub haslo'}
		else:
			response_data = {'error' : 'Niepodano loginu lub hasla'}
	else:
		response_data = {'error' : 'Dane wprowadzone w niepoprawnym formacie, nie przeczytano danych'}
	headers = {'Content-Type' : 'application/json'}
	return make_response(response_data, status, headers)
#Add note
@app.route(app_url, methods=['POST'])
def add_note():
	status = 400
	data = None
	data_read = False
	headers = {'Content-Type' : 'application/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			try:
				data = json.loads(request.data)
				data_read = True
			except:
				response_data = {'error' : 'Dane wprowadzone w niepoprawnym formacie'}
			if data_read == True:
				if 'content' in data and 'title' in data:
					i = 1
					while i in users[user]['notes']:
						i += 1
					if data['category'] != "":
						category = data['category']
					else:
						category = 'No category'
					if data['tag'] != "":
						  tag = data['tag']
					else:
							 tag = 'No tag'

					users[user]['notes'][i] = {'id' : i, 'title' : data['title'], 'content' : data['content'], 'category' : category, 'tag' : tag}
					response_data = {"message" : "OK", "id" : i, "title" : data["title"], "content" : data["content"], "category" : category, "tag" : tag}
					status = 200
				else:
					response_data = {'error' : 'Dane wprowadzone w niepoprawnym formacie'}
			else:
				response_data = {'error' : 'Nie udalo sie odczytac danych'}
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}	
	return make_response(response_data, status, headers)

@app.route(app_url+"/<int:id>", methods=['GET'])
def get_note(id):
	status = 400
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			if id in users[user]['notes']:
				response_data = {"message" : "OK", "id" : id, "title" : users[user]['notes'][id]["title"], "content" : users[user]['notes'][id]["content"], "category" : users[user]['notes'][id]["category"], "tag" : users[user]['notes'][id]["tag"]}
				status = 200
			else:
				response_data = {'error' : "Nie ma wiadomosci o podanym id dla danego uzytkownika"}
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerachX DX XXD XDX DX '}
	return make_response(response_data, status, headers)



@app.route(app_url + "/<int:id>", methods=['PUT'])
def edit_note(id):
	status = 400
	data = None
	data_read = False
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			try:
				 data = json.loads(request.data)
				 data_read = True
			except:
				 response_data = {'error' : 'Dane wprowadzone w niepoprawnym formacie'}
			if data_read == True:
				if id in users[user]['notes']:
					if 'content' in data:
						users[user]['notes'][id]['content'] = data['content']
					if 'title' in data:
						users[user]['notes'][id]['title'] = data['title']
					if 'tag' in data:
						users[user]['notes'][id]['tag'] = data['tag']
					if 'category' in data:
						users[user]['notes'][id]['category'] = data['category']
					response_data = {"message" : "OK", "id" : id, "title" : users[user]['notes'][id]['title'], "content" : users[user]['notes'][id]['content'], "category" : users[user]['notes'][id]['category'], "tag" : users[user]['notes'][id]['tag']}
					status = 200
				else:
					response_data = {'error' : "Nie ma wiadomosci o podanym id dla danego uzytkownika"}
			else:
				response_data = {'error' : 'Dane wprowadzone w niepoprawnym formacie'}
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}
	return make_response(response_data, status, headers)




@app.route(app_url+"/<int:id>", methods=['DELETE'])
def delete_note(id):
	status = 400
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			if id in users[user]['notes']:
				users[user]['notes'].pop(id)
				response_data = {"message" : "OK"}
			else: 
				response_data = {'error' : "Nie ma wiadomosci o podanym id dla danego uzytkownika"}
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}
	return make_response(response_data, status, headers)


@app.route(app_url, methods=['GET'])
def get_all_notes():
	status = 400
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			status = 200
			notes_list = []
			for i in users[user]['notes']:
				notes_list.append(users[user]['notes'][i])
			response_data = notes_list
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}
	return make_response(response_data, status, headers)
	
@app.route(app_url + '/category/<cat>', methods=['GET'])
def get_notes_with_category(cat):
	status = 400
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			status = 200
			notes_list = []
			i = 1
			for i in users[user]['notes']:
				if str(cat) == str(users[user]['notes'][i]['category']):
					notes_list.append(users[user]['notes'][i])
			response_data = notes_list
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}
	return make_response(response_data, status, headers)

@app.route(app_url + '/tag/<tag>', methods=['GET'])
def get_notes_with_tag(tag):
	status = 400
	headers = {'Content-Type' : 'applicatiion/json'}
	if 'token' in request.headers:
		if get_user(request.headers['token']) != None:
			user = get_user(request.headers['token'])
			status = 200
			notes_list = []
			i = 1
			for i in users[user]['notes']:
				if str(tag) == str(users[user]['notes'][i]['tag']):
					notes_list.append(users[user]['notes'][i])
			response_data = notes_list
		else:
			status = 401
			response_data = {'error' : 'Brak uprawnien'}
	else:
		response_data = {'error' : 'Nie podano tokenu w headerach'}
	return make_response(response_data, status, headers)



def make_response(data, status, headers):
	response = Response(json.dumps(data), status=status, mimetype='application/json', headers=headers)
	return response
	

@app.route(app_url)
def normalpath():
	return redirect(app_url + '/mailbox')
@app.errorhandler(404)
def page_not_found(e):
	print("Nie znaleziono strony.")
	return "Nie znaleziono strony."
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
