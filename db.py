from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO, \
    DATABASE_PATH
from migrate.versioning import api
from app import db

import os.path
import click
import imp
import os


def get_database_version():
    return api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo('Database version: {}'.format(get_database_version()))


@cli.command()
def create():
    db.create_all()

    if not os.path.exists(SQLALCHEMY_MIGRATION_REPO):
        api.create(SQLALCHEMY_MIGRATION_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI,
                            SQLALCHEMY_MIGRATION_REPO,
                            api.version(SQLALCHEMY_MIGRATION_REPO))

    click.echo('Created database: {}'.format(DATABASE_PATH))


@cli.command()
def upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)
    version = get_database_version()
    click.echo('=> Upgraded database.\n'
               '=> Current version: {}\n'.format(version))


@cli.command()
def downgrade():
    version = get_database_version()
    previous_version = version - 1
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO,
                  previous_version)
    version = get_database_version()

    click.echo('=> Downgraded database.\n'
               '=> Previous version: {}.\n'
               '=> Current version: {}.\n'.format(previous_version, version))


@cli.command()
def migrate():
    version = get_database_version()
    migration = SQLALCHEMY_MIGRATION_REPO + ('/versions/%03d_migration.py' % (version + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI,
                                 SQLALCHEMY_MIGRATION_REPO)

    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                              SQLALCHEMY_MIGRATION_REPO,
                                              tmp_module.meta, db.metadata)

    open(migration, "wt").write(script)

    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATION_REPO)

    version = get_database_version()

    click.echo('=> New migration saved as {}.\n'
               '=> Current database version: {}.'.format(migration, version))


@cli.command()
def drop():
    db.drop_all()
    os.unlink(DATABASE_PATH)

    click.echo('Dropped database: {}.'.format(DATABASE_PATH))

if __name__ == '__main__':
    cli()
