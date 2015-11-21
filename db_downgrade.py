from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO


version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO, version - 1)
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)

print("Current database version: ", version)