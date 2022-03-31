'''Module used by alembic to generate database migrations'''
from __future__ import with_statement

import sys

sys.path = ['', '..'] + sys.path[1:]

from alembic import context
from sqlalchemy import engine_from_config, pool
from app.database.database import Database

db = Database()
if db.engine is None:
    db.connect_database()

alembic_config = context.config
alembic_config.attributes['connection'] = db.engine

target_metadata = db.get_metadata()


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    if alembic_config.attributes.get('connection'):
        connectable = alembic_config.attributes.get('connection')
    else:
        connectable = engine_from_config(
            alembic_config.get_section(alembic_config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
