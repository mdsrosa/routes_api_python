import os


DEBUG = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,
                                                      'routes_api.db')
DATABASE_CONNECTION_OPTIONS = {}