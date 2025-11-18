from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the Flask app factory and database
from app import create_app, db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# Flask-Migrate doesn't use alembic.ini, so we only load it if it exists
if config.config_file_name is not None and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# Flask-Migrate provides the app via context, but we need to create it
# We'll create it inside the migration functions to avoid context conflicts
def get_app():
    """Get the Flask app instance"""
    return create_app()

# Get the database metadata - will be set in migration functions
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get app and db metadata
    app = get_app()
    # Flask-Migrate manages context, but we need app context for config access
    url = None
    metadata = None
    with app.app_context():
        url = app.config["SQLALCHEMY_DATABASE_URI"]
        metadata = db.metadata
    
    context.configure(
        url=url,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get app and db metadata
    app = get_app()
    # Get config and metadata outside of Flask-Migrate's context
    db_url = None
    metadata = None
    with app.app_context():
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        metadata = db.metadata
    
    # Create connection outside of app context to avoid conflicts
    connectable = engine_from_config(
        {"sqlalchemy.url": db_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

