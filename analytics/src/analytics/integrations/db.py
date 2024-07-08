# pylint: disable=invalid-name, line-too-long
"""Get a connection to the database using a SQLAlchemy engine object."""

from sqlalchemy import Engine, create_engine

from config import DBSettings


# The variables used in the connection url are set in settings.toml and
# .secrets.toml. These can be overridden with the custom prefix defined in config.py: "ANALYTICS".
# e.g. `export ANALYTICS_POSTGRES_USER=new_usr`.
# Docs: https://www.dynaconf.com/envvars/
def get_db() -> Engine:
    """
    Get a connection to the database using a SQLAlchemy engine object.

    This function retrieves the database connection URL from the configuration
    and creates a SQLAlchemy engine object.

    Yields
    ------
    sqlalchemy.engine.Engine
    A SQLAlchemy engine object representing the connection to the database.
    """
    db = DBSettings()
    print(f"postgresql+psycopg://{db.user}:{db.password}@{db.db_host}:{db.port}")
    return create_engine(
        f"postgresql+psycopg://{db.user}:{db.password}@{db.db_host}:{db.port}",
        pool_pre_ping=True,
        hide_parameters=True,
    )
