import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    APP_DATABASE_URL = os.environ.get("APP_DATABASE_URL", None)

    if not APP_DATABASE_URL:
        # Setting the database url to a dummy postgres schema. Setting no url would
        # fail right away, but having the dummy url will defer failing to when some
        # code parts are trying to access the database.
        APP_DATABASE_URL = "postgresql://"

    return APP_DATABASE_URL


def get_engine() -> Engine:
    return create_engine(get_database_url())


def configure_database(url: str) -> None:
    """
    Allows the configuration of the database url after the process startup.
    I.e. for configuring a database url that was not passed by the
    environment variable byt by other means, like a cli option.
    """
    os.environ["APP_DATABASE_URL"] = url
    Session.configure(bind=get_engine())


Session: _Session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

Base = declarative_base()
