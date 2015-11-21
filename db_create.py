from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO
from app import db
import os.path

db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATION_REPO):
    api.create(SQLALCHEMY_MIGRATION_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO,
                        api.version(SQLALCHEMY_MIGRATION_REPO))
