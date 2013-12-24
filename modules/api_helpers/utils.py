from flask import make_response
from pymongo import MongoClient
from . import InvalidUsage
from modules.backend_providers import Settings

def make_json_response(body, statusCode):
	resp = make_response(body, statusCode)
	resp.headers['Content-Type'] = 'application/json; charset=utf-8'
	return resp

def validate_token(req):
	try:
		token = req.headers["X-Token"]
	except Exception as e:
		raise InvalidUsage("No token in header", 401)

	try:
		if token is None:
			raise Exception("Invalid token", 401)
		if str(token) == "null":
			raise Exception("Invalid token", 401)
		if str(token) == "None":
			raise Exception("Invalid token", 401)
	except Exception as e:
		message, status_code = e.args
		raise InvalidUsage(message, status_code)

	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	users = db["users"]

	user = users.find_one({
			"token": token
		})

	try:
		if not user:
			raise Exception("Invalid token", 401)
	except Exception as e:
		message, status_code = e.args
		raise InvalidUsage(message, status_code)

	return True
