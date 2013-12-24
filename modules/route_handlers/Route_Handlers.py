from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo import ASCENDING
from pymongo import DESCENDING
from flask import request
from flask import jsonify
import hashlib, uuid
# Internal Classes and Modules
from modules.api_helpers.utils import make_json_response
from modules.backend_helpers import Settings
from modules.api_helpers import InvalidUsage

# App salt
# Move to different area, probably database it.
# APP_SALT = ''

# Utils
# Move to different module
def encrypt(u_salt, a_salt, un_salt):
	return hashlib.sha512(u_salt.encode('utf-8') + un_salt.encode('utf8') + a_salt.encode('utf-8')).hexdigest()

def make_token():
	return uuid.uuid4().hex

def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Route Handlers
def get_collection(collection):
	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	# if _collection exists return 200 + data
	if collection in db.collection_names():
		query_dictionary = {}
		sort_arg = None
		offset_arg = 0
		limit_arg = 0
		if request.args:
			reserved_property_list = ['sort', 'direction', 'offset', 'limit']
			if 'sort' in request.args:
				if 'direction' in request.args:
					direction = DESCENDING if request.args['direction'] == "desc" else ASCENDING
					sort_arg = [(request.args['sort'], direction)]
				else:
					sort_arg = [(request.args['sort'], ASCENDING)]
			if 'offset' in request.args:
				offset_arg = int(request.args['offset'])
			if 'limit' in request.args:
				limit_arg = int(request.args['limit'])
			for arg in request.args:
				if arg not in reserved_property_list:
					query_dictionary[arg] = request.args[arg]
		# Find the collection
		_collection = db[collection]
		data = list(_collection.find(query_dictionary, sort=sort_arg).skip(offset_arg).limit(limit_arg))
		resp = make_json_response(str(data), 200)
		return resp
	else:
		raise InvalidUsage('Resource does not exist', status_code=404)

def get_doc_by_id(collection, id):
	print(Settings.connection)
	print(Settings.port)
	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	# if collection exists
	if collection in db.collection_names():
		_collection = db[collection]
		data = _collection.find_one({"_id": ObjectId(str(id))})
		# if the specific resource does not exist
		if data:
			resp = make_json_response(str(data), 200)
			return resp
		else:
			raise InvalidUsage('Resource does not exist', status_code=404)
	else:
		raise InvalidUsage('Resource does not exist', status_code=404)

def post_doc(collection):
	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	request_data = request.get_json()
	if not request_data:
		raise InvalidUsage('Unsupported Media Type', status_code=415)
	else:
		_collection = db[collection]
		new_resource_id = _collection.insert(request_data)
		new_resource = _collection.find_one({"_id": new_resource_id})
		resp = make_json_response(str(new_resource), 201)
		return resp

def put_doc(collection, id):
	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	request_data = request.get_json()
	if not request_data:
		raise InvalidUsage('Unsupported Media Type', status_code=415)
	else:
		if collection in db.collection_names():
			_collection = db[collection]
			update_response = _collection.update({"_id": ObjectId(str(id))}, {"$set": request_data}, upsert=True)
			if update_response['updatedExisting'] == True:
				updated_resource = _collection.find_one({"_id": ObjectId(id)})
				resp = make_json_response(str(updated_resource), 201)
				return resp
			else:
				raise InvalidUsage('Error updating', status_code=500)
		else:
			raise InvalidUsage('Collection does not exist', status_code=404)

def delete_doc(collection, id):
	client = MongoClient(Settings.connection, Settings.port)
	db = client[Settings.database_name]
	if collection in db.collection_names():
		_collection = db[collection]
		doc_to_delete = _collection.find_one({"_id": ObjectId(id)})
		if doc_to_delete:
			_collection.remove(ObjectId(id))
			resp = make_response()
			resp.status_code = 204
			return resp
		else:
			raise InvalidUsage('Resource does not exist', status_code=404)
	else:
		raise InvalidUsage('Collection does not exist', status_code=404)