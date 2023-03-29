import sys
from datetime import datetime
from typing import Optional

import click
from fastapi.encoders import jsonable_encoder

from lifedata.cli.configure_db import db_option
from lifedata.cli.main import main
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository
from lifedata.persistence.database import configure_database
from lifedata.persistence.database import Session


@main.group(invoke_without_command=True)
def reporting() -> None:
    """
    Commands to get data reports
    """
    pass


@reporting.command()
@db_option()
@click.option(
    "--interval-start-date",
    "interval_start_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
)
@click.option(
    "--interval-stop-date",
    "interval_stop_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
)
def annotation_report(
    db: str,
    interval_start_date: Optional[datetime],
    interval_stop_date: Optional[datetime],
) -> None:
    """
    Command to create annotation report
    """
    configure_database(db)

    session = Session()
    annotation_db_repository = AnnotationsDBRepository(session)

    queried_annotation_report = annotation_db_repository.query_annotation_report(
        interval_start_date, interval_stop_date
    )

    queried_annotation_report_dict = [
        row._asdict() for row in queried_annotation_report
    ]

    annotation_report = {
        "request_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "Annotation report": queried_annotation_report_dict,
    }

    annotation_report = jsonable_encoder(annotation_report)

    sys.stdout.write(f"{annotation_report} \n")
