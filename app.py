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
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	return Route_Handlers.handle_invalid_usage(error)

# GET /
# Returns Nothing
@app.route("/", methods=['GET'])
def getroot():
	return "The root of all evil"

# GET /collection
# Optional querystring values
# sort, direction, offset, limit
@app.route("/<collection>", methods=['GET'])
def get_collection(collection):
	return Route_Handlers.get_collection(collection)

# GET /collection/id
@app.route("/<collection>/<id>", methods=['GET'])
def get_doc_by_id(collection, id):
	return Route_Handlers.get_doc_by_id(collection, id)

# POST /collection
@app.route("/<collection>", methods=['POST'])
def post_doc(collection):
	return Route_Handlers.post_doc(collection)

# PUT /collection
# Upserts
@app.route("/<collection>/<id>", methods=['PUT'])
def put_doc(collection, id):
	return Route_Handlers.put_doc(collection, id)

# DELETE /collection/id
@app.route("/<collection>/<id>", methods=['DELETE'])
def delete_doc(collection, id):
	return Route_Handlers.delete_doc(collection, id)

# Run App
if __name__ == "__main__":
	app.run(debug=True)