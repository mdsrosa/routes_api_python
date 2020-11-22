from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

api = Api(app)

# database initialization
db = SQLAlchemy(app)


# http error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)

# api error handling
api_errors = {
    'NotFound': {
        'message': 'Route not found',
        'status': 404
    }
}

api.errors = api_errors

from app.resources import RoutesAPI, RouteAPI, RouteCalculateCostAPI

api.add_resource(RoutesAPI, '/routes', endpoint='routes')
api.add_resource(RouteAPI, '/routes/<int:pk>', endpoint='route')
api.add_resource(RouteCalculateCostAPI, '/routes/calculate-cost',
                 endpoint='route_calculate_cost')


@app.route("/", methods=['GET'])
def index():
    return 'Routes API Python Version :)\n'
