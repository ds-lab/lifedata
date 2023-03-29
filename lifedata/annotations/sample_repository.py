from typing import Iterable

from .sample import Sample
from lifedata.lifedata_api.load_lifedata_api import Project


class SampleProjectRepository:
    """
    Finding samples in the project and retrieving them by id.
    """

    def __init__(self, project: Project):
        self._project = project

    def load_all(self) -> Iterable[Sample]:
        find_sample_ids = self._project.get_all_sample_ids()

        for sample_id in find_sample_ids:
            yield Sample(id=sample_id)  # type: ignore

    def by_id(self, id: str) -> Sample:
        return Sample(id=id)  # type: ignore
