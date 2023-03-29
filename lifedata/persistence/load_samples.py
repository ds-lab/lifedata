from loguru import logger
from toolz import partition_all

from lifedata.annotations.sample_repository import SampleProjectRepository
from lifedata.persistence.sample_db_repository import SampleDBRepository


def check_samples_in_sync(
    sample_repository: SampleProjectRepository, sample_db_repository: SampleDBRepository
) -> None:
    local_sample_ids = [
        sample_object.id for sample_object in list(sample_repository.load_all())
    ]
    db_sample_ids = [
        db_row[0] for db_row in list(sample_db_repository.get_sample_ids())
    ]

    if set(local_sample_ids) - set(db_sample_ids):
        raise Exception(
            f"The following samples exist locally, but not in database {set(local_sample_ids) - set(db_sample_ids)}. Ensure that the local and database samples are equal."
        )

    if set(db_sample_ids) - set(local_sample_ids):
        raise Exception(
            f"The following samples exist in the database, but not locally {set(db_sample_ids) - set(local_sample_ids)}. Ensure that the local and database samples are equal."
        )


def load_samples_into_database(
    sample_project_repository: SampleProjectRepository,
    sample_db_repository: SampleDBRepository,
) -> None:
    batch_size = 10000
    samples = list(sample_project_repository.load_all())

    loaded = 0
    new_loaded = 0
    logger.info(f"Loading {len(samples)} samples ...")

    for batch in partition_all(batch_size, samples):
        loaded += len(batch)
        new_loaded += sample_db_repository.load_samples(batch)
        logger.info(f"{loaded}/{len(samples)}...")

    if loaded == 0:
        logger.warning(
            "No samples found! Please check that you checked out your data for "
            "the project (dvc pull). If this doesn't help, try debugging the "
            "`get_all_sample_ids()` function in `lifedata_api.py`."
        )
    logger.info(f"Loaded {new_loaded} new samples (out of {loaded} total samples)")
