from pathlib import Path

import click

from .configure_db import db_option
from .main import main
from lifedata.persistence.database import configure_database
from lifedata.persistence.migrations.run_migrations import upgrade_to_head


@main.command()
@db_option()
def migrate_db(db: str) -> None:
    """
    Update the database with given alembic file
    """

    configure_database(db)

    file_path = Path(__file__).parent.parent
    file_name = "alembic.ini"

    if (file_path / file_name).exists():
        upgrade_to_head()
    else:
        raise click.FileError(
            str(file_path / file_name), hint=f"Ensure alembic.ini exists in {file_path}"
        )
