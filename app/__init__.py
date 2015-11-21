from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api


app = Flask(__name__)
api = Api(app)

# load configuration file
app.config.from_object('config')

# database initialization
db = SQLAlchemy(app)

from app.resources import RouteListAPI

api.add_resource(RouteListAPI, '/routes', endpoint='routes')
