# External Dependencies
from flask import Flask, request
# Internal Classes and Modules
## ./modules/route_handlers
from modules.route_handlers import Route_Handlers
## ./modules/api_helpers
from modules.api_helpers import InvalidUsage
## ./modules/api_helpers/utils.py
from modules.api_helpers.utils import validate_token
# Create app
app = Flask(__name__)

# Handles invaid request events
# Will raise an error and return back a body & status code
# Dependencies
#	InvalidUsage (ln 5)
#	jsonify (ln 3)
# Returns
#	response object
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	return Route_Handlers.handle_invalid_usage(error)

# GET /
# Returns Nothing
@app.route("/", methods=['GET'])
def getroot():
	return "The root of all evil"

# GET /collection/raw
# Optional querystring values
# sort, direction, offset, limit
# Returns [
#	{
#		folderId: <id>
#	},
#	{
#		folderId: <id>		
#}]
@app.route("/<collection>", methods=['GET'])
def get_collection(collection):
	return Route_Handlers.get_collection(collection)

# GET /collection/id
# aliases /collection/raw/id
@app.route("/<collection>/<id>", methods=['GET'])
def get_doc_by_id(collection, id):
	return Route_Handlers.get_doc_by_id(collection, id)

# POST /collection
# Expects JSON in body
# Returns full object + new id
@app.route("/<collection>", methods=['POST'])
def post_doc(collection):
	return Route_Handlers.post_doc(collection)

# PUT /collection
# Expects JSON in body
# Upserts
# Returns full object
@app.route("/<collection>/<id>", methods=['PUT'])
def put_doc(collection, id):
	return Route_Handlers.put_doc(collection, id)

# DELETE /collection/id
# Returns 204
@app.route("/<collection>/<id>", methods=['DELETE'])
def delete_doc(collection, id):
	return Route_Handlers.delete_doc(collection, id)

# Run App
if __name__ == "__main__":
	app.run(debug=True)