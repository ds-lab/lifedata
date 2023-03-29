from typing import Iterable
from typing import List

from ..annotations.sample import Sample
from ..annotations.sample import SampleRepository
from ..persistence import models
from .database import Session
from .models import Sample as SampleModel


class SampleDBRepository(SampleRepository):
    """
    Handle loaded samples in the database.
    """

    def __init__(self, db: Session):
        self._db = db

    def _instantiate_sample(self, model: models.Sample) -> Sample:
        return Sample(id=model.id)

    def load_samples(self, samples: Iterable[Sample]) -> int:
        samples = list(samples)

        ids = {s.id for s in samples}
        existing_ids = {
            row[0]
            for row in (
                self._db.query(SampleModel)
                .filter(SampleModel.id.in_(ids))
                .values(SampleModel.id)
            )
        }

        new_ids = ids - existing_ids
        sample_mappings = [{"id": new_id} for new_id in new_ids]

        if sample_mappings:
            self._db.bulk_insert_mappings(SampleModel, sample_mappings)
        return len(sample_mappings)

    def get_sample_ids(self):
        return self._db.query(SampleModel).values(SampleModel.id)

    def query_samples(self) -> List[Sample]:
        samples_query_results = self._db.query(SampleModel).values(SampleModel.id)

        samples = [self._instantiate_sample(a) for a in samples_query_results]

        return samples
