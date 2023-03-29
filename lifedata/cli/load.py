from .configure_db import db_option
from .main import main
from lifedata.annotations.sample_repository import SampleProjectRepository
from lifedata.lifedata_api.load_lifedata_api import load_project_api
from lifedata.persistence.database import configure_database
from lifedata.persistence.database import Session
from lifedata.persistence.load_queryset import load_queryset_into_database
from lifedata.persistence.load_samples import check_samples_in_sync
from lifedata.persistence.load_samples import load_samples_into_database
from lifedata.persistence.queryset_db_repository import QuerySetDBRepository
from lifedata.persistence.sample_db_repository import SampleDBRepository


@main.group()
def load():
    """
    Load data in the lifedata database
    """
    pass


@load.command()
@db_option()
def samples(db: str) -> None:
    """
    Find available samples in the project and load them into the database to
    make them available for annotation.

    This is using the function ``get_all_sample_ids()`` from the project's
    ``lifedata_api.py``.
    """
    configure_database(db)

    session = Session()
    project = load_project_api()

    sample_repository = SampleProjectRepository(project)
    sample_db_repository = SampleDBRepository(session)

    load_samples_into_database(sample_repository, sample_db_repository)

    session.commit()

    check_samples_in_sync(sample_repository, sample_db_repository)


@load.command()
@db_option()
def queryset(db: str) -> None:
    """
    Load entries of the produced queryset into the database.
    """
    configure_database(db)

    session = Session()
    project = load_project_api()
    queryset_db_repository = QuerySetDBRepository(session)

    load_queryset_into_database(project, queryset_db_repository)

    session.commit()
