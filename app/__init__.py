from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# load configuration file
app.config.from_object('config')

# database initialization
db = SQLAlchemy(app)
db.create_all()
