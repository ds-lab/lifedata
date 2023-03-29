from typing import Any
from typing import NewType
from typing import Optional

from loguru import logger

from lifedata.lifedata_api.load_lifedata_api import load_project_api

SampleDisplayData = NewType("SampleDisplayData", Any)  # type: ignore


def load_sample_display_data(sample_id: str) -> Optional[dict]:
    try:
        project = load_project_api()
        return project.read_sample_for_display(sample_id)
    except Exception as exc:
        logger.exception(
            f"Tried to load sample display data for '{sample_id}', but got an error."
        )
        raise exc
