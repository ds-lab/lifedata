from loguru import logger

from lifedata.lifedata_api.load_lifedata_api import Project
from lifedata.persistence.queryset_db_repository import QuerySetDBRepository


def load_queryset_into_database(
    project: Project, queryset_db_repository: QuerySetDBRepository
) -> None:
    logger.info("Loading new queryset ...")

    queryset = project.get_queryset()

    if len(queryset) > 0:
        queryset_db_repository.remove_queryset()
        queryset_db_repository.add_queryset(queryset)

        logger.info(f"Loaded queryset with {len(queryset)} items")
    else:
        logger.warning(
            "No new queryset found! Please check that you checked out your "
            "data for the project (dvc pull). If this doesn't help, try "
            "debugging the `get_queryset()` function in `lifedata_api.py`."
        )
