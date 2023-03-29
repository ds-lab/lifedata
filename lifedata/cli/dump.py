import sys

from fastapi.encoders import jsonable_encoder

from lifedata.cli.configure_db import db_option
from lifedata.cli.main import main
from lifedata.cli.query_db_state import query_labeled_state
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository
from lifedata.persistence.database import configure_database
from lifedata.persistence.database import Session


@main.group(invoke_without_command=True)
def dump() -> None:
    """
    Dump data states
    """
    pass


@dump.command()
@db_option()
def labelstate(db: str) -> None:
    """
    Dump labeled state as json to your console
    """
    configure_database(db)

    session = Session()
    annotation_db_repository = AnnotationsDBRepository(session)

    sys.stdout.write(
        f"{jsonable_encoder(query_labeled_state(annotation_db_repository))}\n"
    )
