import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO

version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
migration = SQLALCHEMY_MIGRATION_REPO + ('/versions/%03d_migration.py' % (version + 1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)

exec(old_model, tmp_module.__dict__)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO, tmp_module.meta, db.metadata)

open(migration, "wt").write(script)

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)

print("New migration saved as ", migration)
print("Current database version: ", version)
